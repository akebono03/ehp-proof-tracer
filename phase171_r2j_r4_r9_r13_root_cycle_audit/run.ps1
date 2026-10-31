param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ModuleName = 'phase171_r2j_r4_r9_r13_root_cycle_audit'
Push-Location $RepoRoot
try {
    $GitBranch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $GitBranch -ne 'develop') {
        throw 'R13 requires Git develop. No source was modified.'
    }
    $GitHead = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not read Git HEAD.'
    }
    Write-Output "PHASE171_R13_BRANCH=$GitBranch"
    Write-Output "PHASE171_R13_HEAD=$GitHead"

    if ($DryRun) {
        python -m "$ModuleName.audit" --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw 'R13 preflight failed.'
        }
        Write-Output 'PHASE171_R13_DRY_RUN=PASS'
        return
    }

    python -m "$ModuleName.audit" --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 source baseline check failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R13_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$ModuleName/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 focused pytest failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R13_FOCUSED_PYTEST=PASS'

    python -m "$ModuleName.audit"
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 root diagnosis failed.'
    }
    git status -sb
    if ($LASTEXITCODE -ne 0) {
        throw 'Git status query failed.'
    }
    git diff --stat
    if ($LASTEXITCODE -ne 0) {
        throw 'Git diff query failed.'
    }
    Write-Output 'PHASE171_R13_RESULT=PASS_READ_ONLY_ROOT_AUDIT'
}
finally {
    Pop-Location
}
