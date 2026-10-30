param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 guarded integration failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r10_public_short_exact\tests\test_audit.py' `
        '.\phase171_r2j_r4_r5_short_exact_sequence\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R10_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 public short-exact audit failed' }
} finally {
    Pop-Location
}
