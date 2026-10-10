$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'phase163_r4_registry_bridge.py',
  'unified_statement_registry.py',
  'phase163_r4_r11_literature_registration.py',
  'phase163_r4_r12_literature_registration.py',
  'phase163_r4_r12_stable_bases.py',
  'toda_literature_statement_boundary.py',
  'tests\test_phase59_prop53_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing prior phase file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r13_inventory.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r13_inventory.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r13_inventory.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r13_inventory.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r13_inventory.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R13 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R13 inventory audit failed.' }
Write-Host 'R4-R13 read-only inventory finished. Full pytest not run.'
