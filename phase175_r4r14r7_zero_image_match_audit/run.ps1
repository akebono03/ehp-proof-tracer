param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $arguments = @('-m', 'phase175_r4r14r7_zero_image_match_audit.audit', '--root', $root)
    if ($DryRun) { $arguments += '--dry-run' }
    python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R7 read-only audit failed' }
    if ($DryRun) { exit 0 }

    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r7_zero_image_match_audit/tests/test_audit.py `
        phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py `
        phase175_r4r14r5_public_zero_transport/tests/test_provider.py `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_public.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R7 focused tests failed' }
    Write-Output 'PHASE175_R4R14R7_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE175_R4R14R7_GATE=PASS_SOURCE_MATCH_AND_FOCUSED_TESTS'
} finally {
    Pop-Location
}
