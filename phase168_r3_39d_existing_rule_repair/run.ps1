$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Patch failed; inspect any backup files.' }
python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase168_r3_39d_existing_rule.py')
if ($LASTEXITCODE -ne 0) {
  $Targets = @('phase165_r57_r20_general_specialization.py', 'phase165_r12_r15_toda51.py', 'phase165_r52_r9_shared_math.py', 'phase168_r3_37c_reference_projection.py')
  foreach ($Target in $Targets) {
    Copy-Item -LiteralPath (Join-Path (Join-Path $PSScriptRoot 'backup') $Target) -Destination (Join-Path $Project $Target) -Force
  }
  throw 'Focused tests failed. All four production files restored from backup.'
}
Write-Host 'R3-39D focused tests complete; full suite NOT run.'
