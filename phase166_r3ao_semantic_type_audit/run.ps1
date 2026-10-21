$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m phase166_r3ao_semantic_type_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'Semantic type audit failed' }
    python -m pytest -q phase166_r3ao_semantic_type_audit/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'Read-only semantic audit complete; full pytest NOT run.'
} finally {
    Pop-Location
}
