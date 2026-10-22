$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    python '.\phase168_r2_8_4_generic_specialization\apply.py'
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q --import-mode=importlib '.\phase168_r2_8_4_generic_specialization\tests\test_r2_8_4_generic_specialization.py' '.\phase168_r2_8_3_generator_identity\tests\test_r2_8_3_generator_identity.py' '.\phase168_r2_8_1_citation_mismatch_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
    python -m phase168_r2_8_1_citation_mismatch_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'Citation audit failed' }
} finally {
    Pop-Location
}
