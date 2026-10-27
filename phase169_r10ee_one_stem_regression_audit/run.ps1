$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    $branch = (& git branch --show-current).Trim()
    $head = (& git rev-parse HEAD).Trim()
    Write-Host "R10EE_BRANCH=$branch"
    Write-Host "R10EE_HEAD=$head"
    if ($branch -ne 'develop') {
        throw 'R10EE requires local develop; no checkout will be performed'
    }
    & git merge-base --is-ancestor '0cb9b8a88823ccd94a4a8967997bb302d98668eb' HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10EE requires reviewed Phase 169 R10EC-R1 commit ancestry'
    }
    $expected = [ordered]@{
        'phase165_r55_nk_only_goal.py' = 'b207b8169590e634229d412324d857ffb3857939'
        'phase165_r52_r9_shared_math.py' = 'd015e11030a15a62fbe75099bda10ddacdfdcbc5'
        'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
        'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
        'phase169_r10e4_ordered_db_prior/db_prior.py' = 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b'
    }
    foreach ($path in $expected.Keys) {
        $blob = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $expected[$path]) {
            throw "Reviewed Git blob mismatch: $path"
        }
    }
    Write-Host 'R10EE_REVIEWED_GITHUB_DEPENDENCIES=PASS'
    Write-Host 'R10EE_SCOPE=AUDIT_ONLY'
    $before = @(& git status --porcelain --untracked-files=no)
    & python -B -m pytest -q `
        '.\phase169_r10ee_one_stem_regression_audit\tests\test_r10ee_reporting.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EE focused pytest failed' }
    & python -B -m phase169_r10ee_one_stem_regression_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10EE audit did not run to completion' }
    $after = @(& git status --porcelain --untracked-files=no)
    if (($before -join "`n") -ne ($after -join "`n")) {
        throw 'R10EE changed tracked file status unexpectedly'
    }
    Write-Host 'R10EE_TRACKED_FILES_UNCHANGED=PASS'
    Write-Host 'R10EE_AUDIT_EXECUTION=PASS'
    Write-Host 'R10EE_FULL_PYTEST_RUN=False'
}
finally {
    Pop-Location
}
