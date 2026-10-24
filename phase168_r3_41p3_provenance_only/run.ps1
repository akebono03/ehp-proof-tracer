$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$output = Join-Path $package "output"
New-Item -ItemType Directory -Path $output -Force | Out-Null
$python = (Get-Command python -ErrorAction Stop).Source
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONPATH = $project
Push-Location $project
try {
    Write-Host "R3-41P3: patch exactly two projection functions; back up originals."
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $python -B -m phase168_r3_41p3_provenance_only.apply 2>&1 |
        Tee-Object -FilePath (Join-Path $output "apply.log")
    $applyExit = $LASTEXITCODE
    $ErrorActionPreference = $oldPreference
    if ($applyExit -ne 0) {
        Write-Host "PATCH_FAILED $applyExit"; exit $applyExit
    }
    Write-Host "Running focused tests (full pytest deferred)."
    $paths = @(
      ".\phase168_r3_41p3_provenance_only\tests\test_r341p3_provenance_only.py",
      ".\phase168_r3_41p3_provenance_only\tests\test_patch_internals.py",
      ".\phase168_r3_41o_renderer_closure\tests\test_phase168_r3_41o_renderer_closure.py",
      ".\phase168_r3_41n1_import_scope_fix\tests\test_phase168_r3_41n_composed_proof_display.py",
      ".\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py",
      ".\phase168_r3_39a_reference_accuracy\tests\test_phase168_r3_39a_reference_accuracy.py",
      ".\phase168_r3_8_citation_origin\tests\test_phase168_r3_8_citation_origin.py"
    )
    $ErrorActionPreference = "Continue"
    & $python -B -m pytest -q -p no:cacheprovider @paths 2>&1 |
        Tee-Object -FilePath (Join-Path $output "pytest_focused.log")
    $pytestExit = $LASTEXITCODE
    $ErrorActionPreference = $oldPreference
    if ($pytestExit -ne 0) {
        Write-Warning "Focused tests failed: restoring two source files."
        & $python -B -m phase168_r3_41p3_provenance_only.restore
        exit $pytestExit
    }
    Write-Host "Checking 3 public proof/reference fulltexts against frozen R3-41P2 captures: PASS via pytest."
    Write-Host "R3-41P3_FOCUSED_PASS"
    Write-Host "FULL_PYTEST_NOT_RUN"
    Write-Host "Backups: $(Join-Path $output 'backups')"
    Write-Host "Full source files: $(Join-Path $output 'full_files')"
} finally {
    Pop-Location
}
