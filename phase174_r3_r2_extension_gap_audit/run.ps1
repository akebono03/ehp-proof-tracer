param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$AllowedHeads = @(
    '1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9',
    '8687759569d7820e26c53aac6f38aedb8ea04f0b'
)
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

function Checked-Git {
    param([string[]]$Arguments)
    $Output = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('git failed: git ' + ($Arguments -join ' '))
    }
    return $Output
}

$Branch = (Checked-Git -Arguments @('branch', '--show-current')).Trim()
$LocalHead = (Checked-Git -Arguments @('rev-parse', 'HEAD')).Trim()
$RemoteRows = @(Checked-Git -Arguments @('ls-remote', 'origin', 'refs/heads/develop'))
if ($RemoteRows.Count -ne 1) {
    throw 'Cannot resolve origin/develop uniquely'
}
$RemoteHead = (($RemoteRows[0].Trim()) -split '\s+')[0]
Write-Output "PHASE174_R3R2_BRANCH=$Branch"
Write-Output "PHASE174_R3R2_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R3R2_REMOTE_HEAD=$RemoteHead"
if ($Branch -ne 'develop' -or $LocalHead -notin $AllowedHeads -or $RemoteHead -notin $AllowedHeads) {
    throw 'An unreviewed local or GitHub HEAD was encountered'
}

$Blobs = [ordered]@{
    'phase174_r3_r1_frontier_audit/audit.py' = 'ccfc5b17b85dab1650beda0f3cfe84ca6a676846'
    'phase174_r3_r1_frontier_audit/tests/test_audit.py' = 'd9d395fb85a224a8fbb53ff426a017a1e308da34'
    'phase165_r12_r2_quotient_rules.py' = '2b3e8e0449382e9245ee22f08501e9cede0a5b59'
    'phase165_r12_r5_structure_bridge.py' = '4067bf1b2cc4114359c2d1a104d17ba874122060'
    'phase165_r12_r24_web_search_connection.py' = '71d0c6c365a46e833a2bfe304c771d2e010178ca'
    'phase165_r12_r26_map_candidates.py' = 'b57e4efe80d70cf67906882cbc93c047311e10e9'
    'phase165_r12_r17_quotient_chain.py' = 'a2cf9f8b1398a36ee5fda91f58b20b99f8646ff6'
    'phase165_r12_r31_proven_cyclic_reuse.py' = 'a663510cd5aa59e6dee5cae9c981e04e86f896ab'
    'phase165_r52_r9_shared_math.py' = 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'sources/toda/Toda_04_2.tex' = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7'
    'sources/toda/Toda_05_2.tex' = '579661138928499ba04a51327f686d9b971b5314'
}
foreach ($Path in $Blobs.Keys) {
    $Actual = (Checked-Git -Arguments @('hash-object', '--', $Path)).Trim()
    if ($Actual -ne $Blobs[$Path]) {
        throw "Unexpected source content: $Path"
    }
}
Write-Output 'PHASE174_R3R2_SOURCE_GUARD=PASS'

$Prior = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r1\audit.json'
if (-not (Test-Path -LiteralPath $Prior)) {
    throw 'R3-R1 source report missing'
}
$PriorData = Get-Content -LiteralPath $Prior -Raw -Encoding UTF8 | ConvertFrom-Json
if ($PriorData.phase -ne '174-R3-R1' -or $PriorData.local_head -ne '1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9') {
    throw 'Previous report provenance mismatch'
}
Write-Output 'PHASE174_R3R2_PRIOR_PROVENANCE_GUARD=PASS'

$StatusBefore = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexBefore = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"

if ($DryRun) {
    Write-Output 'PHASE174_R3R2_DRY_RUN=PASS'
    Write-Output 'PHASE174_R3R2_NO_CODE_CHANGES=True'
    exit 0
}

$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    & python -B -m phase174_r3_r2_extension_gap_audit.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R2 mathematical obligation audit failed'
    }
    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r3_r2_extension_gap_audit/tests/test_audit.py `
        phase174_r3_r1_frontier_audit/tests/test_audit.py `
        phase174_r2_source_math_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R2 focused pytest failed'
    }
    Write-Output 'PHASE174_R3R2_FOCUSED_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    $env:PYTHONIOENCODING = $OldPythonIO
}

$StatusAfter = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexAfter = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($StatusBefore -cne $StatusAfter -or $IndexBefore -cne $IndexAfter) {
    throw 'Git index or worktree changed during audit'
}
Write-Output 'PHASE174_R3R2_GIT_STATE_PRESERVED=PASS'
Write-Output 'PHASE174_R3R2_GATE=PASS'
