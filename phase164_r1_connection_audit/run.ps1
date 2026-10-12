$ErrorActionPreference = 'Stop'
$Project = (Get-Location).Path
if (-not (Test-Path (Join-Path $Project 'unified_statement_registry.py'))) {
  throw 'Run from ehp-proof-tracer repository root.'
}
$Audit = Join-Path $PSScriptRoot 'audit.py'
python -B $Audit
if ($LASTEXITCODE -ne 0) { throw 'Read-only audit failed.' }
$Tests = @(
  'tests/test_phase163_r2_unified_registry.py',
  'tests/test_phase163_r3_registry_validation.py',
  'tests/test_phase163_r4_registry_bridge.py',
  'tests/test_phase161_r5_backward_proof_reconstruction.py'
)
$Existing = @($Tests | Where-Object { Test-Path (Join-Path $Project $_) })
if ($Existing.Count -eq 0) { throw 'No relevant targeted tests found.' }
python -B -m pytest -q @Existing
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed.' }
Write-Host 'Phase 164 R1 finished. No production changes. Full pytest NOT run.'
