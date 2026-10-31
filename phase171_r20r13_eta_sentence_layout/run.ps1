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
        & python -B -m phase171_r20r13_eta_sentence_layout.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R13 dry run failed' }
        return
    }
    & python -B -m phase171_r20r13_eta_sentence_layout.install
    if ($LASTEXITCODE -ne 0) { throw 'R20R13 patch failed' }
    if (-not $SkipTests) {
        & python -B -m pytest -p no:cacheprovider -q `
            phase171_r20r13_eta_sentence_layout/tests `
            phase171_r20r12_verified_cyclic_narrative/tests `
            phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_r20r11_verified_prior.py
        if ($LASTEXITCODE -ne 0) { throw 'R20R13 focused pytest failed' }
    }
    if (-not $SkipAudit) {
        & python -B -m phase171_r20r13_eta_sentence_layout.audit
        if ($LASTEXITCODE -ne 0) { throw 'R20R13 canonical narrative audit failed' }
    }
    Write-Output 'PHASE171_R20R13_RUN=PASS'
}
finally {
    Pop-Location
}
