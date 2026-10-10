$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'expression.py',
  'homotopy_groups.py',
  'toda_literature_statement_boundary.py',
  'phase162_reference_boundary.py',
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
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_prop56_remaining.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_prop56_remaining.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_prop56_remaining.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_prop56_remaining.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 actual registry audit failed.' }
Write-Host 'Phase 163 R4-R11 focused tests and representative audit finished. Full suite not run.'
