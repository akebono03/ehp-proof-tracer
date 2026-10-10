$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$OriginalPackage = Join-Path $ProjectRoot 'phase163_r4_r12_prop51_prop53'
$Required = @(
  'phase163_r4_r12_literature_registration.py',
  'phase163_r4_registry_bridge.py',
  'tests\test_phase59_prop53_integration.py',
  'tests\test_phase163_r4_r12_literature_registration.py',
  'phase163_r4_r12_prop51_prop53\audit.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'audit.py') -Destination (Join-Path $OriginalPackage 'audit.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r12_audit_import.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r12_audit_import.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r12_literature_registration.py tests/test_phase163_r4_r12_audit_import.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $OriginalPackage 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 typed literature registration audit failed.' }
Write-Host 'R4-R12 repair1 audit import resolved. Full suite not run.'
