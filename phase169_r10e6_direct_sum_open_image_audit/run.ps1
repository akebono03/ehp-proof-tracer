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
    'phase165_r52_r9_shared_math.py' = 'e010e52fb06a20eb6c60557022ffb024036ed5c0'
    'phase169_r10e5_composite_generator_image/rule.py' = '01acace3eb273d47091421a61291ee54b51c369f'
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' = '48bae67c01b6a22a21ec2b9e90255c07b4e53696'
    'phase169_r10e4_ordered_db_prior/db_prior.py' = 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b'
    'phase169_r10e1_general_group_transport/transport.py' = 'd60770fff1b6e14791db6b952733f4062a64c8eb'
    'phase165_r55_nk_only_goal.py' = 'b207b8169590e634229d412324d857ffb3857939'
}
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git branch command failed' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git HEAD command failed' }
    Write-Host "R10E6_BRANCH=$branch"
    Write-Host "R10E6_HEAD=$head"
    Write-Host 'R10E6_REVIEWED_GITHUB_HEAD=c61bfaa72b75121c256518fbe37c7e8e27e5f815'
    if ($branch -ne 'develop') { throw 'R10E6 requires develop branch' }
    # An uncommitted R10E5 installation on the previously reviewed base is
    # accepted ONLY if all relevant working tree blobs match current GitHub.
    $allowedHeads = @(
        'c61bfaa72b75121c256518fbe37c7e8e27e5f815',
        'd6c4bd745b2537ffe4da72a7a77865d3c00f6e18'
    )
    if ($allowedHeads -notcontains $head) {
        throw 'R10E6 HEAD moved: re-review new GitHub diff before re-running'
    }
    foreach ($entry in $expectedBlobs.GetEnumerator()) {
        $path = Join-Path $root $entry.Key
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Required reviewed file missing: $($entry.Key)"
        }
        $blob = (git hash-object -- $entry.Key).Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $entry.Value) {
            throw "Reviewed source does not match current GitHub blob: $($entry.Key)"
        }
    }
    Write-Host 'R10E6_GITHUB_REVIEWED_BLOBS=PASS'
    $before = (@(git -c core.quotepath=false status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect git tracked status' }
    foreach ($name in $generated) {
        $path = Join-Path $here $name
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $originalOutputs[$name] = [System.IO.File]::ReadAllBytes($path)
        } else {
            $originalOutputs[$name] = $null
        }
    }
    $outputsSnapshotTaken = $true
    Write-Host 'R10E6_MODE=AUDIT_ONLY'
    $focused = @(
        'phase169_r10e6_direct_sum_open_image_audit/tests',
        'phase169_r10e5_composite_generator_image/tests',
        'phase169_r10e1_general_group_transport/tests',
        'phase169_r10e4_ordered_db_prior/tests'
    )
    python -m pytest -q @focused
    if ($LASTEXITCODE -ne 0) { throw 'R10E6 focused pytest failed' }
    python -m phase169_r10e6_direct_sum_open_image_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E6 audit failed' }
    $after = (@(git -c core.quotepath=false status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect git tracked status after audit' }
    if ($after -cne $before) {
        throw 'R10E6 integrity: changed tracked status unexpectedly'
    }
    $success = $true
    Write-Host 'R10E6_INTEGRITY=PASS'
    Write-Host 'R10E6_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host 'R10E6_PRODUCTION_FILES_CHANGED=none'
    Write-Host 'R10E6_FULL_PYTEST_RUN=False'
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
        Write-Host 'R10E6_OUTPUT_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
