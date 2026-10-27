$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$target = Join-Path $root 'phase169_r7_general_stable_transport\rule.py'
$backup = Join-Path $folder 'output\phase169_r7_general_stable_transport.rule.py.before'
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10B requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect HEAD.' }
    Write-Host "R10B_BRANCH=$branch"
    Write-Host "R10B_GIT_HEAD=$head"
    $beforeOther = @(git diff --name-only -- . ':!phase169_r7_general_stable_transport/rule.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect existing tracked changes.' }
    python -m phase169_r10b_registered_stable_family_binding.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10B source patch failed.' }
    $patched = $true
    python -m pytest -q `
      (Join-Path $folder 'tests\test_r10b_registered_family.py') `
      (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py') `
      (Join-Path $root 'phase169_r10a2_unified_one_stem\tests\test_r10a2_one_stem_projection.py') `
      (Join-Path $root 'phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10B focused pytest failed.' }
    python -m phase169_r10b_registered_stable_family_binding.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10B proof audit failed.' }
    $afterOther = @(git diff --name-only -- . ':!phase169_r7_general_stable_transport/rule.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'An unrelated tracked file changed.'
    }
    $passed = $true
    Write-Host 'R10B_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10B_PRODUCTION_FILES_CHANGED=phase169_r7_general_stable_transport/rule.py'
    Write-Host 'R10B_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10B_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
