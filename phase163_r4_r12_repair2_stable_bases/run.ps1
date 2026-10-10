$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r12_literature_registration.py',
  'tests\test_phase163_r4_r12_literature_registration.py',
  'toda_upstream_bootstrap.py',
  'tests\test_phase59_prop53_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r12_stable_bases.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r12_stable_bases.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r12_stable_bases.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r12_stable_bases.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r12_literature_registration.py tests/test_phase163_r4_r12_audit_import.py tests/test_phase163_r4_r12_stable_bases.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 repair2 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 repair2 audit failed.' }
Write-Host 'R4-R12 repair2 stable base registration completed. Full pytest not run.'
