$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m pytest -q --import-mode=importlib .\phase168_r2_8_6_reference_trace\tests\test_r2_8_6_reference_trace.py
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
    python -m phase168_r2_8_6_reference_trace.audit
    if ($LASTEXITCODE -ne 0) { throw 'Reference trace failed' }
} finally {
    Pop-Location
}
