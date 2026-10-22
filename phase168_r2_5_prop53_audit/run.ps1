$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m pytest -q phase166_r3t_goal_source_binding/test_connection.py phase168_r2_4_nk_citation_binding/test_binding.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    python -m phase168_r2_5_prop53_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'Read-only audit failed' }
    Write-Host 'R2-5 read-only audit complete; full pytest NOT run.'
} finally {
    Pop-Location
}
