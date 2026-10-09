$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$source = Join-Path $PSScriptRoot 'phase162_pi5_3_backward_selection.py'
$target = Join-Path $repo 'phase162_pi5_3_backward_selection.py'
if (-not (Test-Path (Join-Path $repo 'phase161_r5_backward_proof_reconstruction.py'))) {
    throw 'Run from the EHP Proof Tracer repository root.'
}
if (Test-Path $target) {
    $backup = "$target.before_phase162_backward_selection.bak"
    if (-not (Test-Path $backup)) { Copy-Item $target $backup }
    Write-Host "Backup: $backup"
}
Copy-Item $source $target -Force
Write-Host "Updated: $target"
python -B -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_pi5_3_backward_selection.py')
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
Write-Host 'Focused backward selection repair 2 tests passed. Full suite not run.'
