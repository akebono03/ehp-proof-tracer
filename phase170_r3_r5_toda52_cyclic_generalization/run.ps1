param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root
Write-Host 'PHASE170_R3R5_MODE=GUARDED_SINGLE_FILE_PATCH'
if ($DryRun) {
    & python -B (Join-Path $PSScriptRoot 'runner.py') --root $Root --dry-run
} else {
    & python -B (Join-Path $PSScriptRoot 'runner.py') --root $Root
}
$ExitCode = $LASTEXITCODE
Write-Host "PHASE170_R3R5_EXIT=$ExitCode"
exit $ExitCode
