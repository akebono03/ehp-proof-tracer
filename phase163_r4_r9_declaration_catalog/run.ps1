$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r8_choice_registration.py',
  'phase163_r4_r9_declaration_catalog.py',
  'proof.py',
  'expression.py',
  'toda_rules.py',
  'phase162_reference_boundary.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Required file is missing from project root: $Filename"
  }
}
if (-not (Test-Path (Join-Path $ProjectRoot 'tests'))) {
  throw 'Project tests folder is missing.'
}
& python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py tests/test_phase163_r4_r9_declaration_catalog.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R8/R9 focused pytest failed; audit skipped.' }
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R9 audit failed.' }
Write-Host 'Phase 163 R4-R9 audit import path fixed. Full suite not run.'
