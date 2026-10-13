$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py') apply
if ($LASTEXITCODE -ne 0) { throw 'R49 integration failed' }
$testPaths = @(
  (Join-Path $PSScriptRoot 'test_phase165_r51_common_reason_integration.py'),
  '.\tests\test_phase165_r49_display_fix.py',
  '.\phase165_r50_reference_bridge\test_phase165_r50.py',
  '.\phase165_r50_common_renderer_repair\test_phase165_r50_reference_contract.py',
  '.\phase165_r50_consumer_link_preservation\test_phase165_r50_consumer_link_preservation.py',
  '.\phase165_r50_final_exactness_dedup\test_phase165_r50_final_exactness_dedup.py'
)
python -m pytest -q @testPaths
if ($LASTEXITCODE -ne 0) {
  python (Join-Path $PSScriptRoot 'apply.py') restore
  throw 'R49/R50 targeted tests failed; source restored'
}
python (Join-Path $PSScriptRoot 'apply.py') finalize
if ($LASTEXITCODE -ne 0) { throw 'R49 superseded helper could not be archived' }
Write-Host 'R49 integrated into common Reason Renderer; targeted tests passed; full pytest NOT run.'
