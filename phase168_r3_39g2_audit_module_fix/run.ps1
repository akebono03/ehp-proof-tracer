$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$Files = @('phase168_r3_27_typed_statement_projection.py', 'phase168_r3_29_order_projection.py', 'phase168_r3_37c_reference_projection.py', 'phase168_r3_5_model_renderer.py')
$Backup = Join-Path $PSScriptRoot 'backup'
New-Item -ItemType Directory -Path $Backup -Force | Out-Null
foreach ($File in $Files) { Copy-Item -LiteralPath (Join-Path $Project $File) -Destination (Join-Path $Backup $File) -Force }
try {
    python (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase168_r3_39g_common_projection.py')
    if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
    python -m phase168_r3_39f_frozen_comparison.audit
    if ($LASTEXITCODE -ne 0) { throw 'Frozen comparison failed' }
    Write-Host 'R3-39G limited test and fulltext comparison complete. Full pytest NOT run.'
} catch {
    foreach ($File in $Files) { Copy-Item -LiteralPath (Join-Path $Backup $File) -Destination (Join-Path $Project $File) -Force }
    Write-Host 'ROLLBACK: restored all four original files.'
    throw
}
