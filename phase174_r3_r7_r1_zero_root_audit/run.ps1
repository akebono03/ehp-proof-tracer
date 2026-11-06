param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $RepoRoot
$env:PYTHONDONTWRITEBYTECODE = '1'

$FocusedTests = @(
    'phase174_r3_r7_r1_zero_root_audit/tests/test_audit.py',
    'phase174_r3_r7_source_first_audit/tests/test_audit.py',
    'phase173_r4_r11_zero_public_connection/tests/test_route.py',
    'phase173_r4_r10_general_toda56_core/tests/test_core.py',
    'phase166_r3ai_zero_goal_support/tests/test_zero_goals.py'
)

Write-Output 'PHASE174_R3R7R1_FOCUSED_PYTEST_START'
& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @FocusedTests
if ($LASTEXITCODE -ne 0) {
    throw 'Phase 174 R3-R7-R1 focused pytest failed'
}
Write-Output 'PHASE174_R3R7R1_FOCUSED_PYTEST=PASS'

if ($DryRun) {
    & python -B -m phase174_r3_r7_r1_zero_root_audit.audit --dry-run
} else {
    & python -B -m phase174_r3_r7_r1_zero_root_audit.audit
}
if ($LASTEXITCODE -ne 0) {
    throw 'Phase 174 R3-R7-R1 read-only audit failed'
}
Write-Output '(END)'
