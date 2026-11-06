param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PriorPythonPath = $env:PYTHONPATH
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # A separate pytest process per Phase avoids test_audit.py basename collisions.
    # Prepend mode avoids the repository's file/directory import-name collisions.
    $Groups = @(
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing focused test file: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R9_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R9_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R9 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R9_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r9_composition_associativity.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r9_composition_associativity.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R9 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PriorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    Pop-Location
}
