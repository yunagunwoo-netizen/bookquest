# ============================================================
# BookQuest Deploy Script
# ------------------------------------------------------------
# Usage:
#   .\deploy.ps1                       # prompt for message
#   .\deploy.ps1 "feat: new feature"   # one-shot
#
# Auto handled:
#   1. clean .git\index.lock and *.bak
#   2. bump CACHE_NAME in sw.js with new timestamp
#   3. git add -A -> commit -> push
#
# First-time setup (only once if blocked):
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# ============================================================

param(
    [Parameter(Position = 0)]
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path $PSScriptRoot

function Write-Step { param([string]$Text)
    Write-Host ""
    Write-Host "[*] $Text" -ForegroundColor Cyan
}
function Write-Ok { param([string]$Text)
    Write-Host "    OK  $Text" -ForegroundColor Green
}
function Write-Warn { param([string]$Text)
    Write-Host "    !!  $Text" -ForegroundColor Yellow
}
function Write-Err { param([string]$Text)
    Write-Host "    XX  $Text" -ForegroundColor Red
}

Write-Host ""
Write-Host "===== BookQuest Deploy =====" -ForegroundColor Magenta
Write-Host "  $($PSScriptRoot)" -ForegroundColor DarkGray

# ----- 1. clean leftovers -----------------------------------
Write-Step "Cleaning leftovers"

$lockPath = Join-Path $PSScriptRoot ".git\index.lock"
if (Test-Path $lockPath) {
    Remove-Item $lockPath -Force -ErrorAction SilentlyContinue
    Write-Ok "removed: .git\index.lock"
} else {
    Write-Ok "no lock (clean)"
}

$bakFiles = Get-ChildItem -Path $PSScriptRoot -Filter "*.bak" -File -ErrorAction SilentlyContinue
foreach ($bak in $bakFiles) {
    Remove-Item $bak.FullName -Force -ErrorAction SilentlyContinue
    Write-Ok "removed: $($bak.Name)"
}

# ----- 2. bump SW cache version -----------------------------
Write-Step "Bumping Service Worker cache version"

$swPath = Join-Path $PSScriptRoot "sw.js"
if (Test-Path $swPath) {
    $ts = Get-Date -Format 'yyyyMMddHHmmss'
    $newVer = "bookquest-v$ts"

    $bytes = [System.IO.File]::ReadAllBytes($swPath)
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $newText = [regex]::Replace($text, "bookquest-v\d+", $newVer)

    if ($newText -ne $text) {
        [System.IO.File]::WriteAllBytes($swPath, [System.Text.Encoding]::UTF8.GetBytes($newText))
        Write-Ok "$newVer"
    } else {
        Write-Warn "no bookquest-v pattern found in sw.js (skipped)"
    }
} else {
    Write-Warn "sw.js not found (skipped)"
}

# ----- 3. git status ----------------------------------------
Write-Step "Checking changes"

$status = git status --short 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Err "git status failed"
    Write-Host $status
    exit 1
}

if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Warn "no changes - exit"
    exit 0
}

Write-Host $status -ForegroundColor DarkGray

# ----- 4. commit message ------------------------------------
if ([string]::IsNullOrWhiteSpace($Message)) {
    Write-Host ""
    $Message = Read-Host "Commit message"
    if ([string]::IsNullOrWhiteSpace($Message)) {
        Write-Err "empty message - cancelled"
        exit 1
    }
}

# ----- 5. add -> commit -> push -----------------------------
Write-Step "git add -A"
git add -A
if ($LASTEXITCODE -ne 0) { Write-Err "git add failed"; exit 1 }
Write-Ok "done"

Write-Step "git commit"
git commit -m "$Message"
if ($LASTEXITCODE -ne 0) { Write-Err "git commit failed"; exit 1 }

Write-Step "git push origin main"
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Err "git push failed"; exit 1 }

Write-Host ""
Write-Host "===== Deploy complete =====" -ForegroundColor Green
Write-Host "  GitHub Pages will reflect in 1-2 min." -ForegroundColor DarkGray
Write-Host "  Hard refresh browser with Ctrl+Shift+R." -ForegroundColor DarkGray
Write-Host ""
