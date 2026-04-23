param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
)

# BookQuest deploy script
# Usage: .\deploy_bookquest.ps1 "commit message"
# Steps:
#   1) Remove stale .git\index.lock if any
#   2) Replace bookquest-v<ts> in sw.js with current timestamp
#   3) git add -A / commit / push

$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

# 1. Lock cleanup
$lock = Join-Path $repoRoot ".git\index.lock"
if (Test-Path $lock) {
    Remove-Item $lock -Force
    Write-Host "  - stale .git\index.lock removed" -ForegroundColor DarkGray
}

# 2. Line ending policy
git config core.autocrlf true | Out-Null

# 3. Bump sw.js cache name
$swPath = Join-Path $repoRoot "sw.js"
if (-not (Test-Path $swPath)) {
    Write-Error "sw.js not found at $swPath"
    exit 1
}

$ts = Get-Date -Format "yyyyMMddHHmmss"
$cacheName = "bookquest-v$ts"

$swContent = Get-Content $swPath -Raw
$pattern = "bookquest-v[\w_]+"
$newContent = [System.Text.RegularExpressions.Regex]::Replace($swContent, $pattern, $cacheName)

# Save as UTF-8 (no BOM) to keep sw.js valid JS
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($swPath, $newContent, $utf8NoBom)

Write-Host "  - sw.js cache bumped to $cacheName" -ForegroundColor Cyan

# 4. Stage / commit / push
git add -A
$commitMsg = "$Message`n`n[cache: $cacheName]"
git commit -m $commitMsg

if ($LASTEXITCODE -ne 0) {
    Write-Warning "commit failed (exit $LASTEXITCODE) - nothing to commit?"
    exit $LASTEXITCODE
}

git push
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "  OK deployed with cache $cacheName" -ForegroundColor Green
    Write-Host "  GitHub Pages: visible in 1-2 min" -ForegroundColor Green
    Write-Host "  Existing tabs will auto-reload via SW listener in index.html" -ForegroundColor Green
} else {
    Write-Error "git push failed (exit $LASTEXITCODE)"
}
