param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run from the EHP Git repository root' }
    python -B -m phase171_r2j_r4_r9_r5_remaining_match_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R5_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r5_remaining_match_frontier\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r4_source_bound_hopf\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R5_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r5_remaining_match_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 remaining frontier replay failed' }
} finally {
    Pop-Location
}
