param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r6_middle_cardinality.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R4_R6_RESULT=PASS_DRY_RUN'
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py `
        phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R4_R6_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r6_middle_cardinality.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 cardinality proof replay failed' }
    Write-Output 'PHASE171_R2J_R4_R6_RESULT=PASS_AUDIT_ONLY'
}
finally {
    Pop-Location
}
