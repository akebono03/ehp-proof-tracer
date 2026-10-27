$ErrorActionPreference = 'Stop'
$package = $PSScriptRoot
$root = (Resolve-Path (Join-Path $package '..')).Path
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    Write-Host 'R8: read-only 3-stem dependency audit'
    python -m phase169_r8_three_stem_transport_audit.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'R8 diagnostic failed. Inspect the output/audit.json and Python traceback.'
    }
    Write-Host 'R8_AUDIT_DONE=True'
    Write-Host 'R8_WHOLE_PYTEST_RUN=False'
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
