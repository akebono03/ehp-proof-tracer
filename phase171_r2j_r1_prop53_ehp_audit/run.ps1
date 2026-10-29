param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase171_r2j_r1_prop53_ehp_audit'
Push-Location $Root
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R2J-R1 requires existing develop branch; no checkout/reset is performed'
    }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git rev-parse failed' }
    foreach ($Needed in @(
        'phase171_r2i_eta_hopf_bridge\audit.py',
        'phase171_r2i_eta_hopf_bridge\source.py',
        'phase171_r2h_prop22_cited_hopf\source.py',
        'phase165_r52_r9_shared_math.py',
        'sources\toda\Toda_05_2.tex'
    )) {
        if (-not (Test-Path (Join-Path $Root $Needed) -PathType Leaf)) {
            throw ('missing expected file: ' + $Needed)
        }
    }
    $Shared = [System.IO.File]::ReadAllText((Join-Path $Root 'phase165_r52_r9_shared_math.py'))
    if (-not $Shared.Contains('expand_cited_eta_hopf_power')) {
        throw 'R2I provider hook not installed; do not overwrite the existing math file'
    }
    Write-Output ('PHASE171_R2J_R1_BRANCH=' + $Branch)
    Write-Output ('PHASE171_R2J_R1_HEAD=' + $Head)
    Write-Output 'PHASE171_R2J_R1_R2I_PRESERVED=PASS'
    Write-Output 'PHASE171_R2J_R1_PREFLIGHT=PASS'
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R1_RESULT=PASS_DRY_RUN'
        exit 0
    }
    $Before = ((& git status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0) { throw 'git status before audit failed' }
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & python -B -m pytest -q -p no:cacheprovider `
        (Join-Path $Module 'tests\test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R1 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R1_FOCUSED_PYTEST=PASS'
    & python -B -m phase171_r2j_r1_prop53_ehp_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R1 live audit failed' }
    $After = ((& git status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0 -or $After -ne $Before) {
        throw 'tracked changes detected; audit must be read-only'
    }
    Write-Output 'PHASE171_R2J_R1_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Output 'PHASE171_R2J_R1_RUN=PASS'
}
finally {
    Pop-Location
}
