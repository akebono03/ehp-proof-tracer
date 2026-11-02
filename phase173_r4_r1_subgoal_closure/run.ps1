param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here '..')).Path
Push-Location $Root
try {
    Write-Output 'PHASE173_R4_R1_CLOSURE_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_subgoal_closure\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 closure focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_CLOSURE_FOCUSED_PYTEST=PASS'
    $Arguments = @('-m', 'phase173_r4_r1_subgoal_closure.audit', '--root', $Root)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 closure audit failed' }
}
finally {
    Pop-Location
}
