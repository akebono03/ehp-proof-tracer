$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $package 'files\toda_stable_eta_generator_normalization.py'
$destination = Join-Path $root 'toda_stable_eta_generator_normalization.py'
if (-not (Test-Path -LiteralPath $destination)) { throw 'Original R4-B2 generator normalization module not installed' }
$backup = Join-Path $root 'toda_stable_eta_generator_normalization.phase162_r4_b2_pre_repair1.bak'
if (-not (Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $destination -Destination $backup }
Copy-Item -LiteralPath $source -Destination $destination -Force
Write-Host 'Updated: toda_stable_eta_generator_normalization.py'
Write-Host "Backup: $backup"
python -B -m pytest -q tests/test_phase162_r4_b2_generator_normalization.py tests/test_phase162_r4_b2_concrete_transport.py tests/test_phase162_r4_b1_stable_path_selection.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B2 generator normalization repair1 focused tests failed' }
Write-Host 'R4-B2 generator normalization repair1 focused tests complete; full suite not run.'
