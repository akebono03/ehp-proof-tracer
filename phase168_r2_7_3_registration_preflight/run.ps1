$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $project
try {
    python -m pytest -q phase168_r2_7_3_registration_preflight/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Limited pytest failed' }
    python -m phase168_r2_7_3_registration_preflight.audit
    if ($LASTEXITCODE -ne 0) { throw 'Read-only audit failed' }
} finally { Pop-Location }
