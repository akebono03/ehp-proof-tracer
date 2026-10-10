$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'expression.py',
  'homotopy_groups.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r6_structured_binding.py',
  'phase163_r4_r7_representative_bindings.py',
  'unified_statement_registry.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r10_generator_integrity.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r10_generator_integrity.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r10_generator_integrity.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r10_generator_integrity.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r10_generator_integrity.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 actual generator audit failed.' }
Write-Host 'Phase 163 R4-R10 focused checks finished. Full suite not run.'
