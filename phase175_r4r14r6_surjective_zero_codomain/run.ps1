param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsList = @('-m', 'phase175_r4r14r6_surjective_zero_codomain.installer', '--root', $root)
    if ($DryRun) { $argsList += '--dry-run' }
    python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 source guard or install failed' }
    if ($DryRun) { exit 0 }

    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_rule.py `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_installer.py `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_public.py `
        phase175_r4r14r5_public_zero_transport/tests/test_provider.py `
        phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 focused tests failed' }
    Write-Output 'PHASE175_R4R14R6_FOCUSED_TESTS=PASS'

    python -m phase175_r4r14r6_surjective_zero_codomain.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 public search audit failed' }
    Write-Output 'PHASE175_R4R14R6_NEW_GIVEN=0'
    Write-Output 'PHASE175_R4R14R6_GATE=PASS_R4R14R6_GENERIC_ROOT_AND_SEARCH_AUDITED'
} finally {
    Pop-Location
}
