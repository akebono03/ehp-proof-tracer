param([switch] $DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $Root
$env:PYTHONDONTWRITEBYTECODE = '1'
$arguments = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root)
if ($DryRun) { $arguments += '--dry-run' }
& python @arguments
exit $LASTEXITCODE
