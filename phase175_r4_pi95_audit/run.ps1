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

& python -B -m pytest -p no:cacheprovider -q `
    phase175_r4_pi95_audit/tests/test_audit.py `
    phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py
if ($LASTEXITCODE -ne 0) {
    Write-Output "PHASE175_R4_FOCUSED_PYTEST=FAIL"
    exit $LASTEXITCODE
}
Write-Output "PHASE175_R4_FOCUSED_PYTEST=PASS"

if ($DryRun) {
    & python -B -m phase175_r4_pi95_audit.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
} else {
    & python -B -m phase175_r4_pi95_audit.audit `
        --root $root --timeout-seconds $TimeoutSeconds
}
$code = $LASTEXITCODE
Write-Output "PHASE175_R4_EXIT_CODE=$code"
exit $code
