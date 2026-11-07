param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$Backup = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r17\web_group_proof_common.original.py'
$Target = Join-Path $RepoRoot 'web_group_proof_common.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Fetch, but never pull/reset/stash/checkout user files.
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "R17 Git fetch failed: $LASTEXITCODE" }

    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R17 source guard/preflight failed: $LASTEXITCODE" }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R17 formatting patch dry-run failed: $LASTEXITCODE" }

    $Groups = @(
        @{ Name = 'R17_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_patch.py',
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_audit.py'
        ) },
        @{ Name = 'R16_ROOT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) },
        @{ Name = 'PHASE173_TYPED_DISPLAY'; Paths = @(
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "R17 missing focused test: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R17_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R17 focused test failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R17_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R17_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch
        if ($LASTEXITCODE -ne 0) { throw 'R17 guarded formatting patch failed' }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R17 public typed-map display regression failed' }
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit
        if ($LASTEXITCODE -ne 0) { throw 'R17 public typed-map audit failed' }
    }
    Write-Output '(END)'
}
catch {
    if ($PatchAttempted -and (Test-Path -LiteralPath $Backup)) {
        $Modified = @(git diff --name-only)
        if ($Modified -contains 'web_group_proof_common.py') {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Output 'PHASE174_R3R7R17_ROLLBACK=COMMON_RENDERER_RESTORED'
        }
    }
    throw
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
