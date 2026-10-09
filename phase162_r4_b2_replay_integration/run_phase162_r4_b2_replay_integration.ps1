$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = (Get-Location).Path
$files = @('toda_stable_eta_proof_replay.py', 'tests\test_phase162_r4_b2_replay_integration.py')
foreach ($relative in $files) {
    $src = Join-Path (Join-Path $package 'files') $relative
    $dest = Join-Path $project $relative
    $destDir = Split-Path -Parent $dest
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    if (Test-Path $dest) { Copy-Item $dest "$dest.phase162_r4_b2_pre_replay.bak" -Force }
    Copy-Item $src $dest -Force
    Write-Host "Updated: $relative"
}
python -B -m pytest -q tests/test_phase162_r4_b2_replay_integration.py tests/test_phase162_r4_b2_generator_normalization.py tests/test_phase162_r4_b2_concrete_transport.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B2 replay integration focused tests failed' }
Write-Host 'R4-B2 focused tests complete; repository roots, public renderer and full suite unchanged.'
