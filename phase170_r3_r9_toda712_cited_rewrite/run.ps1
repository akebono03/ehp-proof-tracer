param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Env:PYTHONPATH = $Root
$ArgsList = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root)
if ($DryRun) { $ArgsList += '--dry-run' }
& python @ArgsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
