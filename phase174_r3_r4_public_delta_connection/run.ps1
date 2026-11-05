param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedHead = 'ae2fdbffc4ce15b4141933dc9e529ff450265be1'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

function Checked-Git {
    param([string[]]$Arguments)
    $Output = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('Git failed: git ' + ($Arguments -join ' '))
    }
    return $Output
}

$Branch = (Checked-Git -Arguments @('branch', '--show-current')).Trim()
$LocalHead = (Checked-Git -Arguments @('rev-parse', 'HEAD')).Trim()
$Remote = @(Checked-Git -Arguments @('ls-remote', 'origin', 'refs/heads/develop'))
if ($Remote.Count -ne 1) {
    throw 'Cannot uniquely verify origin/develop'
}
$RemoteHead = (($Remote[0].Trim()) -split '\s+')[0]
Write-Output "PHASE174_R3R4_BRANCH=$Branch"
Write-Output "PHASE174_R3R4_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R3R4_REMOTE_HEAD=$RemoteHead"
if ($Branch -ne 'develop' -or $LocalHead -ne $RemoteHead) {
    throw 'Local and remote develop must agree on the same reviewed lineage'
}
& git merge-base --is-ancestor $ExpectedHead $LocalHead
if ($LASTEXITCODE -ne 0) {
    throw 'Current develop is not a descendant of the reviewed baseline'
}
$ChangedSinceBaseline = @(Checked-Git -Arguments @('diff', '--name-only', "$ExpectedHead..$LocalHead"))
foreach ($ChangedFile in $ChangedSinceBaseline) {
    if ($ChangedFile -notmatch '^phase174_r3_r3_injective_delta_zero/') {
        throw "Unreviewed change after baseline: $ChangedFile"
    }
}
Write-Output 'PHASE174_R3R4_HEAD_LINEAGE=PASS'

$ExpectedBlobs = [ordered]@{
    'sources/toda/Toda_04_2.tex' = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'phase165_r12_r11_prop42_unified.py' = '79752ec035244677ff6a54debff312e87a76fbf2'
    'phase165_r52_r16_web_citation_gate.py' = 'd1138c0450f234b6da761902ed7358b6038a19c8'
    'phase169_r4b_prop44_injectivity/rule.py' = 'aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b'
    'phase174_r3_r3_injective_delta_zero/rule.py' = '39fcc732a3ec50e137ce4279254a4ad223d27008'
    'phase174_r3_r3_injective_delta_zero/audit.py' = 'd89a74565311b0427396c809f4b876e958529cfa'
    'phase174_r3_r3_injective_delta_zero/tests/test_rule.py' = '40894d557458ddc03004e2191bbbf14c3d01a098'
}
foreach ($Filename in $ExpectedBlobs.Keys) {
    $Actual = (Checked-Git -Arguments @('hash-object', '--', $Filename)).Trim()
    if ($Actual -ne $ExpectedBlobs[$Filename]) {
        throw "R3-R4 source guard failed: $Filename"
    }
}
Write-Output 'PHASE174_R3R4_DEPENDENCY_SOURCE_GUARD=PASS'

$PriorReportPath = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r3\audit.json'
if (-not (Test-Path -LiteralPath $PriorReportPath)) {
    throw 'Reviewed R3-R3 audit report not found'
}
$PriorReport = Get-Content -LiteralPath $PriorReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($PriorReport.local_head -ne $ExpectedHead -or $PriorReport.phase -ne '174-R3-R3' -or
    $PriorReport.typed_inference_trial.verified_in_memory_delta_zero -ne $true) {
    throw 'Unreviewed R3-R3 evidence: verified Delta-zero premise absent'
}
Write-Output 'PHASE174_R3R4_R3R3_PROVENANCE_GUARD=PASS'

$StagedBefore = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
$StatusBefore = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$OldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'

    if ($DryRun) {
        & python -B -m phase174_r3_r4_public_delta_connection.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R4 DryRun failed' }
        $StatusAfterDryRun = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
        $StagedAfterDryRun = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
        if ($StatusAfterDryRun -cne $StatusBefore -or $StagedAfterDryRun -cne $StagedBefore) {
            throw 'DryRun unexpectedly changed a Git file'
        }
        Write-Output 'PHASE174_R3R4_DRY_RUN_GATE=PASS'
        exit 0
    }

    & python -B -m phase174_r3_r4_public_delta_connection.patch
    if ($LASTEXITCODE -ne 0) { throw 'R3-R4 reviewed source replacement failed' }

    & python -B -m phase174_r3_r4_public_delta_connection.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-R4 public provider Delta inference failed' }

    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r3_r4_public_delta_connection/tests/test_connection.py `
        phase174_r3_r3_injective_delta_zero/tests/test_rule.py `
        phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py `
        phase165_r14_r11_delta_zero/test_phase165_r14_r11_delta_zero.py
    if ($LASTEXITCODE -ne 0) { throw 'R3-R4 focused tests failed' }
    Write-Output 'PHASE174_R3R4_FOCUSED_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoByteCode
    $env:PYTHONIOENCODING = $OldPythonIO
}

$StagedAfter = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($StagedAfter -cne $StagedBefore) {
    throw 'Git index was modified'
}
$StatusAfter = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$StatusOthersBefore = @(
    $StatusBefore -split "`n" | Where-Object {
        $_ -and $_ -notmatch '^.. phase165_r52_r9_shared_math\.py$'
    }
) -join "`n"
$StatusOthersAfter = @(
    $StatusAfter -split "`n" | Where-Object {
        $_ -and $_ -notmatch '^.. phase165_r52_r9_shared_math\.py$'
    }
) -join "`n"
if ($StatusOthersBefore -cne $StatusOthersAfter) {
    throw 'Unexpected unrelated Git worktree modification'
}
$ModifiedSource = @(Checked-Git -Arguments @('diff', '--name-only', '--', 'phase165_r52_r9_shared_math.py'))
if ($ModifiedSource.Count -ne 1 -or $ModifiedSource[0] -ne 'phase165_r52_r9_shared_math.py') {
    throw 'Expected exactly one reviewed production source modification'
}
Write-Output 'PHASE174_R3R4_GIT_INDEX_PRESERVED=PASS'
Write-Output 'PHASE174_R3R4_GATE=PASS'
