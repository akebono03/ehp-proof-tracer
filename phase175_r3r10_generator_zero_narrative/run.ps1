param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    & python -B -m phase175_r3r10_generator_zero_narrative.audit --root $root --dry-run --timeout-seconds $TimeoutSeconds
} else {
    & python -B -m phase175_r3r10_generator_zero_narrative.audit --root $root --timeout-seconds $TimeoutSeconds
}
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R10_EXIT_CODE=$code"
exit $code
