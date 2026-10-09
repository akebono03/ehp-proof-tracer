$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($name in @('toda_stable_eta_generator_normalization.py', 'tests\test_phase162_r4_b2_generator_normalization.py')) {
    $source = Join-Path (Join-Path $package 'files') $name
    $destination = Join-Path $root $name
    Copy-Item -LiteralPath $source -Destination $destination -Force
    Write-Host "Updated: $name"
}
python -B -m pytest -q tests/test_phase162_r4_b2_generator_normalization.py tests/test_phase162_r4_b2_concrete_transport.py tests/test_phase162_r4_b1_stable_path_selection.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B2 generator normalization focused tests failed' }
Write-Host 'R4-B2 generator normalization focused tests complete; public renderer unchanged; full suite not run.'
