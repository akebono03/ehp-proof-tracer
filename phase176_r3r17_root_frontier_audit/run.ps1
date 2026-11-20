param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r17_root_frontier_audit.audit --dry-run
        exit $LASTEXITCODE
    }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r17_root_frontier_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m phase176_r3r17_root_frontier_audit.audit
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
