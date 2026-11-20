param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
$oldAddopts = $env:PYTEST_ADDOPTS
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTEST_ADDOPTS = "$oldAddopts -p no:cacheprovider".Trim()
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r10_right_zero_transport_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 focused pytest failed' }
        python -B -m phase176_r3r10_right_zero_transport_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $oldAddopts
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONIOENCODING = $oldEncoding
    Pop-Location
}
