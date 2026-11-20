param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r16_public_connection.installer --dry-run
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python -B -m phase176_r3r16_public_connection.audit --dry-run
        exit $LASTEXITCODE
    }
    python -B -m phase176_r3r16_public_connection.installer
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r16_public_connection/tests/test_r3r16_connection.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase175_r3r9_lemma57_explicit_public/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m phase176_r3r16_public_connection.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $fullCode = python -B -m phase176_r3r16_public_connection.emit_full_functions
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $fullCode | Set-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'MODIFIED_FUNCTIONS_FULL_JA.md')
    exit 0
} finally {
    Pop-Location
}
