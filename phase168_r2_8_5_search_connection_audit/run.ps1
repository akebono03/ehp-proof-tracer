$ErrorActionPreference = "Stop"
Push-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
try {
    python -m pytest -q --import-mode=importlib `
        phase168_r2_8_5_search_connection_audit/tests/test_phase168_r2_8_5_search_connection.py `
        phase168_r2_8_1_citation_mismatch_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
    python -m phase168_r2_8_5_search_connection_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
} finally {
    Pop-Location
}
