param(
    [switch]$DryRun,
    [switch]$SkipTests,
    [switch]$SkipAudit
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = Split-Path -Parent $PSScriptRoot
Push-Location $Repo
try {
    if ($DryRun) {
        & python -B -m phase171_r20r12_verified_cyclic_narrative.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R12 dry run failed' }
        return
    }
    & python -B -m phase171_r20r12_verified_cyclic_narrative.install
    if ($LASTEXITCODE -ne 0) { throw 'R20R12 patch failed' }
    if (-not $SkipTests) {
        & python -B -m pytest -p no:cacheprovider -q `
            phase171_r20r12_verified_cyclic_narrative/tests/test_install.py `
            phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py `
            phase171_r2j_r4_r8_cyclic_structure/tests `
            phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_r20r11_verified_prior.py
        if ($LASTEXITCODE -ne 0) { throw 'R20R12 focused pytest failed' }
    }
    if (-not $SkipAudit) {
        & python -B -m phase171_r20r12_verified_cyclic_narrative.audit
        if ($LASTEXITCODE -ne 0) { throw 'R20R12 canonical narrative audit failed' }
    }
    Write-Output 'PHASE171_R20R12_RUN=PASS'
}
finally {
    Pop-Location
}
