param([switch]$DryRun, [switch]$SkipTests, [switch]$SkipAudit)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = Split-Path -Parent $PSScriptRoot
Push-Location $Repo
try {
    if ($DryRun) {
        & python -B -m phase171_r20r13r2_multiple_blank_eta_merge.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R13R2 dry run failed' }
        return
    }
    & python -B -m phase171_r20r13r2_multiple_blank_eta_merge.install
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R2 patch failed' }
    if (-not $SkipTests) {
        & python -B -m pytest -p no:cacheprovider -q `
            phase171_r20r13r2_multiple_blank_eta_merge/tests `
            phase171_r20r13_eta_sentence_layout/tests `
            phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py
        if ($LASTEXITCODE -ne 0) { throw 'R20R13R2 focused pytest failed' }
    }
    if (-not $SkipAudit) {
        & python -B -m phase171_r20r13r2_multiple_blank_eta_merge.audit
        if ($LASTEXITCODE -ne 0) { throw 'R20R13R2 canonical audit failed' }
    }
    Write-Output 'PHASE171_R20R13R2_RUN=PASS'
}
finally {
    Pop-Location
}
