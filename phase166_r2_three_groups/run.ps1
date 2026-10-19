$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    python -m phase166_r2_three_groups.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2 three-group audit failed' }
    python -m pytest -q phase166_r2_three_groups/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2 focused pytest failed' }
    Write-Host 'R2 three-group correspondence audit PASS; full pytest NOT run.'
} finally { Pop-Location }
