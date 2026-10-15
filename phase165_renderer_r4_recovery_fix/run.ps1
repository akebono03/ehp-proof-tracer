$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $project } else { "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'recover.py')
if ($LASTEXITCODE -ne 0) { throw 'R4 recovery failed; original backup is preserved. Do not rerun old R4 installer.' }
& $python -m pytest -q (Join-Path $project 'phase165_renderer_r3_model_connection\test_r3.py') (Join-Path $project 'test_phase165_r56_common_renderer.py')
if ($LASTEXITCODE -ne 0) { throw 'R3 targeted verification failed; original backup is preserved.' }
$baseline = Join-Path $project 'phase165_renderer_r4_legacy_retirement\baseline.json'
if (Test-Path $baseline) {
    & $python (Join-Path $project 'phase165_renderer_r4_legacy_retirement\snapshot.py') after $baseline
    if ($LASTEXITCODE -ne 0) { throw 'R3 narrative output differs from saved baseline. Backup preserved.' }
}
Write-Output 'R4 interruption recovery verified: back to R3. Do NOT rerun original R4 installer. Full pytest NOT run.'
