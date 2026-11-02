param([switch]$DryRun)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Report = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery\phase173_r4_r1_committed_cache_resume\audit.json'
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Write-Output 'PHASE173_R4_R1_READOUT_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_frontier_readout\tests\test_readout.py'
    if ($LASTEXITCODE -ne 0) { throw 'Readout focused tests failed' }
    Write-Output 'PHASE173_R4_R1_READOUT_FOCUSED_PYTEST=PASS'
    if (-not (Test-Path -LiteralPath $Report -PathType Leaf)) {
        throw "Existing R4-R1 report not found: $Report"
    }
    if ($DryRun) {
        & python -m phase173_r4_r1_frontier_readout.readout --report $Report --dry-run
    } else {
        & python -m phase173_r4_r1_frontier_readout.readout --report $Report
    }
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 readout failed' }
} finally {
    Pop-Location
}
