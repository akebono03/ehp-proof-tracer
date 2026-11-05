param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Both commits have been reviewed. The second only adds R2 audit files.
$AllowedHeads = @(
    '3558d713fd7939ded656f2458aacc62d71c7e0b3',
    '1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9'
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
    throw 'Cannot uniquely inspect remote develop'
}
$RemoteHead = (($RemoteRows[0].Trim()) -split '\s+')[0]
Write-Output "PHASE174_R3R1_BRANCH=$Branch"
Write-Output "PHASE174_R3R1_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R3R1_REMOTE_HEAD=$RemoteHead"
if ($Branch -ne 'develop' -or $LocalHead -notin $AllowedHeads -or $RemoteHead -notin $AllowedHeads) {
    throw 'A non-reviewed GitHub/local HEAD was encountered'
}

$Blobs = [ordered]@{
    'sources/toda/Toda_04_2.tex' = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7'
    'sources/toda/Toda_05_2.tex' = '579661138928499ba04a51327f686d9b971b5314'
    'phase165_r52_r9_shared_math.py' = 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'phase165_r52_r16_web_citation_gate.py' = 'd1138c0450f234b6da761902ed7358b6038a19c8'
    'phase165_r12_r11_prop42_unified.py' = '79752ec035244677ff6a54debff312e87a76fbf2'
    'phase166_r3t_goal_source_binding/goal_source.py' = 'e13a07bbc0b6494b0c3c9b891784fe7378448756'
    'phase169_r10e2_unpositioned_citation/source_first.py' = 'b91b97a74d65b843fa8f9c19ffd082f684e461a7'
    'phase174_r2_source_math_audit/audit.py' = 'e5995c4c5f97b220557dba9bc5935501f1e64141'
    'phase174_r2_source_math_audit/tests/test_audit.py' = '62b3b374475e77c14cd0866d53870313d0cc2d57'
    'test_phase165_r55_nk_only_goal.py' = '9def7480a529ab5f6c2e344866016cf36330a409'
    'phase174_r3_r1_frontier_audit/audit.py' = 'ccfc5b17b85dab1650beda0f3cfe84ca6a676846'
    'phase174_r3_r1_frontier_audit/tests/test_audit.py' = 'd9d395fb85a224a8fbb53ff426a017a1e308da34'
}
foreach ($Filename in $Blobs.Keys) {
    $ActualSha = (Checked-Git -Arguments @('hash-object', '--', $Filename)).Trim()
    if ($ActualSha -ne $Blobs[$Filename]) {
        throw "A reviewed file has changed: $Filename"
    }
}
Write-Output 'PHASE174_R3R1_SOURCE_GUARD=PASS'

$R2Json = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r2\audit.json'
if (-not (Test-Path -LiteralPath $R2Json)) {
    throw 'The successful R2 audit report is missing'
}
$R2Report = Get-Content -LiteralPath $R2Json -Raw -Encoding UTF8 | ConvertFrom-Json
if ($R2Report.head -ne '3558d713fd7939ded656f2458aacc62d71c7e0b3') {
    throw 'The original R2 evidence HEAD is not the reviewed one'
}
Write-Output 'PHASE174_R3R1_R2_PROVENANCE_GUARD=PASS'

$StatusBefore = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexBefore = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($DryRun) {
    Write-Output 'PHASE174_R3R1_DRY_RUN=PASS'
    Write-Output 'PHASE174_R3R1_NO_CODE_CHANGES=True'
    exit 0
}

$OldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    & python -B -m phase174_r3_r1_frontier_audit.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R1 live two-hop frontier audit failed'
    }
    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r3_r1_frontier_audit/tests/test_audit.py `
        phase174_r2_source_math_audit/tests/test_audit.py `
        test_phase165_r55_nk_only_goal.py
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R1 focused pytest failed'
    }
    Write-Output 'PHASE174_R3R1_FOCUSED_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoByteCode
    $env:PYTHONIOENCODING = $OldPythonIO
}

$StatusAfter = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexAfter = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($StatusBefore -cne $StatusAfter -or $IndexBefore -cne $IndexAfter) {
    throw 'Git worktree or index changed during R3-R1'
}
Write-Output 'PHASE174_R3R1_GIT_STATE_PRESERVED=PASS'
Write-Output 'PHASE174_R3R1_GATE=PASS'
