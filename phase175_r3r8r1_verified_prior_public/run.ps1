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
    Write-Output 'PHASE175_R3R8R1_DRYRUN_START'
    & python -B -m phase175_r3r8r1_verified_prior_public.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R8R1_EXIT_CODE=$code"
    exit $code
}

Write-Output 'PHASE175_R3R8R1_PUBLIC_INTEGRATION_START'
& python -B -m phase175_r3r8r1_verified_prior_public.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R8R1_EXIT_CODE=$code"
exit $code
