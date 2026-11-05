param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PriorIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $BeforeIndex = @(git ls-files --stage) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git ls-files failed' }
    $BeforeStatus = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    & python -B -m phase174_r3_r5_preflight.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-R5 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider `
            phase174_r3_r5_preflight/tests/test_audit.py `
            phase174_r3_r3_injective_delta_zero/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 focused tests failed' }
        Write-Output 'PHASE174_R3R5_FOCUSED_PYTEST=PASS'
    }
    $AfterIndex = @(git ls-files --stage) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git ls-files failed after audit' }
    $AfterStatus = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git status failed after audit' }
    if ($BeforeIndex -cne $AfterIndex -or $BeforeStatus -cne $AfterStatus) {
        throw 'Audit changed Git index or worktree'
    }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R5_DRY_RUN=PASS'
    } else {
        Write-Output 'PHASE174_R3R5_READ_ONLY_GATE=PASS'
    }
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    $env:PYTHONIOENCODING = $PriorIO
    Pop-Location
}
