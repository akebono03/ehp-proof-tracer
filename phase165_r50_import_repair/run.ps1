$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R50 import repair failed' }
python -m pytest -q `
  '.\phase165_r50_final_exactness_dedup\test_phase165_r50_final_exactness_dedup.py' `
  '.\phase165_r50_common_renderer_repair\test_phase165_r50_reference_contract.py' `
  '.\phase165_r50_consumer_link_preservation\test_phase165_r50_consumer_link_preservation.py' `
  '.\phase165_r50_reference_bridge\test_phase165_r50.py' `
  '.\tests\test_phase165_r49_display_fix.py'
if ($LASTEXITCODE -ne 0) { throw 'R49/R50 targeted tests failed' }
Write-Host 'R49/R50 targeted tests passed; full pytest NOT run.'
