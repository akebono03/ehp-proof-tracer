$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$before = $null
$head = $null
$previousLocation = Get-Location

try {
    Set-Location $root
    $branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R10EA requires the develop branch'
    }
    $head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read current HEAD' }
    Write-Output "R10EA_BRANCH=$branch"
    Write-Output "R10EA_HEAD=$head"

    # Accept later descendant commits without disabling source-content guards.
    $reviewedBase = '6825994198218f7e7fafc8c4fb29925c06eb0bd5'
    & git merge-base --is-ancestor $reviewedBase $head
    if ($LASTEXITCODE -ne 0) { throw 'R10EA refused: HEAD is not a descendant of reviewed develop' }
    Write-Output "R10EA_REVIEWED_ANCESTOR=$reviewedBase"

    $reviewedBlobs = @{
        'phase168_r3_5_model_renderer.py' = 'd4d0aa6b3973d5c3d6fe88861cf11948c419cd6b'
        'phase168_r3_3_proof_narrative_model.py' = '1080843a2a90bf60f0b8096d3c5542a24a9abb7c'
        'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
        'phase168_r3_29_order_projection.py' = 'b0eaf673fa0d36a31a6831b1297679b48453d8a8'
        'phase168_r3_4_link_bridge.py' = 'c3a6233a57c41e61e6649ee33c7a336d7aa1c664'
    }

    foreach ($path in @($reviewedBlobs.Keys)) {
        $blob = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $reviewedBlobs[$path]) {
            throw "R10EA refused: reviewed source changed: $path"
        }
        & git diff --quiet -- $path
        if ($LASTEXITCODE -ne 0) {
            throw "R10EA refused: renderer or verification has local modifications: $path"
        }
    }
    Write-Output 'R10EA_REVIEWED_RENDERER_AND_TRUST_BLOBS=PASS'

    $eta = Join-Path $root 'phase165_r12_r21_eta_generator_chain.py'
    $sourceA = Join-Path $root 'phase169_r10d2_general_family_definition/family_citation.py'
    $sourceB = Join-Path $root 'phase165_r52_r9_shared_math.py'
    if (-not (Test-Path $eta) -or -not (Test-Path $sourceA) -or -not (Test-Path $sourceB)) {
        throw 'R10EA requires the R10E8 and R10E9 production sources'
    }
    $etaText = [System.IO.File]::ReadAllText($eta)
    $aText = [System.IO.File]::ReadAllText($sourceA)
    $bText = [System.IO.File]::ReadAllText($sourceB)
    if (-not $etaText.Contains('_matching_eta_name(goal.source_generator, older.element)')) {
        throw 'R10EA refused: R10E9 typed-eta alias not installed'
    }
    if (-not $aText.Contains('CHAPTER_VI_SOURCE_RECORDS') -or
        -not $bText.Contains('build_cited_chapter_vi_family_definitions')) {
        throw 'R10EA refused: R10E8 Chapter VI sources not connected'
    }
    Write-Output 'R10EA_R10E8_R10E9_PRECONDITIONS=PASS'

    # No production files or existing tests are modified in this audit.
    $trackedBefore = ((& git status --porcelain --untracked-files=no) -join "`n")
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = ''
    Write-Output 'R10EA_MODE=AUDIT_ONLY'

    & python -m pytest -q -p no:cacheprovider `
        'phase169_r10ea_direct_sum_narrative_audit/tests/test_r10ea_audit.py' `
        'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
        'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' `
        'phase169_r10e9_eta_composite_alias_fix/tests/test_r10e9_eta_composite_alias.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EA limited pytest failed' }

    & python -m phase169_r10ea_direct_sum_narrative_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10EA audit or proof replay failed' }

    $trackedAfter = ((& git status --porcelain --untracked-files=no) -join "`n")
    if ($trackedBefore -ne $trackedAfter) {
        throw 'R10EA tracked-file integrity changed during audit'
    }
    Write-Output 'R10EA_TRACKED_FILES_UNCHANGED=PASS'
    Write-Output 'R10EA_FULL_PYTEST_RUN=False'
    Write-Output 'R10EA_LIMITED_TESTS_AND_AUDIT=PASS'
}
catch {
    Write-Output ('R10EA_FAILURE=' + $_.Exception.Message)
    exit 1
}
finally {
    Set-Location $previousLocation
}
