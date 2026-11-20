param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r13_two_boundary_audit.audit --dry-run
        exit $LASTEXITCODE
    }
    python -B -m phase176_r3r13_two_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r13_two_boundary_audit/tests/test_audit.py phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py phase175_r3r9_lemma57_explicit_public/tests/test_rule.py
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
