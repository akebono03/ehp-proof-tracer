$ErrorActionPreference = "Stop"
$repo = (Get-Location).Path
$script = Join-Path $PSScriptRoot "cleanup_phase145_1.py"

Write-Host "=============================================================="
Write-Host "Phase 145-1 Repository Cleanup"
Write-Host "Step 1: dry-run and safety verification"
Write-Host "=============================================================="
python $script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
$answer = Read-Host "Apply the deletions shown above? Type YES to continue"
if ($answer -cne "YES") {
    Write-Host "Cancelled. No files were deleted."
    exit 0
}

Write-Host ""
Write-Host "Applying verified cleanup..."
python $script --apply
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Git status after cleanup:"
git status --short
Write-Host ""
Write-Host "Phase 145-1 cleanup finished."
Write-Host "No production code or tests were intentionally modified."
