param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r9_r1_public_path_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R9-R1 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R4_R9_R1_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r9_r1_public_path_audit/tests/test_audit.py `
        phase171_r2j_r4_r8_cyclic_structure/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R4-R9-R1 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R4_R9_R1_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r1_public_path_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4-R9-R1 public-path audit failed' }
    Write-Output 'PHASE171_R2J_R4_R9_R1_RESULT=PASS_AUDIT_ONLY'
}
finally {
    Pop-Location
}
