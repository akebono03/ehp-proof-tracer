param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -m phase171_r2j_r4_r1_extension_frontier_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R1 DryRun failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R1_RUN=PASS_DRY_RUN"
        exit 0
    }
    python -m pytest -q -p no:cacheprovider phase171_r2j_r4_r1_extension_frontier_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R1 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R1_FOCUSED_PYTEST=PASS"
    python -m phase171_r2j_r4_r1_extension_frontier_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R1 audit failed" }
    Write-Output "PHASE171_R2J_R4_R1_RUN=PASS"
}
finally {
    Pop-Location
}
