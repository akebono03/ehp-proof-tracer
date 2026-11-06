param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$Backup = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r16\phase165_r52_r9_shared_math.original.py'
$Target = Join-Path $RepoRoot 'phase165_r52_r9_shared_math.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "R16 git fetch failed" }

    & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R16 source-first preflight failed" }
    & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R16 guarded patch dry-run failed" }

    $Groups = @(
        @{ Name = 'R16_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_patch.py',
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_audit.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) },
        @{ Name = 'R14_PUBLIC_SOURCE'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        ) },
        @{ Name = 'EHP_EXACTNESS'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "R16 focused test missing: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R16_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R16 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R16_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R16_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.patch
        if ($LASTEXITCODE -ne 0) { throw 'R16 guarded apply failed' }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R16 public provider integration failed' }
        & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.audit
        if ($LASTEXITCODE -ne 0) { throw 'R16 public source-first audit failed' }
    }
    Write-Output '(END)'
}
catch {
    if ($PatchAttempted -and (Test-Path -LiteralPath $Backup)) {
        $Changed = @(git diff --name-only)
        if ($Changed -contains 'phase165_r52_r9_shared_math.py') {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Output 'PHASE174_R3R7R16_ROLLBACK=RESTORED_REVIEWED_SOURCE'
        }
    }
    throw
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
