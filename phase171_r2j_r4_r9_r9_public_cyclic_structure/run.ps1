param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'EHP Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r9_public_cyclic_structure\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r8_public_cardinality\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R9_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 cyclic-structure audit failed' }
} finally {
    Pop-Location
}
