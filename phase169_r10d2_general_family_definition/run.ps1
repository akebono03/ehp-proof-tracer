$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$referenceTarget = Join-Path $root 'phase168_r3_37c_reference_projection.py'
$backup = Join-Path $folder 'output\phase165_r52_r9_shared_math.py.before'
$referenceBackup = Join-Path $folder 'output\phase168_r3_37c_reference_projection.py.before'
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10D2 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10D2 cannot inspect Git HEAD.' }
    Write-Host "R10D2_BRANCH=$branch"
    Write-Host "R10D2_GIT_HEAD=$head"
    $required = @(
        'phase169_r10b_registered_stable_family_binding\family_registry.py',
        'phase169_r7_general_stable_transport\rule.py',
        'data\HyoujiGen.csv',
        'sources\toda\Toda_05_2.tex',
        'phase163_r4_r94_output\manifest.json'
    )
    foreach ($name in $required) {
        if (-not (Test-Path (Join-Path $root $name))) { throw "R10D2 missing prerequisite: $name" }
    }
    $beforeOther = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py' ':!phase168_r3_37c_reference_projection.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'R10D2 cannot inspect tracked changes.' }
    python -m phase169_r10d2_general_family_definition.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10D2 guarded patch failed; no tests run.' }
    $patched = $true
    python -m pytest -q `
        (Join-Path $folder 'tests\test_r10d2_general_family.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10b_registered_stable_family_binding\tests\test_r10b_registered_family.py') `
        (Join-Path $root 'phase169_r10a2_unified_one_stem\tests\test_r10a2_one_stem_projection.py') `
        (Join-Path $root 'phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10D2 focused pytest failed.' }
    python -m phase169_r10d2_general_family_definition.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10D2 limited audit failed.' }
    $afterOther = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py' ':!phase168_r3_37c_reference_projection.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'R10D2 found an unrelated tracked modification.'
    }
    $passed = $true
    Write-Host 'R10D2_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10D2_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py,phase168_r3_37c_reference_projection.py'
    Write-Host 'R10D2_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed -and (Test-Path $backup) -and (Test-Path $referenceBackup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        [System.IO.File]::WriteAllBytes($referenceTarget, [System.IO.File]::ReadAllBytes($referenceBackup))
        Write-Host 'R10D2_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
