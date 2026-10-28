$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
$Output = Join-Path $Package "output\run_$Stamp"
New-Item -ItemType Directory -Force -Path $Output | Out-Null
Push-Location $Repo
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EM cannot read git branch' }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10EM cannot read git HEAD' }
    Write-Host "R10EM_BRANCH=$Branch"
    Write-Host "R10EM_HEAD=$Head"
    Write-Host 'R10EM_MODE=AUDIT_ONLY'
    if ($Branch -ne 'develop') { throw 'R10EM requires develop and does not perform checkout or reset' }
    & git merge-base --is-ancestor '22007678c7d43c8e6410b7905412cf4e8f0790bc' HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10EM requires reviewed Phase169 R10EL predecessor' }
    $Expected = @{
        'phase169_r10a_verified_stable_chain_projection/projection.py' = 'c039a95c31d04d2ca314332f8048f9f1a3723529'
        'phase169_r10ec_direct_sum_narrative_projection/projection.py' = 'd1c863be87462ab64c2c833b324e427d81231473'
        'phase169_r10el_shared_generator_suppression/core.py' = '61d53fdedefc7edcdf7ce4875984959505faa9f0'
        'phase168_r3_5_model_renderer.py' = '2685ef3ef6bf7bc1673dededef1e3487d9941362'
    }
    foreach ($Relative in $Expected.Keys) {
        $Actual = (& git hash-object -- $Relative).Trim()
        if ($LASTEXITCODE -ne 0 -or $Actual -ne $Expected[$Relative]) {
            throw "R10EM unreviewed source for $Relative (blob=$Actual)"
        }
    }
    Write-Host 'R10EM_REVIEWED_DEPENDENCIES=PASS'
    $Before = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EM cannot capture tracked status' }
    $OldPythonNoBytecode = $env:PYTHONDONTWRITEBYTECODE
    $env:PYTHONDONTWRITEBYTECODE = '1'
    try {
        & python -B -m pytest -q -p no:cacheprovider '.\phase169_r10em_citation_provenance_audit\tests\test_r10em_provenance.py'
        if ($LASTEXITCODE -ne 0) { throw 'R10EM focused provenance tests failed' }
        & python -B -m phase169_r10em_citation_provenance_audit.audit $Output
        if ($LASTEXITCODE -ne 0) { throw 'R10EM real-proof provenance audit failed' }
    }
    finally {
        $env:PYTHONDONTWRITEBYTECODE = $OldPythonNoBytecode
    }
    $After = @(& git -c core.quotepath=false status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0) { throw 'R10EM cannot check tracked status' }
    if (@(Compare-Object -ReferenceObject $Before -DifferenceObject $After).Count -ne 0) {
        Write-Host "R10EM_TRACKED_BEFORE=$($Before -join '; ')"
        Write-Host "R10EM_TRACKED_AFTER=$($After -join '; ')"
        throw 'R10EM unexpectedly altered tracked worktree status'
    }
    Write-Host 'R10EM_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Host 'R10EM_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10EM_FULL_PYTEST_RUN=False'
    Write-Host 'R10EM_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host "R10EM_OUTPUT=$Output"
}
finally {
    Pop-Location
}
