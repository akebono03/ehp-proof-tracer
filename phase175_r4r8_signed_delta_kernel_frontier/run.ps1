param(
    [switch] $DryRun,
    [string] $R4R7Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $tests = @(
        'phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_audit.py',
        'phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R8 focused pytest failed' }
    Write-Output 'PHASE175_R4R8_FOCUSED_PYTEST=PASS'

    $command = @('-B', '-m', 'phase175_r4r8_signed_delta_kernel_frontier.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R7Report -ne '') { $command += @('--r4r7-report', $R4R7Report) }
    & python @command
    $exitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R8_EXIT_CODE=$exitCode"
    if ($exitCode -ne 0) { exit $exitCode }
    exit 0
} finally {
    Pop-Location
}
