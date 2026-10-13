$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R50 adapter installation failed' }
python -m pytest -q `
  (Join-Path $PSScriptRoot 'test_phase165_r50_reference_contract.py') `
  '.\phase165_r50_reference_bridge\test_phase165_r50.py' `
  '.\tests\test_phase165_r49_display_fix.py' `
  '.\phase165_r50_consumer_link_preservation\test_phase165_r50_consumer_link_preservation.py'
if ($LASTEXITCODE -ne 0) { throw 'R49/R50 targeted tests failed; do not clean up' }
$archive = Join-Path $PSScriptRoot 'superseded_packages'
New-Item -Path $archive -ItemType Directory -Force | Out-Null
foreach ($folder in @('phase165_r50_reason_preservation_repair', 'phase165_r50_delta_reason_repair')) {
  if (Test-Path $folder) {
    $dest = Join-Path $archive $folder
    if (-not (Test-Path $dest)) { Move-Item -LiteralPath $folder -Destination $dest }
  }
}
Write-Host 'R50 targeted tests passed; two superseded installer folders archived; full pytest NOT run.'
