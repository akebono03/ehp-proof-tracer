$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Package "output\run_$Stamp"
$Targets = @(
    'phase169_r10a_verified_stable_chain_projection/projection.py',
    'phase169_r10ec_direct_sum_narrative_projection/projection.py'
)
$Expected = @{
    'phase169_r10a_verified_stable_chain_projection/projection.py' = 'c039a95c31d04d2ca314332f8048f9f1a3723529'
    'phase169_r10ec_direct_sum_narrative_projection/projection.py' = 'd1c863be87462ab64c2c833b324e427d81231473'
    'phase169_r10el_shared_generator_suppression/core.py' = '61d53fdedefc7edcdf7ce4875984959505faa9f0'
    'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
}
$Patched = $false
$Success = $false
$Before = @()
$OldPythonNoBytecode = $env:PYTHONDONTWRITEBYTECODE
Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EN cannot obtain Git HEAD' }
    Write-Output "R10EN_BRANCH=$Branch"
    Write-Output "R10EN_HEAD=$Head"
    if ($Branch -ne 'develop') { throw 'R10EN requires develop branch' }
    & git merge-base --is-ancestor '5b863e6fdb4ec87b4b6294b4bce5fcdf21f514b8' HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10EN requires the reviewed R10EL baseline' }
    foreach ($Relative in $Expected.Keys) {
        $Actual = (& git hash-object -- $Relative).Trim()
        if ($LASTEXITCODE -ne 0 -or $Actual -ne $Expected[$Relative]) {
            throw "R10EN reviewed dependency mismatch: $Relative ($Actual)"
        }
    }
    foreach ($Relative in $Targets) {
        $Changes = @(& git status --porcelain --untracked-files=no -- $Relative)
        if ($Changes.Count -ne 0) { throw "R10EN target has uncommitted changes: $Relative" }
    }
    Write-Output 'R10EN_REVIEWED_DEPENDENCIES=PASS'
    $Before = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EN cannot snapshot Git status' }
    New-Item -ItemType Directory -Force -Path $Output | Out-Null
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & python -B -m pytest -q -p no:cacheprovider `
        '.\phase169_r10en_shared_citation_provenance\tests\test_r10en_core.py' `
        '.\phase169_r10en_shared_citation_provenance\tests\test_r10en_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EN independent tests failed' }
    $Apply = 'from pathlib import Path; from phase169_r10en_shared_citation_provenance.patch import apply; import sys; apply(Path(sys.argv[1]), Path(sys.argv[2]))'
    & python -B -c $Apply $Repo $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EN checked patch failed' }
    $Patched = $true
    & python -B -m pytest -q -p no:cacheprovider `
        '.\phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py' `
        '.\phase169_r10ec_direct_sum_narrative_projection\tests\test_r10ec_projection.py' `
        '.\phase169_r10el_shared_generator_suppression\tests\test_r10el_live.py' `
        '.\phase169_r10em_citation_provenance_audit\tests\test_r10em_provenance.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EN focused regression tests failed' }
    & python -B -m phase169_r10en_shared_citation_provenance.audit $Output
    if ($LASTEXITCODE -ne 0) { throw 'R10EN complete-proof audit failed' }
    $After = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EN cannot check Git status' }
    $BeforeUnrelated = @($Before | Where-Object {
        $_.Length -lt 4 -or $Targets -notcontains $_.Substring(3).Replace('\','/')
    })
    $AfterUnrelated = @($After | Where-Object {
        $_.Length -lt 4 -or $Targets -notcontains $_.Substring(3).Replace('\','/')
    })
    $BeforeText = (@($BeforeUnrelated | Sort-Object) -join "`n")
    $AfterText = (@($AfterUnrelated | Sort-Object) -join "`n")
    if ($BeforeText -cne $AfterText) {
        throw 'R10EN unexpectedly changed other tracked files'
    }
    $Success = $true
    Write-Output 'R10EN_UNRELATED_TRACKED_FILES_UNCHANGED=PASS'
    Write-Output 'R10EN_INFERENCE_RULES_CHANGED=False'
    Write-Output 'R10EN_PROOF_TREE_CHANGED=False'
    Write-Output 'R10EN_FULL_PYTEST_RUN=False'
    Write-Output 'R10EN_FOCUSED_TESTS_AND_AUDIT=PASS'
    Write-Output "R10EN_OUTPUT=$Output"
}
finally {
    if ($Patched -and -not $Success) {
        foreach ($Relative in $Targets) {
            $Target = Join-Path $Repo $Relative
            $Name = (Split-Path -Leaf (Split-Path -Parent $Target)) + '_projection.py.before'
            $Backup = Join-Path $Output $Name
            if (Test-Path -LiteralPath $Backup) {
                [System.IO.File]::WriteAllBytes(
                    $Target, [System.IO.File]::ReadAllBytes($Backup)
                )
                Write-Output "R10EN_ROLLBACK=$Relative"
            }
        }
    }
    $env:PYTHONDONTWRITEBYTECODE = $OldPythonNoBytecode
    Pop-Location
}
