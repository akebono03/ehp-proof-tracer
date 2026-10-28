$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$OriginalRunner = Join-Path $Repo 'phase169_r10ej_cyclic_verified_projection\run.ps1'
$CacheFile = Join-Path $Repo '.pytest_cache\v\cache\nodeids'
$OldAddopts = [Environment]::GetEnvironmentVariable('PYTEST_ADDOPTS', 'Process')

Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R10EJ-R1 requires local develop; no checkout/reset performed'
    }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ-R1 git HEAD unavailable' }
    Write-Host "R10EJR1_BRANCH=$Branch"
    Write-Host "R10EJR1_HEAD=$Head"
    Write-Host 'R10EJR1_SCOPE=PYTEST_CACHE_ISOLATION_ONLY'
    Write-Host 'R10EJR1_ORIGINAL_RUNNER_PRESERVED=True'
    if (Test-Path -LiteralPath $CacheFile -PathType Leaf) {
        $CacheBefore = (Get-FileHash -Algorithm SHA256 -LiteralPath $CacheFile).Hash
        Write-Host 'R10EJR1_EXISTING_CACHE=present (left unchanged)'
    } else {
        $CacheBefore = $null
        Write-Host 'R10EJR1_EXISTING_CACHE=absent'
    }

    & python -B -m phase169_r10ejr1_pytest_cache_isolation.verify check $Repo
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ-R1 original runner guard failed' }

    # The original R10EJ runner invokes pytest twice. Propagate pytest's
    # documented environment option so both tests keep all normal assertions
    # but disable the cacheprovider plugin and its writes to tracked nodeids.
    $env:PYTEST_ADDOPTS = (($OldAddopts + ' -p no:cacheprovider').Trim())
    Write-Host 'R10EJR1_PYTEST_CACHE_PROVIDER=DISABLED'

    & python -B -m pytest -q --import-mode=importlib '.\phase169_r10ejr1_pytest_cache_isolation\tests\test_r10ejr1_verify.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ-R1 focused wrapper tests failed' }

    & powershell -NoProfile -ExecutionPolicy Bypass -File $OriginalRunner
    if ($LASTEXITCODE -ne 0) { throw 'Original R10EJ run failed (its rollback policy remains authoritative)' }

    if ($null -eq $CacheBefore) {
        if (Test-Path -LiteralPath $CacheFile -PathType Leaf) {
            throw 'R10EJ-R1 unexpected pytest cache creation'
        }
    } else {
        if (-not (Test-Path -LiteralPath $CacheFile -PathType Leaf)) {
            throw 'R10EJ-R1 unexpected pytest cache deletion'
        }
        $CacheAfter = (Get-FileHash -Algorithm SHA256 -LiteralPath $CacheFile).Hash
        if ($CacheAfter -ne $CacheBefore) {
            throw 'R10EJ-R1 unexpectedly changed previously tracked pytest cache'
        }
    }
    & python -B -m phase169_r10ejr1_pytest_cache_isolation.verify check $Repo
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ original runner changed unexpectedly' }
    Write-Host 'R10EJR1_PYTEST_CACHE_UNCHANGED=PASS'
    Write-Host 'R10EJR1_PRODUCTION_PATCH_DELEGATED_TO_ORIGINAL_R10EJ=True'
    Write-Host 'R10EJR1_FULL_PYTEST_RUN=False'
    Write-Host 'R10EJR1_RESULT=PASS'
}
finally {
    if ($null -eq $OldAddopts) {
        Remove-Item Env:PYTEST_ADDOPTS -ErrorAction SilentlyContinue
    } else {
        $env:PYTEST_ADDOPTS = $OldAddopts
    }
    Pop-Location
}
