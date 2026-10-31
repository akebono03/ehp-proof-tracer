param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun) {
        python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20_DRY_RUN_FAILED' }
        Write-Output 'PHASE171_R20_DRY_RUN=PASS'
        return
    }
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20_PREFLIGHT_FAILED' }
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.install
    if ($LASTEXITCODE -ne 0) { throw 'R20_INSTALL_FAILED' }
    Write-Output 'PHASE171_R20_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        .\phase171_r2j_r4_r9_r20_eta_route_precedence\tests\test_r20.py `
        .\phase171_r2j_r4_r9_r8_public_cardinality\tests\test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R20_FOCUSED_PYTEST_FAILED' }
    Write-Output 'PHASE171_R20_FOCUSED_PYTEST=PASS'
    python -m phase171_r2j_r4_r9_r20_eta_route_precedence.audit
    if ($LASTEXITCODE -ne 0) { throw 'R20_AUDIT_FAILED' }
    Write-Output 'PHASE171_R20_RESULT=PASS'
}
finally { Pop-Location }
