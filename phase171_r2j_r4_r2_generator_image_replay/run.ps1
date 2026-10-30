param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R2_RUN=PASS_DRY_RUN"
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider phase171_r2j_r4_r2_generator_image_replay/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R2_FOCUSED_PYTEST=PASS"
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 proof replay failed" }
    Write-Output "PHASE171_R2J_R4_R2_RESULT=PASS_AUDIT_ONLY"
}
finally {
    Pop-Location
}
