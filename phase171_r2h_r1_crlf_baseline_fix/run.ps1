param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m phase171_r2h_r1_crlf_baseline_fix.repair check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2H_R1_RESULT=PASS_DRY_RUN'
        return
    }
    & python -B -m phase171_r2h_r1_crlf_baseline_fix.repair apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_REPAIR_FAILED' }
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider 'phase171_r2h_r1_crlf_baseline_fix/tests/test_repair.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2H_R1_FOCUSED_PYTEST=PASS'
    & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2h_prop22_cited_hopf\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_REPAIRED_PREFLIGHT_FAILED' }
    & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2h_prop22_cited_hopf\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_ORIGINAL_RUN_FAILED' }
    Write-Host 'PHASE171_R2H_R1_RESULT=PASS'
}
finally { Pop-Location }
