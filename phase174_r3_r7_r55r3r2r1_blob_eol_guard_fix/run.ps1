param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R55R3R2R1_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 deletion and guarded replacement failed' }

    # Focused test only; full suite is reserved for the Phase 174 final gate.
    python -m pytest -q --import-mode=importlib `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_payload.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_static.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_typed.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_public.py `
        .\phase174_r3_r7_r55_common_exactness_intro\tests\test_http.py `
        .\phase174_r3_r7_r37_upper_delta_surjectivity_isolated\tests\test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 focused pytest failed' }

    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 public proof audit failed' }
    Write-Output 'PHASE174_R55R3R2R1_FOCUSED_TESTS=PASS'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
