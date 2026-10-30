param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run R9-R3 at the Git repository root.' }
    python -B -m phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R3_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R3_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 Hopf frontier diagnostic failed' }
} finally {
    Pop-Location
}
