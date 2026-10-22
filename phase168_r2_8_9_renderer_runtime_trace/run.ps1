$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q --import-mode=importlib .\phase168_r2_8_9_renderer_runtime_trace\tests\test_r2_8_9_renderer_runtime_trace.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m phase168_r2_8_9_renderer_runtime_trace.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
