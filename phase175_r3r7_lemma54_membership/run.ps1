param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

$tests = @(
    'phase175_r3r7_lemma54_membership/tests',
    'phase175_r3r6_lemma57_general/tests/test_rule.py',
    'phase175_r3r6_lemma57_general/tests/test_source.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/test_frontier.py',
    'phase173_r4_r1_lemma54_source_bridge/tests/test_source.py'
)

Write-Output 'PHASE175_R3R7_FOCUSED_PYTEST_START'
& python -B -m pytest -q -p no:cacheprovider @tests
if ($LASTEXITCODE -ne 0) {
    Write-Error 'R3R7 focused pytest failed'
    exit 2
}
Write-Output 'PHASE175_R3R7_FOCUSED_PYTEST=PASS'

$argsList = @(
    '-B', '-m', 'phase175_r3r7_lemma54_membership.audit',
    '--root', $root, '--timeout-seconds', [string]$TimeoutSeconds
)
if ($DryRun) {
    $argsList += '--dry-run'
}
& python @argsList
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R7_EXIT_CODE=$code"
exit $code
