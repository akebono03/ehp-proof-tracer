param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $reviewedHead = 'ecbb2fea225c5b88000629d9c025934fcc2d7075'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R3-R6-R3R1 requires develop.'
    }
    git fetch origin
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify remote develop.' }
    $head = (git rev-parse HEAD).Trim()
    $remote = (git rev-parse origin/develop).Trim()
    if ($head -ne $reviewedHead -or $remote -ne $reviewedHead) {
        throw "Unreviewed HEAD: local=$head remote=$remote expected=$reviewedHead"
    }
    $originalPatch = Join-Path $repo 'phase174_r3_r6_r3_common_narrative/patch.py'
    $originalProjection = Join-Path $repo 'phase174_r3_r6_r3_common_narrative/projection.py'
    if (-not (Test-Path $originalPatch) -or -not (Test-Path $originalProjection)) {
        throw 'The original R3-R6-R3 package must remain installed.'
    }
    if ((Get-FileHash $originalPatch -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6b79153c208724c179ae6c57fea2fb79507875d3c22f09dc822f25272a1fe01b') {
        throw 'The original R3-R6-R3 patch.py has unreviewed changes.'
    }
    if ((Get-FileHash $originalProjection -Algorithm SHA256).Hash.ToLowerInvariant() -ne '28f629b1b163ecd55402f0e4d3a71b1d0640b029c59c8a739b5800e3741af995') {
        throw 'The original R3-R6-R3 projection.py has unreviewed changes.'
    }
    $staged = @(git diff --cached --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect git index.' }
    foreach ($path in @('phase168_r3_27_typed_statement_projection.py', 'phase168_r3_5_model_renderer.py')) {
        if ($staged -contains $path) {
            throw "Staged changes must be reviewed before R3R1: $path"
        }
    }
    Write-Output "PHASE174_R3R6R3R1_BRANCH=$branch"
    Write-Output "PHASE174_R3R6R3R1_LOCAL_HEAD=$head"
    Write-Output "PHASE174_R3R6R3R1_REMOTE_HEAD=$remote"
    if ($DryRun) {
        python -m phase174_r3_r6_r3r1_scoped_guard_fix.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3R1 DryRun failed; no production files changed.' }
    } else {
        python -m phase174_r3_r6_r3r1_scoped_guard_fix.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3R1 Apply failed.' }
        Write-Output 'PHASE174_R3R6R3R1_FOCUSED_PYTEST_START'
        python -m pytest -q `
            phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py `
            phase174_r3_r6_r3_common_narrative/tests/test_projection.py `
            phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
            phase174_r3_r6_source_extension/tests/test_source.py `
            phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
            phase172_r5_prior_reference_display/tests/test_projection.py
        if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed; Gate not certified.' }
        Write-Output 'PHASE174_R3R6R3R1_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE174_R3R6R3R1_GATE=PASS'
    }
} finally {
    Pop-Location
}
