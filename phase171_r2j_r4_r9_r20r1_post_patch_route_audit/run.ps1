param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun) {
        python -m phase171_r2j_r4_r9_r20r1_post_patch_route_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R1_DRY_RUN_FAILED' }
        Write-Output 'PHASE171_R20R1_DRY_RUN=PASS'
        return
    }
    Write-Output 'PHASE171_R20R1_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        .\phase171_r2j_r4_r9_r20r1_post_patch_route_audit\tests\test_classification.py `
        .\phase171_r2j_r4_r9_r20r1_post_patch_route_audit\tests\test_live.py
    if ($LASTEXITCODE -ne 0) { throw 'R20R1_FOCUSED_PYTEST_FAILED' }
    Write-Output 'PHASE171_R20R1_FOCUSED_PYTEST=PASS'
    python -m phase171_r2j_r4_r9_r20r1_post_patch_route_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R20R1_AUDIT_FAILED' }
    Write-Output 'PHASE171_R20R1_RESULT=PASS_READ_ONLY_ROUTE_DIAGNOSTIC'
}
finally { Pop-Location }
