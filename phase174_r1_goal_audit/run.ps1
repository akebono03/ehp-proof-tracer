param(
    [switch]$DryRun,
    [switch]$SkipFocusedTests
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedHead = 'cb85913905b2f7452bda2a2c4428e6fe5a3a793a'
$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepositoryRoot

function Invoke-CheckedGit {
    param([string[]]$Arguments)
    $Result = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('git command failed: git ' + ($Arguments -join ' '))
    }
    return $Result
}

$Branch = (Invoke-CheckedGit -Arguments @('branch', '--show-current')).Trim()
$LocalHead = (Invoke-CheckedGit -Arguments @('rev-parse', 'HEAD')).Trim()
$RemoteLine = @(Invoke-CheckedGit -Arguments @('ls-remote', 'origin', 'refs/heads/develop'))
if ($RemoteLine.Count -ne 1) {
    throw 'Cannot uniquely resolve remote develop'
}
$RemoteHead = (($RemoteLine[0].Trim()) -split '\s+')[0]

Write-Output "PHASE174_R1_BRANCH=$Branch"
Write-Output "PHASE174_R1_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R1_REMOTE_HEAD=$RemoteHead"

if ($Branch -ne 'develop') {
    throw 'This audit requires the develop branch'
}
if ($RemoteHead -ne $ExpectedHead) {
    throw 'Remote HEAD changed. Review the new GitHub source before proceeding.'
}
if ($LocalHead -ne $ExpectedHead) {
    throw 'Local HEAD differs from reviewed remote HEAD. Synchronize manually after inspecting changes; this script will not pull, reset, or checkout.'
}

$ExpectedBlobs = [ordered]@{
    'toda_typed_group_facade.py' = '14c1b1752c1007c7dabb353c471cb021644e9e18'
    'phase165_r52_r5_auto_search.py' = 'e2d03a336f69b01fb69a2affa19b81fc73be0dbf'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'phase165_r52_partial_proof.py' = '0af6b459ed5a136a8e30a9e349ccf9fa601d448b'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
}
foreach ($Path in $ExpectedBlobs.Keys) {
    $ActualBlob = (Invoke-CheckedGit -Arguments @('hash-object', '--', $Path)).Trim()
    if ($ActualBlob -ne $ExpectedBlobs[$Path]) {
        throw "Source Guard mismatch: $Path"
    }
}
Write-Output 'PHASE174_R1_SOURCE_GUARD=PASS'

$StatusBefore = @(Invoke-CheckedGit -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexBefore = @(Invoke-CheckedGit -Arguments @('ls-files', '--stage')) -join "`n"

if ($DryRun) {
    Write-Output 'PHASE174_R1_DRY_RUN=PASS'
    Write-Output 'PHASE174_R1_NO_CODE_CHANGES=True'
    exit 0
}

$OldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'

    & python -B -m phase174_r1_goal_audit.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R1 goal audit failed'
    }

    if (-not $SkipFocusedTests) {
        & python -B -m pytest -q -p no:cacheprovider `
            test_phase165_r52_r2_search_adapter.py `
            test_phase165_r52_r5_auto_search.py `
            test_phase165_r55_nk_only_goal.py `
            phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
            phase174_r1_goal_audit/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) {
            throw 'Phase 174 R1 focused pytest failed'
        }
        Write-Output 'PHASE174_R1_FOCUSED_PYTEST=PASS'
    }
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoByteCode
    $env:PYTHONIOENCODING = $OldPythonIO
}

$StatusAfter = @(Invoke-CheckedGit -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexAfter = @(Invoke-CheckedGit -Arguments @('ls-files', '--stage')) -join "`n"

if ($StatusBefore -cne $StatusAfter) {
    throw 'Git worktree status changed during the audit'
}
if ($IndexBefore -cne $IndexAfter) {
    throw 'Git index changed during the audit'
}
Write-Output 'PHASE174_R1_GIT_STATUS_PRESERVED=PASS'
Write-Output 'PHASE174_R1_GIT_INDEX_PRESERVED=PASS'
Write-Output 'PHASE174_R1_GATE=PASS'
