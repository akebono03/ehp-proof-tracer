$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Production = Join-Path $Root 'phase165_r52_r7_registered_common_proof.py'
$TestDestination = Join-Path $Root 'phase165_r52_r7_registered_common_proof\test_phase165_r52_r7_registered_common_proof.py'
$TestSource = Join-Path $PSScriptRoot 'test_phase165_r52_r7_registered_common_proof.py'
if (!(Test-Path $Production)) { throw 'Production module missing' }
if (!(Test-Path $TestDestination)) { throw 'Existing test file missing' }
$Code = Get-Content -Path $Production -Raw -Encoding UTF8
if ($Code -match 'class RegisteredProofProvider|def registered_proof_providers\(') {
  throw 'Retirement is not installed; do not overwrite tests'
}
Copy-Item $TestDestination ($TestDestination + '.r6_1_pre_test_fix.bak') -Force
Copy-Item $TestSource $TestDestination -Force
python -m pytest -q $TestDestination
if ($LASTEXITCODE -ne 0) { throw 'Focused regression tests failed' }
Write-Host 'R6-1 focused tests passed. Full pytest NOT run.'
