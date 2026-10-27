$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$changedPaths = @(
    'phase169_r10d2_general_family_definition/family_citation.py',
    'phase165_r52_r9_shared_math.py'
)
$reviewedBlobs = @{
    'phase169_r10d2_general_family_definition/family_citation.py' = '4a33870892e139ac52d7b26503584b4d9624e0ba'
    'phase165_r52_r9_shared_math.py' = 'e010e52fb06a20eb6c60557022ffb024036ed5c0'
}
$expectedHead = 'c3573d29e21688f54e73cf4d51ad53a5591d7959'
$backups = @{}
$patched = $false
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    $branch = (& git branch --show-current).Trim()
    $head = (& git rev-parse HEAD).Trim()
    Write-Output "R10E8_BRANCH=$branch"
    Write-Output "R10E8_HEAD=$head"
    Write-Output "R10E8_REVIEWED_GITHUB_HEAD=$expectedHead"
    if ($branch -ne 'develop' -or $head -ne $expectedHead) {
        throw 'R10E8 refused: Git branch or HEAD changed since source review'
    }
    foreach ($path in $changedPaths) {
        $sha = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $sha -ne $reviewedBlobs[$path]) {
            throw "R10E8 refused: reviewed Git blob does not match $path"
        }
        & git diff --quiet HEAD -- $path
        if ($LASTEXITCODE -ne 0) {
            throw "R10E8 refused: tracked local modifications in $path"
        }
        $absolute = Join-Path $root ($path -replace '/', [IO.Path]::DirectorySeparatorChar)
        $backups[$absolute] = [IO.File]::ReadAllBytes($absolute)
    }
    Write-Output 'R10E8_GITHUB_REVIEWED_BLOBS=PASS'
    Write-Output 'R10E8_SCOPE=CHAPTER_VI_SOURCE_ONLY_PLUS_SHARED_BRIDGE_WIRING'
    & python -B -m phase169_r10e8_hyoujigen_generic_suspension.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E8 guarded patch failed' }
    $patched = $true
    & python -B -m pytest -q -p no:cacheprovider `
      'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' `
      'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' `
      'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
      'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10E8 focused pytest failed' }
    & python -B -m phase169_r10e8_hyoujigen_generic_suspension.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E8 focused group search audit failed' }
    $modified = @(& git diff --name-only)
    $unexpected = @($modified | Where-Object { $_ -notin $changedPaths })
    if ($unexpected.Count -gt 0) {
        Write-Output ('R10E8_EXISTING_OTHER_DIFF=' + ($unexpected -join ','))
    }
    foreach ($path in $changedPaths) {
        if ($path -notin $modified) { throw "R10E8 expected patch absent: $path" }
    }
    Write-Output ('R10E8_PRODUCTION_FILES_CHANGED=' + ($changedPaths -join ','))
    Write-Output 'R10E8_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Output 'R10E8_INTEGRITY=PASS'
    Write-Output 'R10E8_FULL_PYTEST_RUN=False'
}
catch {
    if ($backups.Count -eq 2) {
        foreach ($path in $backups.Keys) {
            [IO.File]::WriteAllBytes($path, $backups[$path])
        }
        Write-Output 'R10E8_ROLLBACK=tracked source restored to initial bytes'
    }
    Write-Output ('R10E8_FAILURE=' + $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
