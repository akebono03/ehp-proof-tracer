$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'web_group_proof.py',
  'phase164_r5_web_registry_connection.py',
  'phase164_r4_r8_registry_reconstruction.py',
  'phase164_r4_r6_typed_binding.py',
  'phase163_r4_r94_output\manifest.json'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) { throw "Missing prerequisite: $File" }
}
$Existing = Get-Content (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Raw
if ($Existing -notmatch 'def build_phase164_r5_web_pi5_3_proof') {
  throw 'R5 source changed unexpectedly; aborting'
}
$Backup = Join-Path $Project 'phase164_r5_web_registry_connection.phase164_r5_r1_backup.py'
if (-not (Test-Path $Backup)) { Copy-Item (Join-Path $Project 'phase164_r5_web_registry_connection.py') $Backup }
Copy-Item (Join-Path $PSScriptRoot 'phase164_r5_web_registry_connection.py') (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_r1_common_renderer.py') (Join-Path $Project 'tests\test_phase164_r5_r1_common_renderer.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_web_registry_connection.py') (Join-Path $Project 'tests\test_phase164_r5_web_registry_connection.py') -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R1 patch failed' }
python -B -m pytest -q `
  tests/test_phase164_r5_r1_common_renderer.py `
  tests/test_phase164_r5_web_registry_connection.py `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R1 focused tests failed' }
Write-Output 'Phase 164 R5-R1 common renderer path installed. Full pytest NOT run.'
