$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$root = (Resolve-Path (Join-Path $scriptDir '..')).Path
$target = Join-Path $root 'phase168_r3_5_model_renderer.py'
$backup = Join-Path $scriptDir 'output\phase168_r3_5_model_renderer.py.before'
$success = $false
$patchDone = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R10A requires the develop branch.'
    }
    Write-Host "R10A_GIT_BRANCH=$branch"
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read HEAD' }
    Write-Host "R10A_GIT_HEAD=$head"
    $beforeOther = @(git diff --name-only -- . ':!phase168_r3_5_model_renderer.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read existing tracked changes.' }
    $beforeStatus = @(git status --porcelain -- phase168_r3_5_model_renderer.py)
    if ($LASTEXITCODE -ne 0 -or $beforeStatus.Count -gt 0) {
        throw 'Renderer has local modifications; refusing to patch.'
    }

    python -m phase169_r10a_verified_stable_chain_projection.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10A patch failed; production should be unchanged.' }
    $patchDone = $true

    python -m pytest -q `
        (Join-Path $scriptDir 'tests\test_r10a_verified_stable_chain.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r6a_pi86_two_step_transport\tests\test_r6a_two_step_transport.py') `
        (Join-Path $root 'phase169_r5b_pi75_prior_transport\tests\test_r5b_pi75_transport.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10A focused pytest failed.' }

    python -m phase169_r10a_verified_stable_chain_projection.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10A narrative/proof-tree audit failed.' }
    $afterOther = @(git diff --name-only -- . ':!phase168_r3_5_model_renderer.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read resulting tracked changes.' }
    if (($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'Unrelated tracked files changed.'
    }
    $changed = @(git diff --name-only -- phase168_r3_5_model_renderer.py)
    if ($LASTEXITCODE -ne 0 -or $changed.Count -ne 1) {
        throw 'Expected only the shared renderer to change.'
    }
    $success = $true
    Write-Host 'R10A_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10A_PRODUCTION_FILES_CHANGED=phase168_r3_5_model_renderer.py'
    Write-Host 'R10A_FULL_PYTEST_RUN=False'
} finally {
    if ($patchDone -and -not $success -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10A_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
