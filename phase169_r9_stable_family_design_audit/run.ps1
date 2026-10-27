$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$priorBytecode = $env:PYTHONDONTWRITEBYTECODE
$priorPytest = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    Write-Host 'Phase 169 R9: HyoujiGen stable-family AUDIT_ONLY'
    python -m phase169_r9_stable_family_design_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9 audit failed.' }
    python -m pytest -q '.\phase169_r9_stable_family_design_audit\tests\test_r9_family_boundaries.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9 targeted pytest failed.' }
    Write-Host 'R9_COMPLETE=AUDIT_ONLY'
    Write-Host 'R9_WHOLE_PYTEST_RUN=False'
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $priorBytecode
    $env:PYTEST_ADDOPTS = $priorPytest
    Pop-Location
}
