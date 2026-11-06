param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each phase group runs in a separate pytest process: many legacy tests
    # share test_audit.py/test_rule.py basenames. Keep prepend import mode.
    $Groups = @(
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
                throw "Focused test file missing: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R7_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R7_PYTEST_GROUP=$($Group.Name)"
        $TestPaths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @TestPaths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R7 $($Group.Name) focused pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R7_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r7_composite_zero_audit.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r7_composite_zero_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R7 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
