param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = Split-Path -Parent $PSScriptRoot
Push-Location $Repo
try {
    if ($DryRun) {
        & python -B -m phase171_r20r13r4_test_count_fix.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R20R13R4 test-only dry run failed' }
        Write-Output 'PHASE171_R20R13R4_DRY_RUN_WRAPPER=PASS'
        return
    }
    & python -B -m phase171_r20r13r4_test_count_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R4 guarded test patch failed' }
    & python -B -m pytest -p no:cacheprovider -q `
        phase171_r20r13r4_test_count_fix/tests
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R4 installer tests failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass `
        -File '.\phase171_r20r13r3_content_guard_fix\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R3 focused pytest or proof audit failed' }
    & python -B -m phase171_r20r13r4_test_count_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R20R13R4 audit failed' }
    Write-Output 'PHASE171_R20R13R4_RUN=PASS'
}
finally {
    Pop-Location
}
