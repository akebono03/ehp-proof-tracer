$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 3: Delete 28 audited A_SAFE_DELETE artifacts"
Write-Host "Step 1: dry-run and safety verification"
Write-Host "=============================================================="

python ".\phase145_1_stage3_delete_safe_artifacts\cleanup_phase145_1_stage3.py"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
$answer = Read-Host "Apply deletion of exactly these 28 artifacts? Type YES to continue"
if ($answer -cne "YES") {
    Write-Host "Cancelled. No Phase artifacts were deleted."
    exit 0
}

Write-Host ""
Write-Host "Applying Stage 3 cleanup..."
python ".\phase145_1_stage3_delete_safe_artifacts\cleanup_phase145_1_stage3.py" --apply
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Git status after Stage 3 cleanup:"
git status --short

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 3 cleanup finished."
Write-Host "No production code, canonical tests, formal docs, B_REVIEW, or C_SAVE"
Write-Host "artifacts were intentionally modified."
Write-Host "=============================================================="
