$ErrorActionPreference = "Stop"
Push-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
try {
    $OldTest = Join-Path $PSScriptRoot "tests\test_audit.py"
    if (Test-Path $OldTest) {
        Remove-Item -LiteralPath $OldTest -Force
        Write-Host "REMOVED obsolete R2-8(2) test basename: $OldTest"
    }
    python -m pytest -q --import-mode=importlib phase168_r2_8_2_structured_generator_audit/tests/test_phase168_r2_8_2_structured_comparison.py phase168_r2_8_1_citation_mismatch_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed" }
    python -m phase168_r2_8_2_structured_generator_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Audit failed" }
} finally {
    Pop-Location
}
