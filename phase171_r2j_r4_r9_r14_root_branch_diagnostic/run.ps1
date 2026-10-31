param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase171_r2j_r4_r9_r14_root_branch_diagnostic'
Push-Location $RepoRoot
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'Phase 171 R14 requires develop.'
    }
    $Head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect HEAD.' }
    Write-Output "PHASE171_R14_BRANCH=$Branch"
    Write-Output "PHASE171_R14_HEAD=$Head"

    python -m "$Module.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R14 preflight failed.' }
    if ($DryRun) {
        Write-Output 'PHASE171_R14_DRY_RUN=PASS'
        return
    }

    Write-Output 'PHASE171_R14_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$Module/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R14 focused pytest failed.' }
    Write-Output 'PHASE171_R14_FOCUSED_PYTEST=PASS'

    python -m "$Module.audit"
    if ($LASTEXITCODE -ne 0) { throw 'R14 root exception audit failed.' }
    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed.' }
    git diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed.' }
    Write-Output 'PHASE171_R14_RESULT=PASS_READ_ONLY_ROOT_BRANCH_AUDIT'
}
finally {
    Pop-Location
}
