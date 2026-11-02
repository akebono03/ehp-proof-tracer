param(
    [switch]$DryRun,
    [switch]$SkipPi77Search
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Write-Output 'PHASE173_R4_R1_TYPED_PREMISE_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_typed_premise_probe\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 typed-premise focused tests failed' }
    Write-Output 'PHASE173_R4_R1_TYPED_PREMISE_FOCUSED_PYTEST=PASS'
    $Arguments = @('-m', 'phase173_r4_r1_typed_premise_probe.audit')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($SkipPi77Search) { $Arguments += '--skip-pi77-search' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 typed-premise audit failed' }
} finally {
    Pop-Location
}
