$ErrorActionPreference = "Stop"
Push-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
try {
    python -m pytest -q phase168_r2_8_1_citation_mismatch_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    python -m phase168_r2_8_1_citation_mismatch_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
} finally {
    Pop-Location
}
