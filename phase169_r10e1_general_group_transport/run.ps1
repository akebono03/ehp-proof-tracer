$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$backup = Join-Path $folder 'output\phase165_r52_r9_shared_math.py.before'
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E1 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E1 cannot inspect Git HEAD.' }
    Write-Host "R10E1_BRANCH=$branch"
    Write-Host "R10E1_GIT_HEAD=$head"
    $required = @(
        'phase169_r10d2_general_family_definition\family_citation.py',
        'phase169_r10b_registered_stable_family_binding\family_registry.py',
        'phase169_r7_general_stable_transport\rule.py',
        'data\HyoujiGen.csv'
    )
    foreach ($item in $required) {
        if (-not (Test-Path (Join-Path $root $item))) {
            throw "R10E1 missing prerequisite: $item"
        }
    }
    $beforeOther = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'R10E1 cannot inspect unrelated files.' }
    python -m phase169_r10e1_general_group_transport.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E1 guarded patch failed.' }
    $patched = $true
    python -m pytest -q `
        (Join-Path $folder 'tests\test_r10e1_general_transport.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport\tests\test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10b_registered_stable_family_binding\tests\test_r10b_registered_family.py') `
        (Join-Path $root 'phase169_r10d2_general_family_definition\tests\test_r10d2_general_family.py') `
        (Join-Path $root 'phase169_r10a2_unified_one_stem\tests\test_r10a2_one_stem_projection.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E1 limited pytest failed.' }
    python -m phase169_r10e1_general_group_transport.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E1 limited audit failed.' }
    $afterOther = @(git diff --name-only -- . ':!phase165_r52_r9_shared_math.py' | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'R10E1 detected unrelated tracked changes.'
    }
    $passed = $true
    Write-Host 'R10E1_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E1_PRODUCTION_FILES_CHANGED=phase165_r52_r9_shared_math.py'
    Write-Host 'R10E1_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed -and (Test-Path $backup)) {
        [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
        Write-Host 'R10E1_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
