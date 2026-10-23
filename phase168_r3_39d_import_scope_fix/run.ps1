$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$Targets = @(
  'phase165_r57_r20_general_specialization.py',
  'phase165_r12_r15_toda51.py',
  'phase165_r52_r9_shared_math.py',
  'phase168_r3_37c_reference_projection.py'
)
foreach ($Target in $Targets) {
  $Backup = Join-Path (Join-Path $PSScriptRoot 'backup') $Target
  New-Item -ItemType Directory -Force -Path (Split-Path $Backup) | Out-Null
  Copy-Item -LiteralPath (Join-Path $Project $Target) -Destination $Backup -Force
}
try {
  python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'Patch failed.' }
  python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase168_r3_39d_existing_rule.py')
  if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed.' }
  Write-Host 'R3-39D import-scope fix complete. Full suite NOT run.'
} catch {
  foreach ($Target in $Targets) {
    Copy-Item -LiteralPath (Join-Path (Join-Path $PSScriptRoot 'backup') $Target) -Destination (Join-Path $Project $Target) -Force
  }
  Write-Host 'ROLLBACK: four production files restored.'
  throw
}
