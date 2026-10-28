param()
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$stage = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $stage
Set-Location $repo
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
Write-Output "R10EL_BRANCH=$branch"
Write-Output "R10EL_HEAD=$head"
if ($branch -ne 'develop') { throw 'R10EL requires develop branch' }
& git merge-base --is-ancestor '01e20c4d7bb74b8680bd3311130358266c97e884' HEAD
if ($LASTEXITCODE -ne 0) { throw 'R10EL review baseline is not ancestor of HEAD' }
$targets = @(
    'phase169_r10a_verified_stable_chain_projection/projection.py',
    'phase169_r10ec_direct_sum_narrative_projection/projection.py'
)
$reviewed = @(
    '60aa71eebac2441c8b1f51f8636f7c8b63b1c51eaacc744132e84d7098fb9864',
    '53c20a8c3911866de7da44f31df1a965e333d5a4961ab215918637334ec686e0'
)
for ($i = 0; $i -lt $targets.Count; $i++) {
    $target = Join-Path $repo $targets[$i]
    $hash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $reviewed[$i]) { throw "R10EL reviewed target hash mismatch: $($targets[$i])" }
    $status = @(& git status --porcelain --untracked-files=no -- $targets[$i])
    if ($status.Count -gt 0) { throw "R10EL target has uncommitted changes: $($targets[$i])" }
}
Write-Output 'R10EL_REVIEWED_BASELINES=PASS'
function Get-UnrelatedTracked {
    $entries = @(& git status --porcelain --untracked-files=no)
    return @($entries | Where-Object {
        ($_.Length -lt 4) -or ($targets -notcontains $_.Substring(3).Replace('\','/'))
    })
}
$before = @(Get-UnrelatedTracked)
$out = Join-Path $stage ("output/run_" + (Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'))
New-Item -ItemType Directory -Force -Path $out | Out-Null
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:PYTHONDONTWRITEBYTECODE = '1'
$patched = $false
$completed = $false
try {
    & python -B -m pytest -q -p no:cacheprovider `
        '.\phase169_r10el_shared_generator_suppression\tests\test_r10el_patch.py' `
        '.\phase169_r10el_shared_generator_suppression\tests\test_r10el_isolated.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EL offline patch tests failed' }
    $call = 'from pathlib import Path; from phase169_r10el_shared_generator_suppression.patch import apply; import sys; apply(Path(sys.argv[1]), Path(sys.argv[2]))'
    & python -B -c $call $repo $out
    if ($LASTEXITCODE -ne 0) { throw 'R10EL patch failed' }
    $patched = $true
    & python -B -m pytest -q -p no:cacheprovider `
        '.\phase169_r10el_shared_generator_suppression\tests\test_r10el_live.py' `
        '.\phase169_r10ej_cyclic_verified_projection\tests\test_r10ej_live.py' `
        '.\phase169_r10a_verified_stable_chain_projection\tests\test_r10a_verified_stable_chain.py' `
        '.\phase169_r10ec_direct_sum_narrative_projection\tests\test_r10ec_projection.py'
    if ($LASTEXITCODE -ne 0) { throw 'R10EL focused regressions failed' }
    & python -B -m phase169_r10el_shared_generator_suppression.audit $out
    if ($LASTEXITCODE -ne 0) { throw 'R10EL real-proof audit failed' }
    $after = @(Get-UnrelatedTracked)
    $beforeStatus = (@($before | Sort-Object) -join "`n")
    $afterStatus = (@($after | Sort-Object) -join "`n")
    if ($beforeStatus -cne $afterStatus) { throw 'R10EL changed unrelated tracked files' }
    $completed = $true
    Write-Output 'R10EL_UNRELATED_TRACKED_FILES_UNCHANGED=PASS'
    Write-Output 'R10EL_INFERENCE_RULES_CHANGED=False'
    Write-Output 'R10EL_PROOF_TREE_CHANGED=False'
    Write-Output 'R10EL_FULL_PYTEST_RUN=False'
    Write-Output 'R10EL_FOCUSED_TESTS_AND_AUDIT=PASS'
    Write-Output "R10EL_OUTPUT=$out"
} finally {
    if ($patched -and -not $completed) {
        for ($i = 0; $i -lt $targets.Count; $i++) {
            $target = Join-Path $repo $targets[$i]
            $name = (Split-Path -Leaf (Split-Path -Parent $target)) + '_projection.py.before'
            $backup = Join-Path $out $name
            if (Test-Path -LiteralPath $backup) {
                [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
                Write-Output "R10EL_ROLLBACK=$target"
            }
        }
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
}
