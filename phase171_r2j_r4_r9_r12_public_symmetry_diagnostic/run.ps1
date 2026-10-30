param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ModuleName = 'phase171_r2j_r4_r9_r12_public_symmetry_diagnostic'
Push-Location $RepoRoot
try {
    $GitBranch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $GitBranch -ne 'develop') {
        throw 'R12 requires Git develop. No source was modified.'
    }
    $GitHead = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not read Git HEAD.'
    }
    Write-Output "PHASE171_R12_BRANCH=$GitBranch"
    Write-Output "PHASE171_R12_HEAD=$GitHead"

    if ($DryRun) {
        python -m "$ModuleName.audit" --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw 'R12 preflight failed; install nothing.'
        }
        Write-Output 'PHASE171_R12_DRY_RUN=PASS'
        return
    }

    python -m "$ModuleName.audit" --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 source baseline check failed; audit cancelled.'
    }

    Write-Output 'PHASE171_R12_FOCUSED_PYTEST_START'
    python -m pytest -q "$ModuleName/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 focused pytest failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R12_FOCUSED_PYTEST=PASS'

    python -m "$ModuleName.audit"
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 public-search diagnosis failed without modifying source.'
    }

    git status -sb
    if ($LASTEXITCODE -ne 0) {
        throw 'Git status query failed.'
    }
    git diff --stat
    if ($LASTEXITCODE -ne 0) {
        throw 'Git diff query failed.'
    }
    Write-Output 'PHASE171_R12_RESULT=PASS_READ_ONLY_AUDIT'
}
finally {
    Pop-Location
}
