$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$OldPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($OldPath) { "$Root$([IO.Path]::PathSeparator)$OldPath" } else { $Root }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r14_r42_common_narrative.py')
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally { $env:PYTHONPATH = $OldPath }
Write-Host 'R42 targeted pytest passed; full pytest NOT run. Restart Web server.'
