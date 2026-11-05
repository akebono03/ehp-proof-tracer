param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Baseline = 'cb85913905b2f7452bda2a2c4428e6fe5a3a793a'
$ExpectedHead = '3558d713fd7939ded656f2458aacc62d71c7e0b3'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root

function GitChecked {
    param([string[]]$Arguments)
    $Result = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('git command failed: git ' + ($Arguments -join ' '))
    }
    return $Result
}

$Branch = (GitChecked -Arguments @('branch', '--show-current')).Trim()
$Head = (GitChecked -Arguments @('rev-parse', 'HEAD')).Trim()
$Remote = @(GitChecked -Arguments @('ls-remote', 'origin', 'refs/heads/develop'))
if ($Remote.Count -ne 1) { throw 'Cannot resolve remote develop' }
$RemoteHead = (($Remote[0].Trim()) -split '\s+')[0]
if ($Branch -ne 'develop' -or $Head -ne $ExpectedHead -or $RemoteHead -ne $ExpectedHead) {
    throw 'HEAD guard failed; do not apply this correction without re-reviewing GitHub develop'
}
& git merge-base --is-ancestor $Baseline $Head
if ($LASTEXITCODE -ne 0) { throw 'The R1 baseline is not an ancestor of the reviewed HEAD' }

$ReviewedFiles = @(
    @{ Path = 'sources/toda/Toda_04_2.tex'; Sha = '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7' },
    @{ Path = 'sources/toda/Toda_05_2.tex'; Sha = '579661138928499ba04a51327f686d9b971b5314' },
    @{ Path = 'phase165_r52_r9_shared_math.py'; Sha = 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336' },
    @{ Path = 'phase165_r55_nk_only_goal.py'; Sha = '9aa232c8f98a7a75f27266044224eddfa98c5e04' },
    @{ Path = 'phase165_r52_r16_web_citation_gate.py'; Sha = 'd1138c0450f234b6da761902ed7358b6038a19c8' },
    @{ Path = 'phase165_r3_recursive_search.py'; Sha = '06009bfcf57f99cac58c229d99c53f16324692d0' },
    @{ Path = 'test_phase165_r55_nk_only_goal.py'; Sha = '9def7480a529ab5f6c2e344866016cf36330a409' },
    @{ Path = 'phase174_r1_goal_audit/audit.py'; Sha = 'dfd80cc44111c8df9cebd6398b21223f5d831e80' }
)
foreach ($Item in $ReviewedFiles) {
    $Sha = (GitChecked -Arguments @('hash-object', '--', $Item.Path)).Trim()
    if ($Sha -ne $Item.Sha) { throw ('Source guard failed: ' + $Item.Path) }
}

$Files = @(
    @{ Path = 'audit.py'; Original = '7cc607da1757f0cd9617d838916bfd803d08d6db'; Replacement = 'e5995c4c5f97b220557dba9bc5935501f1e64141' },
    @{ Path = 'run.ps1'; Original = '4675d181100e21aba77eda623da41517450b4161'; Replacement = '3a0ec748dbb583daa191c97aa6a7f740516c7930' }
)
$OverwriteNeeded = @()
foreach ($File in $Files) {
    $Destination = Join-Path $Root (Join-Path 'phase174_r2_source_math_audit' $File.Path)
    $Replacement = Join-Path $PSScriptRoot (Join-Path 'full_replacements\phase174_r2_source_math_audit' $File.Path)
    if (-not (Test-Path -LiteralPath $Destination)) { throw ('Missing original R2 file: ' + $File.Path) }
    if (-not (Test-Path -LiteralPath $Replacement)) { throw ('Missing replacement R2 file: ' + $File.Path) }
    $Actual = (GitChecked -Arguments @('hash-object', '--', $Destination)).Trim()
    $Candidate = (GitChecked -Arguments @('hash-object', '--', $Replacement)).Trim()
    if ($Candidate -ne $File.Replacement) { throw ('Replacement file SHA mismatch: ' + $File.Path) }
    if ($Actual -ne $File.Original -and $Actual -ne $File.Replacement) {
        throw ('Refusing to overwrite locally edited file: ' + $File.Path)
    }
    if ($Actual -eq $File.Original) { $OverwriteNeeded += @{ From = $Replacement; To = $Destination } }
}

Write-Output "PHASE174_R2R1_LOCAL_HEAD=$Head"
Write-Output "PHASE174_R2R1_REMOTE_HEAD=$RemoteHead"
Write-Output 'PHASE174_R2R1_HEAD_LINEAGE=PASS'
Write-Output 'PHASE174_R2R1_SOURCE_GUARD=PASS'
Write-Output 'PHASE174_R2R1_REPLACEMENT_CONTENT_GUARD=PASS'
Write-Output ("PHASE174_R2R1_ALREADY_INSTALLED=" + ($OverwriteNeeded.Count -eq 0))
if ($DryRun) {
    Write-Output 'PHASE174_R2R1_DRY_RUN=PASS'
    Write-Output 'PHASE174_R2R1_NO_FILES_CHANGED=True'
    exit 0
}

$IndexBefore = @(GitChecked -Arguments @('ls-files', '--stage')) -join "`n"
foreach ($Item in $OverwriteNeeded) {
    Copy-Item -LiteralPath $Item.From -Destination $Item.To
}
foreach ($File in $Files) {
    $Installed = (GitChecked -Arguments @('hash-object', '--', (Join-Path $Root (Join-Path 'phase174_r2_source_math_audit' $File.Path)))).Trim()
    if ($Installed -ne $File.Replacement) { throw ('Installed R2 file differs: ' + $File.Path) }
}
Write-Output 'PHASE174_R2R1_REPLACEMENT_INSTALLED=PASS'

$OldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
$OldPythonIO = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    & python -B -m pytest -q -p no:cacheprovider `
        phase174_r2r1_head_lineage_fix/tests/test_head_lineage.py
    if ($LASTEXITCODE -ne 0) { throw 'R2R1 focused lineage pytest failed' }
    Write-Output 'PHASE174_R2R1_LINEAGE_PYTEST=PASS'
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoByteCode
    $env:PYTHONIOENCODING = $OldPythonIO
}

& powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r2_source_math_audit\run.ps1' -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R2 DryRun failed after lineage correction' }
& powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r2_source_math_audit\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'R2 audit or its focused regression failed' }

$IndexAfter = @(GitChecked -Arguments @('ls-files', '--stage')) -join "`n"
if ($IndexBefore -cne $IndexAfter) { throw 'Git index changed during R2R1 correction' }
Write-Output 'PHASE174_R2R1_GIT_INDEX_PRESERVED=PASS'
Write-Output 'PHASE174_R2R1_GATE=PASS'
