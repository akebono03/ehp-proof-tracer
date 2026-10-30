param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r7_nonzero_nu_order.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R4_R7_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py `
        phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py `
        phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R4_R7_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r7_nonzero_nu_order.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 nonzero/order proof replay failed' }
    Write-Output 'PHASE171_R2J_R4_R7_RESULT=PASS_AUDIT_ONLY'
}
finally {
    Pop-Location
}
