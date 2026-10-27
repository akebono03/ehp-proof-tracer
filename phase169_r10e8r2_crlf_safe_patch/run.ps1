$ErrorActionPreference = 'Stop'
$wrapper = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $wrapper
$original = Join-Path $root 'phase169_r10e8_hyoujigen_generic_suspension'
$reviewedHead = '940d1d1cc2e9943e9d2955c7204a4392984d65e9'
$changedPaths = @(
    'phase169_r10d2_general_family_definition/family_citation.py',
    'phase165_r52_r9_shared_math.py'
)
$reviewedBlobs = @{
    'phase169_r10d2_general_family_definition/family_citation.py' = '4a33870892e139ac52d7b26503584b4d9624e0ba'
    'phase165_r52_r9_shared_math.py' = 'e010e52fb06a20eb6c60557022ffb024036ed5c0'
    'phase169_r10e8_hyoujigen_generic_suspension/patch.py' = 'c652e4afbe1669e798c8ee9ab0ab9b02b246eb50'
    'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' = '85d0bcfd122a4b3ae3b2ae04d0949f7c5773f39e'
    'phase169_r10e8_hyoujigen_generic_suspension/source_records.py' = 'bb54cc49092c6b16c4b83b113b325e028a42f50c'
    'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
    'data/HyoujiGen.csv' = '26f33db0c83ba7f151433583fe861598399cbe6a'
    'sources/toda/Toda_06_2.tex' = '76934583cff01c8ea83f768e26947eb9b556653b'
    'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' = '3b1255e9942d95dae06d104df38ac750c201e452'
}
$allowedNewPrefixes = @(
    'phase169_r10e8r1_head_guard_refresh/',
    'phase169_r10e8r2_crlf_safe_patch/'
)
$backups = @{}
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    if (-not (Test-Path (Join-Path $original 'patch.py'))) {
        throw 'R10E8R2 requires the original R10E8 package, bundled in this archive'
    }
    $branch = (& git branch --show-current).Trim()
    $head = (& git rev-parse HEAD).Trim()
    Write-Output "R10E8R2_BRANCH=$branch"
    Write-Output "R10E8R2_HEAD=$head"
    Write-Output "R10E8R2_REVIEWED_HEAD=$reviewedHead"
    if ($branch -ne 'develop') { throw 'R10E8R2 requires develop branch' }
    & git merge-base --is-ancestor $reviewedHead HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10E8R2 refused: HEAD does not descend from the reviewed GitHub commit'
    }
    $changesSinceReview = @(& git diff --name-only $reviewedHead HEAD)
    foreach ($path in $changesSinceReview) {
        $safe = $false
        foreach ($prefix in $allowedNewPrefixes) {
            if ($path.StartsWith($prefix, [System.StringComparison]::Ordinal)) { $safe = $true }
        }
        if (-not $safe) {
            throw "R10E8R2 refused: unreviewed HEAD changes $path"
        }
    }
    foreach ($path in $reviewedBlobs.Keys) {
        $sha = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $sha -ne $reviewedBlobs[$path]) {
            throw "R10E8R2 refused: reviewed Git blob does not match $path"
        }
    }
    foreach ($path in $changedPaths) {
        & git diff --quiet HEAD -- $path
        if ($LASTEXITCODE -ne 0) {
            throw "R10E8R2 refused: tracked local modifications in $path"
        }
        $absolute = Join-Path $root ($path -replace '/', [IO.Path]::DirectorySeparatorChar)
        $backups[$absolute] = [IO.File]::ReadAllBytes($absolute)
    }
    Write-Output 'R10E8R2_GITHUB_REVIEWED_BLOBS=PASS'
    Write-Output 'R10E8R2_MODE=SOURCE_NEWLINE_COMPATIBILITY_ONLY'
    & python -B -m phase169_r10e8r2_crlf_safe_patch.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R2 guarded CRLF patch failed' }
    & python -B -m pytest -q -p no:cacheprovider `
      'phase169_r10e8r2_crlf_safe_patch/tests/test_r10e8r2_newlines.py' `
      'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' `
      'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' `
      'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
      'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R2 limited pytest failed' }
    & python -B -m phase169_r10e8_hyoujigen_generic_suspension.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R2 focused proof search audit failed' }
    $modified = @(& git diff --name-only)
    foreach ($path in $changedPaths) {
        if ($path -notin $modified) { throw "R10E8R2 expected patch absent: $path" }
    }
    $unexpected = @($modified | Where-Object { $_ -notin $changedPaths })
    if ($unexpected.Count -gt 0) {
        Write-Output ('R10E8R2_OTHER_EXISTING_TRACKED_DIFF=' + ($unexpected -join ','))
    }
    Write-Output ('R10E8R2_PRODUCTION_FILES_CHANGED=' + ($changedPaths -join ','))
    Write-Output 'R10E8R2_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Output 'R10E8R2_INTEGRITY=PASS'
    Write-Output 'R10E8R2_FULL_PYTEST_RUN=False'
}
catch {
    if ($backups.Count -eq 2) {
        foreach ($path in $backups.Keys) {
            [IO.File]::WriteAllBytes($path, $backups[$path])
        }
        Write-Output 'R10E8R2_ROLLBACK=original working bytes restored'
    }
    Write-Output ('R10E8R2_FAILURE=' + $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
