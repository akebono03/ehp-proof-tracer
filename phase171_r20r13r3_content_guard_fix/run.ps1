param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = Split-Path -Parent $PSScriptRoot
Push-Location $Repo
try {
    if ($DryRun) {
        & python -B -m phase171_r20r13r2_multiple_blank_eta_merge.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R13R3 content-guard dry run failed' }
        Write-Output 'PHASE171_R20R13R3_DRY_RUN=PASS'
        return
    }
    & python -B -m pytest -p no:cacheprovider -q `
        phase171_r20r13r3_content_guard_fix/tests
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R3 focused guard pytest failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass `
        -File '.\phase171_r20r13r2_multiple_blank_eta_merge\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R2 corrected installer or audit failed' }
    & python -B -m phase171_r20r13r3_content_guard_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R3 final audit failed' }
    Write-Output 'PHASE171_R20R13R3_RUN=PASS'
}
finally {
    Pop-Location
}
