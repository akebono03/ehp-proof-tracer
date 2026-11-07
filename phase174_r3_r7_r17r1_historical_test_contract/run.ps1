param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$AttemptedWebPatch = $false
$AttemptedTestPatch = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R17R1 Git fetch failed' }

    # All source gates run before any tracked file is modified.
    & python -B -m phase174_r3_r7_r17r1_historical_test_contract.audit
    if ($LASTEXITCODE -ne 0) { throw 'R17R1 source guard failed' }
    & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Historical contract patch preflight failed' }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Original R17 source guard failed' }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Original R17 formatter patch preflight failed' }

    # Targeted tests only: the obsolete historical parametrization is fixed
    # in this package after the original R17 audit, not silently skipped.
    $Groups = @(
        @{ Name = 'R17R1_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17r1_historical_test_contract\tests\test_patch.py'
        ) },
        @{ Name = 'R17_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_patch.py',
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_audit.py'
        ) },
        @{ Name = 'R16_ROOT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing reviewed test: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R17R1_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R17R1 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R17R1_PREFLIGHT_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R17R1_STALE_HISTORICAL_CASE=DOCUMENTED_NOT_EXECUTED_BEFORE_CORRECTION'
        Write-Output 'PHASE174_R3R7R17R1_GATE=PASS_PREFLIGHT'
    }
    else {
        # 1. Complete the originally intended R17 formatting patch while its
        # original strict source guard still sees an unchanged historical test.
        $AttemptedWebPatch = $true
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch
        if ($LASTEXITCODE -ne 0) { throw 'R17 original formatting patch failed' }
        Write-Output 'PHASE174_R3R7R17R1_PYTEST_GROUP=R17_PUBLIC'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'Original R17 public display test failed' }
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit
        if ($LASTEXITCODE -ne 0) { throw 'Original R17 public audit failed' }

        # 2. Update the obsolete Phase 173 test contract. Never skip the
        # completed pi_8^5 case: it now has an explicit completed-proof test.
        $AttemptedTestPatch = $true
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 historical test correction failed' }
        Write-Output 'PHASE174_R3R7R17R1_PYTEST_GROUP=PHASE173_TYPED_DISPLAY_CORRECTED'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        if ($LASTEXITCODE -ne 0) { throw 'Corrected historical typed display tests failed' }
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.audit --applied
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 final source-first gate failed' }
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_.ToString()
    if ($AttemptedTestPatch) {
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --rollback
        if ($LASTEXITCODE -ne 0) { Write-Warning 'Historical test rollback needs manual review' }
    }
    if ($AttemptedWebPatch) {
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.rollback
        if ($LASTEXITCODE -ne 0) { Write-Warning 'Common formatter rollback needs manual review' }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
