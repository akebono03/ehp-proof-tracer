param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'Phase 174 R3-R6-R3 requires the develop branch.'
    }

    git fetch origin
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to verify GitHub origin/develop.'
    }
    $remote = (git rev-parse origin/develop).Trim()
    $head = (git rev-parse HEAD).Trim()
    $old = 'e4a5b73962bb98acb62b5335ffecae4728d98378'
    $reviewed = 'ecbb2fea225c5b88000629d9c025934fcc2d7075'
    if ($remote -ne $reviewed) {
        throw "origin/develop has moved: $remote; re-audit before installing."
    }
    if ($head -ne $old -and $head -ne $reviewed) {
        throw "Unreviewed local HEAD $head; re-audit before installing."
    }
    $stagedPaths = @(git diff --cached --name-only)
    $protected = @(
        'phase168_r3_27_typed_statement_projection.py',
        'phase168_r3_5_model_renderer.py'
    )
    foreach ($target in $protected) {
        if ($stagedPaths -contains $target) {
            throw "Staged local work on $target must be reviewed first."
        }
    }

    Write-Output "PHASE174_R3R6R3_BRANCH=$branch"
    Write-Output "PHASE174_R3R6R3_LOCAL_HEAD=$head"
    Write-Output "PHASE174_R3R6R3_REMOTE_HEAD=$remote"
    if ($DryRun) {
        python -m phase174_r3_r6_r3_common_narrative.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3 DryRun failed.' }
    } else {
        python -m phase174_r3_r6_r3_common_narrative.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3 patch failed.' }
        Write-Output 'PHASE174_R3R6R3_FOCUSED_PYTEST_START'
        python -m pytest -q `
            phase174_r3_r6_r3_common_narrative/tests/test_projection.py `
            phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
            phase174_r3_r6_source_extension/tests/test_source.py `
            phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
            phase172_r5_prior_reference_display/tests/test_projection.py
        if ($LASTEXITCODE -ne 0) {
            throw 'R3-R6-R3 focused tests failed; changes are NOT certified.'
        }
        Write-Output 'PHASE174_R3R6R3_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE174_R3R6R3_GATE=PASS'
    }
} finally {
    Pop-Location
}
