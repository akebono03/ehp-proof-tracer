$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = (Resolve-Path (Join-Path $here '..')).Path
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
$success = $false
$outputsSnapshotTaken = $false
$originalOutputs = @{}
$generated = @('output/audit.json', 'output/audit.md')
$expectedBlobs = [ordered]@{
    'data/HyoujiGen.csv' = '26f33db0c83ba7f151433583fe861598399cbe6a'
    'sources/toda/Toda_06_2.tex' = '76934583cff01c8ea83f768e26947eb9b556653b'
    'phase163_r4_r94_output/manifest.json' = '8f6fc9bdcb28e7eb038d2a01cedcbbbcc2bc2457'
    'phase169_r10d2_general_family_definition/family_citation.py' = '4a33870892e139ac52d7b26503584b4d9624e0ba'
    'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py' = '3b1255e9942d95dae06d104df38ac750c201e452'
    'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
    'phase169_r10e6_direct_sum_open_image_audit/audit.py' = 'a7112bb993b86955446bb3430f83960c544b32b3'
    'phase169_r10e6_direct_sum_open_image_audit/tests/test_r10e6_audit.py' = 'fdb8762eb829c7ea85452566c8044a9fc80ca89a'
}
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git branch command failed' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git HEAD command failed' }
    Write-Host "R10E7_BRANCH=$branch"
    Write-Host "R10E7_HEAD=$head"
    Write-Host 'R10E7_REVIEWED_GITHUB_HEAD=c3573d29e21688f54e73cf4d51ad53a5591d7959'
    if ($branch -ne 'develop') { throw 'R10E7 requires develop branch' }
    $allowedHeads = @(
        'c61bfaa72b75121c256518fbe37c7e8e27e5f815',
        'c3573d29e21688f54e73cf4d51ad53a5591d7959'
    )
    if ($allowedHeads -notcontains $head) {
        throw 'R10E7 HEAD has changed: review the new GitHub diff before rerunning.'
    }
    foreach ($entry in $expectedBlobs.GetEnumerator()) {
        $path = Join-Path $root $entry.Key
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Required reviewed file missing: $($entry.Key)"
        }
        $blob = (git hash-object -- $entry.Key).Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $entry.Value) {
            throw "Reviewed blob mismatch: $($entry.Key)"
        }
    }
    Write-Host 'R10E7_GITHUB_REVIEWED_BLOBS=PASS'
    $before = (@(git -c core.quotepath=false status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect tracked git status' }
    foreach ($name in $generated) {
        $path = Join-Path $here $name
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $originalOutputs[$name] = [System.IO.File]::ReadAllBytes($path)
        } else {
            $originalOutputs[$name] = $null
        }
    }
    $outputsSnapshotTaken = $true
    Write-Host 'R10E7_MODE=AUDIT_ONLY'
    $focused = @(
        'phase169_r10e7_ch6_family_source_audit/tests',
        'phase169_r10d2_general_family_definition/tests',
        'phase169_r10b_registered_stable_family_binding/tests',
        'phase169_r10e6_direct_sum_open_image_audit/tests'
    )
    python -m pytest -q @focused
    if ($LASTEXITCODE -ne 0) { throw 'R10E7 focused pytest failed' }
    python -m phase169_r10e7_ch6_family_source_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E7 audit failed' }
    $after = (@(git -c core.quotepath=false status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0 -or $before -cne $after) {
        throw 'R10E7 integrity: tracked files changed'
    }
    $success = $true
    Write-Host 'R10E7_INTEGRITY=PASS'
    Write-Host 'R10E7_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E7_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10E7_FULL_PYTEST_RUN=False'
} finally {
    if (-not $success -and $outputsSnapshotTaken) {
        foreach ($name in $generated) {
            $path = Join-Path $here $name
            $previous = $originalOutputs[$name]
            if ($null -ne $previous) {
                [System.IO.Directory]::CreateDirectory((Split-Path -Parent $path)) | Out-Null
                [System.IO.File]::WriteAllBytes($path, $previous)
            } elseif (Test-Path -LiteralPath $path -PathType Leaf) {
                Remove-Item -LiteralPath $path -Force
            }
        }
        Write-Host 'R10E7_OUTPUT_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
