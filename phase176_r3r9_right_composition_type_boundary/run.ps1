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
        python -B -m phase176_r3r9_right_composition_type_boundary.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r9_right_composition_type_boundary/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 focused pytest failed' }
        python -B -m phase176_r3r9_right_composition_type_boundary.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $oldAddopts
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONIOENCODING = $oldEncoding
    Pop-Location
}
