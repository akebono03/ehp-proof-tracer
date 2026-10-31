param(
    [switch]$DryRun,
    [switch]$SkipTests,
    [switch]$SkipAudit
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repository = Split-Path -Parent $PSScriptRoot
Push-Location $Repository
try {
    if ($DryRun) {
        & python -B -m phase171_r20r11_verified_prior_hopf_surjectivity.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R11 dry run failed' }
        return
    }
    & python -B -m phase171_r20r11_verified_prior_hopf_surjectivity.install
    if ($LASTEXITCODE -ne 0) { throw 'R20R11 patch failed' }
    if (-not $SkipTests) {
        & python -B -m pytest -p no:cacheprovider -q `
            phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_install.py `
            phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_r20r11_verified_prior.py `
            phase171_r2j_r2_cyclic_hopf_surjective/tests/test_cited_cyclic_hopf.py `
            phase171_r2j_r3_ehp_exactness/tests/test_r2j_r3_exactness.py `
            phase171_r2j_r4_r4_cited_hopf_surjectivity/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R20R11 focused pytest failed' }
    }
    if (-not $SkipAudit) {
        & python -B -m phase171_r20r11_verified_prior_hopf_surjectivity.audit
        if ($LASTEXITCODE -ne 0) { throw 'R20R11 public audit failed; see output\audit.json' }
    }
    Write-Output 'PHASE171_R20R11_RUN=PASS'
}
finally {
    Pop-Location
}
