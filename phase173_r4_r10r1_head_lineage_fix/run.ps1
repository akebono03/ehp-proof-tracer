param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Root
try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'Python is not available on PATH'
    }
    if ($DryRun) {
        & python -B -m phase173_r4_r10r1_head_lineage_fix.apply --root $Root --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10R1 guarded DryRun failed'
        }
    }
    else {
        Write-Output 'PHASE173_R4_R10R1_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r10r1_head_lineage_fix/tests/test_apply.py'
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10R1 focused patch tests failed'
        }
        & python -B -m phase173_r4_r10r1_head_lineage_fix.apply --root $Root
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10R1 guarded patch failed'
        }
        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase173_r4_r10_general_toda56_core\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10 revised DryRun failed'
        }
        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase173_r4_r10_general_toda56_core\run.ps1'
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10 focused core verification failed'
        }
    }
    Write-Output 'PHASE173_R4_R10R1_RESULT=PASS'
}
finally {
    Pop-Location
}
