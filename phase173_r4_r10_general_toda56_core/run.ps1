param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $Root
try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'Python is not available on PATH'
    }
    $Args = @('-B', '-m', 'phase173_r4_r10_general_toda56_core.verify', '--root', $Root)
    if ($DryRun) {
        $Args += '--dry-run'
    }
    & python @Args
    if ($LASTEXITCODE -ne 0) {
        throw 'R4-R10 source-pinned core verification failed'
    }
    if (-not $DryRun) {
        Write-Output 'PHASE173_R4_R10_FOCUSED_PYTEST_START'
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            'phase173_r4_r10_general_toda56_core/tests/test_core.py' `
            'phase173_r4_r7_source_first_rule/tests/test_rule.py' `
            'phase173_r4_r8_public_connection/tests/test_route.py' `
            'phase173_r4_r1_narrative_source_fix/tests/test_live.py'
        if ($LASTEXITCODE -ne 0) {
            throw 'R4-R10 focused pytest failed'
        }
        Write-Output 'PHASE173_R4_R10_FOCUSED_PYTEST=PASS'
    }
    Write-Output 'PHASE173_R4_R10_RESULT=PASS'
}
finally {
    Pop-Location
}
