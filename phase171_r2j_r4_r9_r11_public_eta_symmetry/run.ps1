param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r11_public_eta_symmetry\tests\test_audit.py' `
        '.\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R11_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 public equality audit failed' }
} finally {
    Pop-Location
}
