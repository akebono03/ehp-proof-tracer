$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $root 'phase164_r5_web_registry_connection.py'
$backup = Join-Path $root 'phase164_r5_web_registry_connection.phase165_r1_before_cutover.bak'
if (-not (Test-Path $target)) { throw "Required production file missing: $target" }
if (-not (Test-Path $backup)) { Copy-Item $target $backup }
Copy-Item (Join-Path $package 'phase164_r5_web_registry_connection.py') $target -Force
Copy-Item (Join-Path $package 'phase165_goal_only_search.py') (Join-Path $root 'phase165_goal_only_search.py') -Force
Copy-Item (Join-Path $package 'tests/test_phase165_goal_only_cutover.py') (Join-Path $root 'tests/test_phase165_goal_only_cutover.py') -Force
python -m py_compile $target (Join-Path $root 'phase165_goal_only_search.py')
if ($LASTEXITCODE -ne 0) { throw 'Syntax preflight failed' }
python -m pytest -q tests/test_phase165_goal_only_cutover.py
if ($LASTEXITCODE -ne 0) { throw 'Focused cutover tests failed' }
Write-Host 'Goal-only boundary installed; unimplemented proof search FAILS CLOSED.'
Write-Host 'Legacy pi5_3 web construction is disabled, not yet replaced with a working solver.'
Write-Host 'Full pytest was NOT run.'
