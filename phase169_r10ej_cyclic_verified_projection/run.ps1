$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Package ("output\run_" + $Stamp)
$Target = 'phase169_r10a_verified_stable_chain_projection/projection.py'
$Installed = $false
$Success = $false

Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R10EJ requires an existing local develop branch; no checkout/reset performed'
    }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ git HEAD unavailable' }
    Write-Host "R10EJ_BRANCH=$Branch"
    Write-Host "R10EJ_HEAD=$Head"
    & git merge-base --is-ancestor 'f4dac2b166afde19babeb523e42b973bdf5f3569' HEAD
    if ($LASTEXITCODE -ne 0) {
        throw 'R10EJ requires the reviewed R10EI Git history'
    }
    if (-not (Test-Path -LiteralPath $Target -PathType Leaf)) {
        throw 'R10EJ target source missing'
    }
    $StatusBefore = @(& git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ baseline git status failed' }
    if (@($StatusBefore | Where-Object { $_.Contains($Target) }).Count -ne 0) {
        throw 'R10EJ target already has tracked changes; refusing to overwrite it'
    }
    Write-Host 'R10EJ_SCOPE=VERIFIED_CYCLIC_PRESENTATION_ONLY'
    Write-Host 'R10EJ_REVIEWED_ANCESTOR_AND_TARGET_CLEAN=PASS'

    & python -B -m pytest -q --import-mode=importlib '.\phase169_r10ej_cyclic_verified_projection\tests\test_r10ej_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ static patch tests failed' }

    & python -B -m phase169_r10ej_cyclic_verified_projection.apply apply --root $Repo --output $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ one-function patch failed' }
    $Installed = $true

    $Tests = @(
        '.\phase169_r10ej_cyclic_verified_projection\tests\test_r10ej_live.py',
        '.\phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py',
        '.\phase169_r10e1_general_group_transport\tests\test_r10e1_general_transport.py',
        '.\phase169_r10ec_direct_sum_narrative_projection\tests\test_r10ec_projection.py',
        '.\phase169_r10eg_one_stem_route_priority\tests\test_r10eg_live.py'
    )
    & python -B -m pytest -q --import-mode=importlib @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ focused pytest failed' }

    & python -B -m phase169_r10ej_cyclic_verified_projection.audit --output (Join-Path $Output 'audit')
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ full Proof Tree and narrative audit failed' }

    $StatusAfter = @(& git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EJ final git status failed' }
    $OtherAfter = @($StatusAfter | Where-Object { -not $_.Contains($Target) })
    $BeforeComparable = @($StatusBefore | Where-Object { -not $_.Contains($Target) })
    $OtherAfterText = ($OtherAfter | Sort-Object) -join "`n"
    $BeforeText = ($BeforeComparable | Sort-Object) -join "`n"
    if ($OtherAfterText -ne $BeforeText) {
        throw 'R10EJ unexpectedly changed other tracked files'
    }
    if (@($StatusAfter | Where-Object { $_.Contains($Target) }).Count -ne 1) {
        throw 'R10EJ target change not visible as a single tracked edit'
    }
    Write-Host 'R10EJ_UNRELATED_TRACKED_FILES_UNCHANGED=PASS'
    Write-Host 'R10EJ_INFERENCE_RULES_CHANGED=False'
    Write-Host 'R10EJ_PROOF_TREE_CHANGED=False'
    Write-Host 'R10EJ_FULL_PYTEST_RUN=False'
    Write-Host 'R10EJ_FOCUSED_TESTS_AND_AUDIT=PASS'
    Write-Host "R10EJ_OUTPUT=$Output"
    $Success = $true
}
finally {
    if (-not $Success -and $Installed) {
        & python -B -m phase169_r10ej_cyclic_verified_projection.apply restore --root $Repo --output $Output
        if ($LASTEXITCODE -ne 0) {
            Write-Warning 'R10EJ automatic restoration failed; review byte-exact backup!'
        }
    }
    Pop-Location
}
