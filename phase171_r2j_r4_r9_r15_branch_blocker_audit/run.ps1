param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase171_r2j_r4_r9_r15_branch_blocker_audit'
Push-Location $RepoRoot
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R15 requires the develop branch.'
    }
    Write-Output "PHASE171_R15_BRANCH=$Branch"

    python -m "$Module.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15 preflight failed.' }
    if ($DryRun) {
        Write-Output 'PHASE171_R15_DRY_RUN=PASS'
        return
    }

    Write-Output 'PHASE171_R15_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$Module/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R15 focused pytest failed.' }
    Write-Output 'PHASE171_R15_FOCUSED_PYTEST=PASS'

    python -m "$Module.audit"
    if ($LASTEXITCODE -ne 0) { throw 'R15 audit failed.' }

    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed.' }
    git diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed.' }
    Write-Output 'PHASE171_R15_RESULT=PASS_READ_ONLY_BLOCKER_AUDIT'
}
finally {
    Pop-Location
}
