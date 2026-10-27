$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
$base = '940d1d1cc2e9943e9d2955c7204a4392984d65e9'
$target = 'phase165_r12_r21_eta_generator_chain.py'
$reviewed = @{
    'phase165_r12_r21_eta_generator_chain.py' = 'dfd5eb7eb85ef5635aa68ad0b50de49a48aaf59c'
    'phase165_r12_r28_presentation_connection.py' = '8fa601c8bdc8a13a100021484d9df58c3c05ac8b'
    'phase165_r12_r20_eta_definition.py' = '9d7058607c102c47265a192735180cac36321910'
    'phase169_r10e5_composite_generator_image/rule.py' = '01acace3eb273d47091421a61291ee54b51c369f'
    'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
    'data/HyoujiGen.csv' = '26f33db0c83ba7f151433583fe861598399cbe6a'
}
$targetPath = Join-Path $root $target
$outputFolder = Join-Path $folder 'output'
$outputNames = @('_eta_pair_FULL.py', 'phase165_r12_r21_eta_generator_chain.py.FULL', 'audit.json')
$before = $null
$outputBefore = @{}
$snapshot = $false
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    $branch = (& git branch --show-current).Trim()
    $head = (& git rev-parse HEAD).Trim()
    Write-Output "R10E9_BRANCH=$branch"
    Write-Output "R10E9_HEAD=$head"
    Write-Output "R10E9_REVIEWED_GITHUB_BASE=$base"
    if ($branch -ne 'develop') { throw 'R10E9 requires develop branch' }
    & git merge-base --is-ancestor $base HEAD
    if ($LASTEXITCODE -ne 0) { throw 'R10E9 refused: current HEAD is not descended from the reviewed base' }
    foreach ($path in $reviewed.Keys) {
        $blob = (& git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $reviewed[$path]) {
            throw "R10E9 refused: reviewed dependency changed $path"
        }
    }
    & git diff --quiet HEAD -- $target
    if ($LASTEXITCODE -ne 0) { throw 'R10E9 refused: eta source has existing tracked changes' }
    $family = Join-Path $root 'phase169_r10d2_general_family_definition/family_citation.py'
    $shared = Join-Path $root 'phase165_r52_r9_shared_math.py'
    if (-not (([IO.File]::ReadAllText($family)).Contains('CHAPTER_VI_SOURCE_RECORDS'))) {
        throw 'R10E9 requires successfully applied R10E8 family source wiring'
    }
    if (-not (([IO.File]::ReadAllText($shared)).Contains('build_cited_chapter_vi_family_definitions'))) {
        throw 'R10E9 requires successfully applied R10E8 shared source wiring'
    }
    $priorNames = @(& git diff --name-only)
    $before = [IO.File]::ReadAllBytes($targetPath)
    foreach ($name in $outputNames) {
        $path = Join-Path $outputFolder $name
        if (Test-Path $path) {
            $outputBefore[$path] = [IO.File]::ReadAllBytes($path)
        } else {
            $outputBefore[$path] = $null
        }
    }
    $snapshot = $true
    Write-Output 'R10E9_REVIEWED_GITHUB_BLOBS=PASS'
    Write-Output 'R10E9_SCOPE=ETA_TYPED_NAME_ALIAS_ONLY'
    & python -B -m phase169_r10e9_eta_composite_alias_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E9 guarded function patch failed' }
    & python -B -m pytest -q -p no:cacheprovider `
        'phase169_r10e9_eta_composite_alias_fix/tests/test_r10e9_eta_composite_alias.py' `
        'phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py' `
        'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' `
        'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10E9 limited pytest failed' }
    & python -B -m phase169_r10e9_eta_composite_alias_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E9 focused 9-stem audit failed' }
    $afterNames = @(& git diff --name-only)
    if ($target -notin $afterNames) { throw 'R10E9 eta source patch not observed' }
    $expectedNames = @($priorNames) + @($target) | Select-Object -Unique
    $unexpected = @($afterNames | Where-Object { $_ -notin $expectedNames })
    if ($unexpected.Count -gt 0) { throw ('R10E9 unexpected tracked diff: ' + ($unexpected -join ',')) }
    $missing = @($priorNames | Where-Object { $_ -notin $afterNames })
    if ($missing.Count -gt 0) { throw ('R10E9 existing tracked diff lost: ' + ($missing -join ',')) }
    Write-Output ('R10E9_PRODUCTION_FILES_CHANGED=' + $target)
    Write-Output 'R10E9_SOURCE_EQUATIONS_ADDED=False'
    Write-Output 'R10E9_INFERENCE_ENGINE_CHANGED=False'
    Write-Output 'R10E9_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Output 'R10E9_INTEGRITY=PASS'
    Write-Output 'R10E9_FULL_PYTEST_RUN=False'
}
catch {
    if ($null -ne $before) {
        [IO.File]::WriteAllBytes($targetPath, $before)
        Write-Output 'R10E9_ROLLBACK=eta source restored to original bytes'
    }
    if ($snapshot) {
        foreach ($path in $outputBefore.Keys) {
            if ($null -eq $outputBefore[$path]) {
                if (Test-Path $path) { Remove-Item -LiteralPath $path -Force }
            } else {
                [IO.File]::WriteAllBytes($path, $outputBefore[$path])
            }
        }
        Write-Output 'R10E9_OUTPUT_ROLLBACK=restored'
    }
    Write-Output ('R10E9_FAILURE=' + $_.Exception.Message)
    exit 1
}
finally { Pop-Location }
