$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r7_representative_bindings.py',
  'phase163_r4_r11_prop56_remaining.py',
  'tests\test_phase65_prop56_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing project prerequisite: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_shared_origin.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_shared_origin.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_shared_origin.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_shared_origin.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_shared_origin.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair2 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair2 read-only audit failed.' }
Write-Host 'R4-R11 repair2 read-only shared ancestry audit finished. Full pytest not run.'
