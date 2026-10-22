$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m pytest -q --import-mode=importlib .\phase168_r2_8_7_reference_binding\tests\test_r2_8_7_reference_binding.py
    if ($LASTEXITCODE -ne 0) { throw 'Prepatch focused pytest failed' }
    python -m phase168_r2_8_7_reference_binding.patch
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q --import-mode=importlib .\phase168_r2_8_6_reference_trace\tests\test_r2_8_6_reference_trace.py
    if ($LASTEXITCODE -ne 0) { throw 'Reference trace tests failed' }
    python -m phase168_r2_8_6_reference_trace.audit
    if ($LASTEXITCODE -ne 0) { throw 'Reference trace failed' }
} finally {
    Pop-Location
}
