param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r19_cyclic_structure_frontier.audit --dry-run
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        python -B -m phase176_r3r19_cyclic_structure_frontier.audit
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python -B -m pytest -q -p no:cacheprovider --import-mode=importlib phase176_r3r19_cyclic_structure_frontier/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
} finally {
    Pop-Location
}
