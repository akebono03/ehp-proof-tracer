$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($name in @('toda_stable_concrete_transport_proof.py', 'tests\test_phase162_r4_b2_concrete_transport.py')) {
    $source = Join-Path (Join-Path $package 'files') $name
    $destination = Join-Path $root $name
    Copy-Item -LiteralPath $source -Destination $destination -Force
    Write-Host "Updated: $name"
}
python -B -m pytest -q tests/test_phase162_r4_b2_concrete_transport.py tests/test_phase162_r4_b1_stable_path_selection.py tests/test_phase160_canonical_toda45_specialization.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 162 R4-B2 focused tests failed' }
Write-Host 'R4-B2 focused tests complete; existing roots and renderers unchanged; full suite not run.'
