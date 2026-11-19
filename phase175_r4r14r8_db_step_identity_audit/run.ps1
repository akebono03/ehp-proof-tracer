param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $params = @('-m', 'phase175_r4r14r8_db_step_identity_audit.audit', '--root', $repo)
    if ($DryRun) { $params += '--dry-run' }
    python @params
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R8 read-only audit failed' }
    if ($DryRun) { exit 0 }
    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r8_db_step_identity_audit/tests/test_audit.py `
        phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py `
        phase175_r4r14r7_zero_image_match_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R8 focused pytest failed' }
    Write-Output 'PHASE175_R4R14R8_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE175_R4R14R8_GATE=PASS_DB_IDENTITY_DIAGNOSIS_AND_FOCUSED_TESTS'
} finally {
    Pop-Location
}
