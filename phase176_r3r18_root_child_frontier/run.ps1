param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r18_root_child_frontier.audit --dry-run
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        python -B -m phase176_r3r18_root_child_frontier.audit
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python -B -m pytest -q -p no:cacheprovider --import-mode=importlib phase176_r3r18_root_child_frontier/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    exit 0
} finally { Pop-Location }
