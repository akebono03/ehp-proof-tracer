param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'EHP Git root required' }
    python -B -m phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R6_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r6_source_bound_cited_hopf\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r4_source_bound_hopf\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R6_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 replay failed' }
} finally {
    Pop-Location
}
