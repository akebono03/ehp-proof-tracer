param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    Write-Output 'PHASE173_R4_R1_SOURCE_BOUND_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_source_bound_56\tests'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 source-bound focused tests failed' }
    Write-Output 'PHASE173_R4_R1_SOURCE_BOUND_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        python -m phase173_r4_r1_source_bound_56.audit --root $Root --dry-run
    } else {
        python -m phase173_r4_r1_source_bound_56.audit --root $Root
    }
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 source-bound run failed' }
} finally {
    Pop-Location
}
