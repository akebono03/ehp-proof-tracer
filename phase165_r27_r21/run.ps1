$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$python = 'python'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { $python = 'py' }
& $python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python -m pytest -q "$PSScriptRoot\test_patch.py" "test_phase165_r52_r5_auto_search.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R21 targeted tests passed; full pytest NOT run.'
