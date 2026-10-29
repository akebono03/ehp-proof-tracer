param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Env:PYTHONPATH = $Root
$ArgList = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root)
if ($DryRun) { $ArgList += '--dry-run' }
& python @ArgList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
