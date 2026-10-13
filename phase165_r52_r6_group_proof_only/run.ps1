$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'web_app.py'))) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R52-R6 layout installation failed' }
$tests = @(
  'test_phase165_r52_r6_group_proof_only.py',
  'test_phase165_r52_r5_auto_search.py',
  'test_phase165_r52_r4_flask_connection.py'
)
foreach ($item in $tests) {
  if (-not (Test-Path (Join-Path $root $item))) { throw "Missing targeted test: $item" }
}
$absolute = @($tests | ForEach-Object { Join-Path $root $_ })
python -m pytest -q @absolute
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
Write-Host 'R52-R6 group-proof-only layout verified; full pytest NOT run.'
