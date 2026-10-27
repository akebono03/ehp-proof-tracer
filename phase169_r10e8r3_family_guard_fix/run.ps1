$ErrorActionPreference = 'Stop'
$wrapper = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $wrapper
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
    'phase169_r10e8r2_crlf_safe_patch/',
    'phase169_r10e8r3_family_guard_fix/'
)
$outputFolder = Join-Path $root 'phase169_r10e8_hyoujigen_generic_suspension/output'
$outputNames = @(
    'phase169_r10d2_general_family_definition__family_citation.py.FULL',
    'phase165_r52_r9_shared_math.py.FULL',
    'family_citation_IMPORTS_FULL.py',
    'canonical_member_FULL.py',
    'cited_family_reference_sentence_FULL.py',
    'build_shared_typed_bridge_FULL.py',
    'audit.json'
)
$backups = @{}
$outputBackups = @{}
$outputSnapshotted = $false
$success = $false
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    $branch = (& git branch --show-current).Trim()
    $head = (& git rev-parse HEAD).Trim()
    Write-Output "R10E8R3_BRANCH=$branch"
    Write-Output "R10E8R3_HEAD=$head"
    Write-Output "R10E8R3_REVIEWED_GITHUB_BASE=$reviewedHead"
    if ($branch -ne 'develop') { throw 'R10E8R3 requires develop branch' }
    & git merge-base --is-ancestor $reviewedHead HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10E8R3 refused: HEAD does not descend from reviewed commit'
    }
    $changesSinceReview = @(& git diff --name-only $reviewedHead HEAD)
    foreach ($path in $changesSinceReview) {
        $safe = $false
        foreach ($prefix in $allowedNewPrefixes) {
            if ($path.StartsWith($prefix, [System.StringComparison]::Ordinal)) {
                $safe = $true
            }
        }
        if (-not $safe) { throw "R10E8R3 refused: unreviewed HEAD change $path" }
    }
    foreach ($path in $reviewedBlobs.Keys) {
        $sha = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $sha -ne $reviewedBlobs[$path]) {
            throw "R10E8R3 refused: reviewed Git blob mismatch $path"
        }
    }
    $dependencies = @(
        'phase169_r10e8_hyoujigen_generic_suspension/patch.py',
        'phase169_r10e8r2_crlf_safe_patch/newline_support.py'
    )
    foreach ($path in $dependencies) {
        if (-not (Test-Path (Join-Path $root $path))) {
            throw "R10E8R3 missing required earlier package $path"
        }
    }
    foreach ($path in $changedPaths) {
        & git diff --quiet HEAD -- $path
        if ($LASTEXITCODE -ne 0) {
            throw "R10E8R3 refused: pre-existing tracked modifications in $path"
        }
        $absolute = Join-Path $root ($path -replace '/', [IO.Path]::DirectorySeparatorChar)
        $backups[$absolute] = [IO.File]::ReadAllBytes($absolute)
    }
    foreach ($name in $outputNames) {
        $absolute = Join-Path $outputFolder $name
        if (Test-Path $absolute) {
            $outputBackups[$absolute] = [IO.File]::ReadAllBytes($absolute)
        } else {
            $outputBackups[$absolute] = $null
        }
    }
    $outputSnapshotted = $true
    Write-Output 'R10E8R3_GITHUB_REVIEWED_BLOBS=PASS'
    Write-Output 'R10E8R3_SCOPE=EXACT_TWO_FUNCTION_GUARD_FIX_ONLY'
    & python -B -m phase169_r10e8r3_family_guard_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R3 corrected guarded patch failed' }
    & python -B -m pytest -q -p no:cacheprovider `
      'phase169_r10e8r3_family_guard_fix/tests/test_r10e8r3_family_guard.py' `
      'phase169_r10e8r2_crlf_safe_patch/tests/test_r10e8r2_newlines.py' `
      'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' `
      'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' `
      'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
      'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R3 limited pytest failed' }
    & python -B -m phase169_r10e8_hyoujigen_generic_suspension.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E8R3 focused group audit failed' }
    $modified = @(& git diff --name-only)
    foreach ($path in $changedPaths) {
        if ($path -notin $modified) { throw "R10E8R3 expected source change missing: $path" }
    }
    $other = @($modified | Where-Object { $_ -notin $changedPaths })
    if ($other.Count -gt 0) {
        Write-Output ('R10E8R3_OTHER_EXISTING_TRACKED_DIFF=' + ($other -join ','))
    }
    Write-Output ('R10E8R3_PRODUCTION_FILES_CHANGED=' + ($changedPaths -join ','))
    Write-Output 'R10E8R3_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Output 'R10E8R3_INTEGRITY=PASS'
    Write-Output 'R10E8R3_FULL_PYTEST_RUN=False'
    $success = $true
}
catch {
    if ($backups.Count -eq 2) {
        foreach ($path in $backups.Keys) {
            [IO.File]::WriteAllBytes($path, $backups[$path])
        }
        Write-Output 'R10E8R3_ROLLBACK=tracked source restored to initial bytes'
    }
    if ($outputSnapshotted) {
        foreach ($path in $outputBackups.Keys) {
            if ($null -eq $outputBackups[$path]) {
                if (Test-Path $path) { Remove-Item -LiteralPath $path -Force }
            } else {
                [IO.File]::WriteAllBytes($path, $outputBackups[$path])
            }
        }
        Write-Output 'R10E8R3_OUTPUT_ROLLBACK=restored'
    }
    Write-Output ('R10E8R3_FAILURE=' + $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
