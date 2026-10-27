$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$target = Join-Path $root 'phase168_r3_5_model_renderer.py'
$backup = Join-Path $folder 'output\phase168_r3_5_model_renderer.py.r10a-before'
$modified = $false
$passed = $false
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$previousPytestOpts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R10A2 requires the develop branch.'
    }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Could not determine local Git HEAD.' }
    Write-Host "R10A2_BRANCH=$branch"
    Write-Host "R10A2_GIT_HEAD=$head"
    $existing = [System.IO.File]::ReadAllBytes($target)
    $r10aFull = Join-Path $root 'phase169_r10a_verified_stable_chain_projection\output\phase168_r3_5_model_renderer.py.FULL'
    if (-not (Test-Path $r10aFull)) { throw 'R10A1 full Renderer output is missing.' }
    $oldHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($existing))
    $expectedHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.IO.File]::ReadAllBytes($r10aFull)))
    if ($oldHash -ne $expectedHash) {
        throw 'Current Renderer is not the reviewed and successful R10A1 version.'
    }
    $otherBefore = @(git diff --name-only -- . ':!phase168_r3_5_model_renderer.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'Could not read initial Git changes.' }
    python -m phase169_r10a2_unified_one_stem.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10A2 patch failed.' }
    $modified = $true

    python -m pytest -q `
      (Join-Path $folder 'tests\test_r10a2_one_stem_projection.py') `
      (Join-Path $root 'phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py') `
      (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10A2 focused pytest failed.' }

    python -m phase169_r10a2_unified_one_stem.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10A2 1-stem/Web audit failed.' }
    $otherAfter = @(git diff --name-only -- . ':!phase168_r3_5_model_renderer.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($otherAfter -join "`n") -ne ($otherBefore -join "`n")) {
        throw 'A tracked file outside the Renderer changed.'
    }
    $passed = $true
    Write-Host 'R10A2_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10A2_PRODUCTION_FILES_CHANGED=phase168_r3_5_model_renderer.py'
    Write-Host 'R10A2_FULL_PYTEST_RUN=False'
} finally {
    if ($modified -and -not $passed -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10A2_ROLLBACK_TO_R10A1=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTEST_ADDOPTS = $previousPytestOpts
    Pop-Location
}
