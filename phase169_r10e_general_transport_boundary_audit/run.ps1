$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldPytest = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E0 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E0 cannot read HEAD.' }
    Write-Host "R10E0_BRANCH=$branch"
    Write-Host "R10E0_GIT_HEAD=$head"
    $required = @(
        'phase169_r10d2_general_family_definition\family_citation.py',
        'phase169_r10b_registered_stable_family_binding\family_registry.py',
        'phase169_r7_general_stable_transport\rule.py',
        'phase165_r52_r9_shared_math.py',
        'phase168_r3_37c_reference_projection.py',
        'data\sphere.csv',
        'data\HyoujiGen.csv'
    )
    foreach ($path in $required) {
        if (-not (Test-Path (Join-Path $root $path))) {
            throw "R10E0 missing prerequisite: $path"
        }
    }
    $production = @(
        'phase165_r52_r9_shared_math.py',
        'phase168_r3_37c_reference_projection.py',
        'phase169_r7_general_stable_transport\rule.py'
    )
    $before = @()
    foreach ($path in $production) {
        $before += (Get-FileHash -Algorithm SHA256 (Join-Path $root $path)).Hash
    }
    python -m pytest -q (Join-Path $folder 'tests\test_r10e_boundary.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E0 focused tests failed.' }
    python -m phase169_r10e_general_transport_boundary_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E0 audit failed.' }
    $after = @()
    foreach ($path in $production) {
        $after += (Get-FileHash -Algorithm SHA256 (Join-Path $root $path)).Hash
    }
    if (($before -join ',') -ne ($after -join ',')) {
        throw 'R10E0 detected an unexpected production change.'
    }
    Write-Host 'R10E0_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E0_FULL_PYTEST_RUN=False'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldPytest
    Pop-Location
}
