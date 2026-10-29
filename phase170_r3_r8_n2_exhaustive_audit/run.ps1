param(
    [switch]$DryRun,
    [int]$MinK = 0,
    [int]$MaxK = -1
)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Repo
$Env:PYTHONPATH = $Repo
$Parameters = @('-B', (Join-Path $PSScriptRoot 'audit.py'), '--root', $Repo, '--min-k', "$MinK")
if ($MaxK -ge 0) { $Parameters += @('--max-k', "$MaxK") }
if ($DryRun) { $Parameters += '--dry-run' }
& python @Parameters
exit $LASTEXITCODE
