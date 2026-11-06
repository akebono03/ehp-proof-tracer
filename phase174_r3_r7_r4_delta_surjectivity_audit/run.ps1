param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir '..')).Path
Push-Location $RepoRoot
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # The Phase R4 and Phase R3 test_audit.py files have the same basename.
    # Run each test group in a separate Python process. Keep prepend mode
    # because importlib mode conflicts with existing module/package names.
    $R4Tests = @(
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
    )
    $RegressionTests = @(
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py',
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
        '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
        '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py'
    )
    $FocusedTests = @($R4Tests + $RegressionTests)
    foreach ($TestPath in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestPath)) {
            throw "Focused pytest file missing: $TestPath"
        }
    }

    Write-Output 'PHASE174_R3R7R4_FOCUSED_PYTEST_START'
    Write-Output 'PHASE174_R3R7R4_PYTEST_GROUP=R4'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @R4Tests
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 own pytest failed: $LASTEXITCODE"
    }
    Write-Output 'PHASE174_R3R7R4_PYTEST_GROUP=REGRESSION'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @RegressionTests
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 regression pytest failed: $LASTEXITCODE"
    }
    Write-Output 'PHASE174_R3R7R4_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B '.\phase174_r3_r7_r4_delta_surjectivity_audit\audit.py' --dry-run
    }
    else {
        & python -B '.\phase174_r3_r7_r4_delta_surjectivity_audit\audit.py'
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R4 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
