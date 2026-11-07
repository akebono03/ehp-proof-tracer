param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Fetch only; never pull, checkout, reset, stash, or touch tracked sources.
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "Unable to fetch reviewed develop history" }
    & python -B -m phase174_r3_r7_r15_chain_frontier_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R15 source-first DryRun failed" }

    $FocusedGroups = @(
        @{ Name = 'R15_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r15_chain_frontier_audit\tests\test_contract.py'
        ) },
        @{ Name = 'R14_PUBLIC'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        ) },
        @{ Name = 'R12_SPECIALIZATION'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py'
        ) },
        @{ Name = 'R6_CYCLIC'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py'
        ) },
        @{ Name = 'R7_COMPOSITE_ZERO'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py'
        ) },
        @{ Name = 'R9_ASSOCIATIVITY'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py'
        ) }
    )
    foreach ($Group in $FocusedGroups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) { throw "Missing focused test: $TestPath" }
        }
        Write-Output "PHASE174_R3R7R15_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R15_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R15_GATE=PASS_PREFLIGHT'
    }
    else {
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r15_chain_frontier_audit\tests\test_public_frontier.py'
        if ($LASTEXITCODE -ne 0) { throw 'R15 public frontier integration pytest failed' }
        & python -B -m phase174_r3_r7_r15_chain_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R15 read-only proof-frontier audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
