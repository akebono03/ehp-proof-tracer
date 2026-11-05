param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedHead = '3558d713fd7939ded656f2458aacc62d71c7e0b3'
$R1BaselineHead = 'cb85913905b2f7452bda2a2c4428e6fe5a3a793a'
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
    throw 'Cannot uniquely resolve origin/develop'
}
$RemoteHead = (($RemoteLine[0].Trim()) -split '\s+')[0]

Write-Output "PHASE174_R2_BRANCH=$Branch"
Write-Output "PHASE174_R2_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R2_REMOTE_HEAD=$RemoteHead"

if ($Branch -ne 'develop' -or $LocalHead -ne $ExpectedHead -or $RemoteHead -ne $ExpectedHead) {
    throw 'Current HEAD differs from the reviewed develop HEAD; re-audit first'
}

$ExpectedBlobs = [ordered]@{
    'sources/toda/Toda_04_2.tex' = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7'
    'sources/toda/Toda_05_2.tex' = '579661138928499ba04a51327f686d9b971b5314'
    'phase165_r52_r9_shared_math.py' = 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase165_r52_r16_web_citation_gate.py' = 'd1138c0450f234b6da761902ed7358b6038a19c8'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'test_phase165_r55_nk_only_goal.py' = '9def7480a529ab5f6c2e344866016cf36330a409'
}

foreach ($RelativePath in $ExpectedBlobs.Keys) {
    $Actual = (Invoke-CheckedGit -Arguments @('hash-object', '--', $RelativePath)).Trim()
    if ($Actual -ne $ExpectedBlobs[$RelativePath]) {
        throw "Source/content guard failed: $RelativePath"
    }
}
$R1AuditBlob = (Invoke-CheckedGit -Arguments @('rev-parse', 'HEAD:phase174_r1_goal_audit/audit.py')).Trim()
if ($R1AuditBlob -ne 'dfd80cc44111c8df9cebd6398b21223f5d831e80') {
    throw 'Committed R1 audit content differs from the reviewed version'
}

& git merge-base --is-ancestor $R1BaselineHead $LocalHead
if ($LASTEXITCODE -ne 0) {
    throw 'The recorded Phase 174 R1 baseline is not an ancestor of the current HEAD'
}
Write-Output 'PHASE174_R2_HEAD_LINEAGE=PASS'
Write-Output 'PHASE174_R2_R1_BASELINE_PROVENANCE=PASS'
Write-Output 'PHASE174_R2_SOURCE_GUARD=PASS'

$StatusBefore = @(Invoke-CheckedGit -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexBefore = @(Invoke-CheckedGit -Arguments @('ls-files', '--stage')) -join "`n"

if ($DryRun) {
    Write-Output 'PHASE174_R2_DRY_RUN=PASS'
    Write-Output 'PHASE174_R2_NO_CODE_CHANGES=True'
    exit 0
}

$OldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    & python -B -m phase174_r2_source_math_audit.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R2 source-frontier audit failed'
    }

    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r2_source_math_audit/tests/test_audit.py `
        phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
        phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R2 focused pytest failed'
    }
    Write-Output 'PHASE174_R2_FOCUSED_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoByteCode
    $env:PYTHONIOENCODING = $OldPythonIO
}

$StatusAfter = @(Invoke-CheckedGit -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexAfter = @(Invoke-CheckedGit -Arguments @('ls-files', '--stage')) -join "`n"

if ($StatusBefore -cne $StatusAfter) {
    throw 'Git worktree changed during R2 audit'
}
if ($IndexBefore -cne $IndexAfter) {
    throw 'Git index changed during R2 audit'
}
Write-Output 'PHASE174_R2_WORKTREE_PRESERVED=PASS'
Write-Output 'PHASE174_R2_GIT_INDEX_PRESERVED=PASS'
Write-Output 'PHASE174_R2_GATE=PASS'
