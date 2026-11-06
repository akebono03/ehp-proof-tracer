param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each group gets a separate Python process. Several previous Phase
    # packages contain test_audit.py or test_rule.py with the same basename.
    # Prepend mode is required for old module/directory naming collisions.
    $R5Tests = @(
        '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
        '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
    )
    $R4Tests = @(
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
    )
    $R3Tests = @(
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
    )
    $MathTests = @(
        '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
        '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
        '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
    )
    $Groups = @(
        @{ Name = 'R5'; Paths = $R5Tests },
        @{ Name = 'R4'; Paths = $R4Tests },
        @{ Name = 'R3'; Paths = $R3Tests },
        @{ Name = 'MATH_REGRESSION'; Paths = $MathTests }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Focused test file missing: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R5_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R5_PYTEST_GROUP=$($Group.Name)"
        $TestPaths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @TestPaths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R5 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R5_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r5_zero_image_hopf_injective.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r5_zero_image_hopf_injective.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R5 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
