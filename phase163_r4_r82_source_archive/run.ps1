$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
$Preflight = Join-Path $Root 'phase163_r4_r80_output\registration_preflight.json'
$Duplicates = Join-Path $Root 'phase163_r4_r81_output\duplicate_audit.json'
foreach ($item in @($Preflight, $Duplicates)) { if (-not (Test-Path $item)) { throw "Missing prerequisite: $item" } }
$env:PYTHONPATH = "$Package;$Root"
python -m pytest -q (Join-Path $Package 'tests\test_phase163_r4_r82_source_archive.py')
if ($LASTEXITCODE -ne 0) { throw 'R82 focused pytest failed.' }
python (Join-Path $Package 'phase163_r4_r82_source_archive.py') --preflight $Preflight --duplicates $Duplicates --output (Join-Path $Root 'phase163_r4_r82_output')
if ($LASTEXITCODE -ne 0) { throw 'R82 archive build failed.' }
Write-Host 'R82 complete. Production application unchanged. Full pytest not run.'
