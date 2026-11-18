param(
    [switch] $DryRun,
    [string] $R4R5R3Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $tests = @(
        'phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py',
        'phase175_r4r4_pi95_premise_frontier/tests/test_audit.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R6 focused pytest failed' }
    Write-Output 'PHASE175_R4R6_FOCUSED_PYTEST=PASS'

    $command = @('-B', '-m', 'phase175_r4r6_prop25_eq58_source_frontier.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R5R3Report -ne '') { $command += @('--r4r5r3-report', $R4R5R3Report) }
    & python @command
    if ($LASTEXITCODE -ne 0) { throw 'R4R6 source/type/boundary audit failed' }
    Write-Output 'PHASE175_R4R6_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R6_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R6_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
