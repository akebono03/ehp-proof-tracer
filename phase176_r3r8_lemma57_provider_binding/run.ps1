param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
$previousAddopts = $env:PYTEST_ADDOPTS
$previousBytes = $env:PYTHONDONTWRITEBYTECODE
$previousEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTEST_ADDOPTS = "$previousAddopts -p no:cacheprovider".Trim()
    if ($DryRun) {
        python -B -m phase176_r3r8_lemma57_provider_binding.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r8_lemma57_provider_binding/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 focused pytest failed' }
        python -B -m phase176_r3r8_lemma57_provider_binding.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $previousAddopts
    $env:PYTHONDONTWRITEBYTECODE = $previousBytes
    $env:PYTHONIOENCODING = $previousEncoding
    Pop-Location
}
