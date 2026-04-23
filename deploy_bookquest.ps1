param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message,
    [Alias("v")][string]$Version
)

# BookQuest deploy script
# Usage:
#   .\deploy_bookquest.ps1 "hotfix message"            (cache bump only)
#   .\deploy_bookquest.ps1 -v 1.5.0 "release msg"      (version + changelog bump)

$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$utf8NoBom = New-Object System.Text.UTF8Encoding $false

# Korean literals built from [char] so this script stays ASCII-safe.
#   jemok   (title)   = U+C81C U+BAA9
#   byeongyeong (changes) = U+BCC0 U+ACBD
$K_TITLE   = [char]0xC81C + [char]0xBAA9               # (title)
$K_CHANGES = [char]0xBCC0 + [char]0xACBD               # (changes)
$K_HEAD    = "# " + [char]0xB2E4 + [char]0xC74C + " " + [char]0xB9B4 + [char]0xB9AC + [char]0xC2A4 + " " + [char]0xC2A4 + [char]0xD14C + [char]0xC774 + [char]0xC9D5
# (Header: next release staging)

function Read-Utf8 ([string]$path) {
    return [System.IO.File]::ReadAllText($path, $utf8NoBom)
}
function Write-Utf8 ([string]$path, [string]$content) {
    [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
}

# Stale lock cleanup
$lock = Join-Path $repoRoot ".git\index.lock"
if (Test-Path $lock) {
    Remove-Item $lock -Force
    Write-Host "  - stale .git\index.lock removed" -ForegroundColor DarkGray
}

git config core.autocrlf true | Out-Null

# Release mode
if ($Version) {
    $stagingPath = Join-Path $repoRoot "NEXT_RELEASE.md"
    $indexPath = Join-Path $repoRoot "index.html"

    if (-not (Test-Path $stagingPath)) {
        Write-Error "NEXT_RELEASE.md not found"
        exit 1
    }
    if (-not (Test-Path $indexPath)) {
        Write-Error "index.html not found"
        exit 1
    }

    $staging = Read-Utf8 $stagingPath

    # Build patterns dynamically using Korean chars via [char] constants
    $titlePattern = "(?ms)^##\s*" + [regex]::Escape($K_TITLE) + "\s*\r?\n(?<t>.+?)(?=\r?\n##|\Z)"
    $titleMatch = [regex]::Match($staging, $titlePattern)
    if (-not $titleMatch.Success) {
        Write-Error "NEXT_RELEASE.md: '## $K_TITLE' section missing"
        exit 1
    }
    $releaseTitle = $titleMatch.Groups["t"].Value.Trim()
    if (-not $releaseTitle) {
        Write-Error "NEXT_RELEASE.md: release title is empty"
        exit 1
    }

    $changesPattern = "(?ms)^##\s*" + [regex]::Escape($K_CHANGES) + "\s*\r?\n(?<c>.+?)\Z"
    $changesMatch = [regex]::Match($staging, $changesPattern)
    if (-not $changesMatch.Success) {
        Write-Error "NEXT_RELEASE.md: '## $K_CHANGES' section missing"
        exit 1
    }
    $bulletLines = @()
    foreach ($line in ($changesMatch.Groups["c"].Value -split "\r?\n")) {
        $trim = $line.Trim()
        if ($trim -match "^-\s+(.+)$") {
            $bulletLines += $matches[1].Trim()
        }
    }
    if ($bulletLines.Count -eq 0) {
        Write-Error "NEXT_RELEASE.md: no '- ' bullets found in changes"
        exit 1
    }

    $today = Get-Date -Format "yyyy-MM-dd"

    function Escape-JS ([string]$s) {
        return $s.Replace("\", "\\").Replace('"', '\"')
    }

    $changesLines = ($bulletLines | ForEach-Object { '          "' + (Escape-JS $_) + '"' }) -join ",`r`n"
    $titleJS = Escape-JS $releaseTitle

    $newEntry = "      {`r`n" +
                "        version: `"$Version`",`r`n" +
                "        date: `"$today`",`r`n" +
                "        title: `"$titleJS`",`r`n" +
                "        changes: [`r`n" +
                "$changesLines`r`n" +
                "        ]`r`n" +
                "      },"

    $indexContent = Read-Utf8 $indexPath
    $origIndexContent = $indexContent       # keep pristine backup in memory
    $origLength = $indexContent.Length

    $verPattern = 'const\s+APP_VERSION\s*=\s*"[^"]*"\s*;'
    $verReplace = 'const APP_VERSION = "' + $Version + '";'
    if ($indexContent -match $verPattern) {
        $indexContent = [regex]::Replace($indexContent, $verPattern, $verReplace)
    }

    $datePattern = 'const\s+APP_BUILD_DATE\s*=\s*"[^"]*"\s*;'
    $dateReplace = 'const APP_BUILD_DATE = "' + $today + '";'
    if ($indexContent -match $datePattern) {
        $indexContent = [regex]::Replace($indexContent, $datePattern, $dateReplace)
    }

    $anchor = "const CHANGELOG = ["
    $aIdx = $indexContent.IndexOf($anchor)
    if ($aIdx -lt 0) {
        Write-Error "CHANGELOG anchor not found in index.html"
        exit 1
    }
    $afterAnchor = $aIdx + $anchor.Length
    $nl = $indexContent.IndexOf("`n", $afterAnchor)
    if ($nl -lt 0) { $nl = $afterAnchor }
    $indexContent = $indexContent.Substring(0, $nl + 1) + $newEntry + "`r`n" + $indexContent.Substring($nl + 1)

    # ── Safety: in-memory integrity check BEFORE write ──
    if ($indexContent.Length -lt ($origLength * 0.9)) {
        Write-Error ("Aborted: new content shrunk to {0} (was {1}, <90%). File NOT written." -f $indexContent.Length, $origLength)
        exit 1
    }
    if (-not $indexContent.Contains("</html>")) {
        Write-Error "Aborted: new content missing </html>. File NOT written."
        exit 1
    }
    if (-not $indexContent.Contains("<BookQuest />")) {
        Write-Error "Aborted: new content missing <BookQuest /> mount. File NOT written."
        exit 1
    }

    Write-Utf8 $indexPath $indexContent

    # ── Safety: verify disk file matches what we intended ──
    $verify = Read-Utf8 $indexPath
    if ($verify.Length -lt ($indexContent.Length - 8)) {
        Write-Warning ("Disk write mismatch: disk={0} memory={1}. Restoring original." -f $verify.Length, $indexContent.Length)
        Write-Utf8 $indexPath $origIndexContent
        Write-Error "Aborted deploy due to index.html write corruption."
        exit 1
    }
    if (-not $verify.Contains("</html>")) {
        Write-Warning "Disk file missing </html>. Restoring original."
        Write-Utf8 $indexPath $origIndexContent
        Write-Error "Aborted deploy due to index.html write corruption."
        exit 1
    }

    # Reset NEXT_RELEASE.md (plain template, no backticks to avoid parse issues)
    $resetTemplate = $K_HEAD + "`r`n`r`n## " + $K_TITLE + "`r`n`r`n`r`n## " + $K_CHANGES + "`r`n`r`n"
    Write-Utf8 $stagingPath $resetTemplate

    Write-Host "  - release v$Version '$releaseTitle' ($($bulletLines.Count) items) injected" -ForegroundColor Cyan
    Write-Host "  - NEXT_RELEASE.md reset" -ForegroundColor Cyan
}

# Bump sw.js cache name
$swPath = Join-Path $repoRoot "sw.js"
if (-not (Test-Path $swPath)) {
    Write-Error "sw.js not found"
    exit 1
}

$ts = Get-Date -Format "yyyyMMddHHmmss"
$cacheName = "bookquest-v$ts"

$swContent = Read-Utf8 $swPath
$cachePattern = "bookquest-v[\w_]+"
$newSwContent = [System.Text.RegularExpressions.Regex]::Replace($swContent, $cachePattern, $cacheName)
Write-Utf8 $swPath $newSwContent

Write-Host "  - sw.js cache bumped to $cacheName" -ForegroundColor Cyan

# Stage / commit / push
git add -A
if ($Version) {
    $commitMsg = "$Message`n`n[release: v$Version] [cache: $cacheName]"
} else {
    $commitMsg = "$Message`n`n[cache: $cacheName]"
}
git commit -m $commitMsg

if ($LASTEXITCODE -ne 0) {
    Write-Warning "commit failed (exit $LASTEXITCODE)"
    exit $LASTEXITCODE
}

git push
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    if ($Version) {
        Write-Host "  OK released v$Version with cache $cacheName" -ForegroundColor Green
    } else {
        Write-Host "  OK deployed with cache $cacheName" -ForegroundColor Green
    }
    Write-Host "  GitHub Pages: 1-2 min" -ForegroundColor Green
    Write-Host "  Existing tabs auto-reload via SW listener" -ForegroundColor Green
} else {
    Write-Error "git push failed (exit $LASTEXITCODE)"
}
