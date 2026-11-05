param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$AllowedHeads = @(
    '8687759569d7820e26c53aac6f38aedb8ea04f0b',
    'ae2fdbffc4ce15b4141933dc9e529ff450265be1'
)
$R3R2BaselineHead = '8687759569d7820e26c53aac6f38aedb8ea04f0b'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

function Checked-Git {
    param([string[]]$Arguments)
    $Output = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('Git failed: ' + ($Arguments -join ' '))
    }
    return $Output
}

$Branch = (Checked-Git -Arguments @('branch', '--show-current')).Trim()
$LocalHead = (Checked-Git -Arguments @('rev-parse', 'HEAD')).Trim()
$Remote = @(Checked-Git -Arguments @('ls-remote', 'origin', 'refs/heads/develop'))
if ($Remote.Count -ne 1) {
    throw 'Cannot read exactly one remote develop HEAD'
}
$RemoteHead = (($Remote[0].Trim()) -split '\s+')[0]
Write-Output "PHASE174_R3R3_BRANCH=$Branch"
Write-Output "PHASE174_R3R3_LOCAL_HEAD=$LocalHead"
Write-Output "PHASE174_R3R3_REMOTE_HEAD=$RemoteHead"
if ($Branch -ne 'develop' -or $LocalHead -notin $AllowedHeads -or $RemoteHead -notin $AllowedHeads) {
    throw 'An unreviewed GitHub/local HEAD was encountered; inspect source before continuing'
}
& git merge-base --is-ancestor $LocalHead $RemoteHead
if ($LASTEXITCODE -ne 0) {
    throw 'Local develop is not an ancestor of the reviewed remote develop'
}

$ExpectedBlobs = [ordered]@{
    'sources/toda/Toda_04_2.tex' = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7'
    'sources/toda/Toda_05_2.tex' = '579661138928499ba04a51327f686d9b971b5314'
    'phase165_r52_r9_shared_math.py' = 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    'phase165_r55_nk_only_goal.py' = '9aa232c8f98a7a75f27266044224eddfa98c5e04'
    'phase165_r3_recursive_search.py' = '06009bfcf57f99cac58c229d99c53f16324692d0'
    'phase165_r52_r16_web_citation_gate.py' = 'd1138c0450f234b6da761902ed7358b6038a19c8'
    'phase165_r12_r11_prop42_unified.py' = '79752ec035244677ff6a54debff312e87a76fbf2'
    'phase165_r14_r11_delta_zero.py' = '0bc61ede969bb3ddf43cdd43e9ef7a557c4dac61'
    'phase165_r14_r6_generic_iso.py' = '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7'
    'phase169_r4b_prop44_injectivity/rule.py' = 'aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b'
    'phase165_r52_r27_r5_literature.py' = 'c9bfe2788f4cf043db6dada98a437afea6accf75'
    'phase171_r2j_r3_ehp_exactness/source.py' = 'f87ce6dc8278661a56bc0024c3a06645c509934d'
    'phase165_r14_r11_delta_zero/test_phase165_r14_r11_delta_zero.py' = '76c9069a856f7695f670f68a7853afc91e280a3d'
    'phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py' = '9bcec30bb228126e1e7670a221d447a524219d0c'
    'phase174_r3_r2_extension_gap_audit/audit.py' = 'b20a9f6b23d85fab2f0e634fa4cca0ed8d58dca2'
    'phase174_r3_r3_injective_delta_zero/rule.py' = '39fcc732a3ec50e137ce4279254a4ad223d27008'
    'phase174_r3_r3_injective_delta_zero/audit.py' = 'd89a74565311b0427396c809f4b876e958529cfa'
    'phase174_r3_r3_injective_delta_zero/tests/test_rule.py' = '40894d557458ddc03004e2191bbbf14c3d01a098'
}
foreach ($Filename in $ExpectedBlobs.Keys) {
    $Actual = (Checked-Git -Arguments @('hash-object', '--', $Filename)).Trim()
    if ($Actual -ne $ExpectedBlobs[$Filename]) {
        throw "A reviewed source or test has changed: $Filename"
    }
}
Write-Output 'PHASE174_R3R3_SOURCE_GUARD=PASS'

$PriorReport = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r2\audit.json'
if (-not (Test-Path -LiteralPath $PriorReport)) {
    throw 'The completed R3-R2 audit evidence is absent'
}
$Prior = Get-Content -LiteralPath $PriorReport -Raw -Encoding UTF8 | ConvertFrom-Json
if ($Prior.phase -ne '174-R3-R2' -or $Prior.local_head -ne $R3R2BaselineHead -or $Prior.new_proof_steps -ne 0) {
    throw 'The existing R3-R2 report has unreviewed provenance'
}
Write-Output 'PHASE174_R3R3_R3R2_PROVENANCE_GUARD=PASS'

$StatusBefore = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexBefore = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($DryRun) {
    Write-Output 'PHASE174_R3R3_DRY_RUN=PASS'
    Write-Output 'PHASE174_R3R3_NO_FILES_CHANGED=True'
    exit 0
}

$PriorNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$PriorEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'

    & python -B -m phase174_r3_r3_injective_delta_zero.audit
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R3 Delta-zero capability trial failed'
    }

    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r3_r3_injective_delta_zero/tests/test_rule.py `
        phase165_r14_r11_delta_zero/test_phase165_r14_r11_delta_zero.py `
        phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py `
        phase174_r3_r2_extension_gap_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) {
        throw 'R3-R3 focused tests failed'
    }
    Write-Output 'PHASE174_R3R3_FOCUSED_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoByteCode
    $env:PYTHONIOENCODING = $PriorEncoding
}

$StatusAfter = @(Checked-Git -Arguments @('status', '--porcelain=v1', '--untracked-files=all')) -join "`n"
$IndexAfter = @(Checked-Git -Arguments @('ls-files', '--stage')) -join "`n"
if ($StatusBefore -cne $StatusAfter -or $IndexBefore -cne $IndexAfter) {
    throw 'The Git index or worktree changed during the R3-R3 trial'
}
Write-Output 'PHASE174_R3R3_GIT_STATE_PRESERVED=PASS'
Write-Output 'PHASE174_R3R3_GATE=PASS'
