param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run R9-R2 at the Git repository root.' }
    python -B -m phase171_r2j_r4_r9_r2_scoped_search_bridge.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R2_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_live_scoped.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R2_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r2_scoped_search_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 scoped canonical search failed' }
} finally {
    Pop-Location
}
