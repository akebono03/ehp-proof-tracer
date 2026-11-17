param(
    [switch] $DryRun,
    [string] $R4R6Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_audit.py',
        'phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R7 focused pytest failed' }
    Write-Output 'PHASE175_R4R7_FOCUSED_PYTEST=PASS'

    $argsForAudit = @(
        '-B', '-m', 'phase175_r4r7_prop25_typed_composition.audit', '--root', $root
    )
    if ($DryRun) { $argsForAudit += '--dry-run' }
    if ($R4R6Report -ne '') { $argsForAudit += @('--r4r6-report', $R4R6Report) }
    & python @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R4R7 isolated typed/source audit failed' }
    Write-Output 'PHASE175_R4R7_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R7_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R7_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
