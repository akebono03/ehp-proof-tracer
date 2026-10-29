param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 180
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Arguments = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root, '--timeout-seconds', "$TimeoutSeconds")
if ($DryRun) { $Arguments += '--dry-run' }
& python @Arguments
exit $LASTEXITCODE
