param(
    [switch] $DryRun,
    [string] $R4R4Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        phase175_r4r5_eta7_annihilator_isolated/tests/test_rule.py `
        phase175_r4r5_eta7_annihilator_isolated/tests/test_audit.py `
        phase175_r4r4_pi95_premise_frontier/tests/test_audit.py `
        phase175_r4r3_two_summand_quotient/tests/test_rule.py `
        phase175_r4r3_two_summand_quotient/tests/test_audit.py `
        phase175_r4_pi95_audit/tests/test_audit.py

    if ($LASTEXITCODE -ne 0) { throw 'R4R5 focused pytest failed' }
    Write-Output 'PHASE175_R4R5_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE175_R4R5R2_FOCUSED_PYTEST=PASS'

    $cmd = @('-B', '-m', 'phase175_r4r5_eta7_annihilator_isolated.audit', '--root', $root)
    if ($DryRun) { $cmd += '--dry-run' }
    if ($R4R4Report -ne '') { $cmd += @('--r4r4-report', $R4R4Report) }
    & python @cmd
    $auditExitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R5_EXIT_CODE=$auditExitCode"
    Write-Output "PHASE175_R4R5R2_EXIT_CODE=$auditExitCode"
    if ($auditExitCode -ne 0) { exit $auditExitCode }
    exit 0
} finally {
    Pop-Location
}
