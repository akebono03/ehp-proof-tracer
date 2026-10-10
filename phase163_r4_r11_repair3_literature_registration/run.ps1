$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'homotopy_groups.py',
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r10_generator_integrity.py',
  'phase163_r4_r11_prop56_remaining.py',
  'probes\probe_phase65_capabilities.py',
  'tests\test_phase65_prop56_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_literature_registration.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_literature_registration.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_literature_registration.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_literature_registration.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_literature_registration.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair3 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair3 literature registration audit failed.' }
Write-Host 'R4-R11 repair3 typed literature registration complete. Full suite not run.'
