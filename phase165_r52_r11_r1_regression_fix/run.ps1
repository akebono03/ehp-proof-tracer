$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $projectRoot

python ".\phase165_r52_r11_r1_regression_fix\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$requiredTests = @(
    "test_phase165_r52_r11_common_renderer.py",
    "test_phase165_r52_r8_show_proof_route.py"
)
foreach ($test in $requiredTests) {
    if (-not (Test-Path -LiteralPath $test -PathType Leaf)) {
        throw "Required test missing: $test"
    }
}

$optionalTests = @(
    "test_phase165_r52_partial_proof.py",
    "test_phase165_r52_r9_shared_math.py",
    "test_phase165_r52_r10_readable_partial.py"
)
$selectedTests = @($requiredTests)
foreach ($test in $optionalTests) {
    if (Test-Path -LiteralPath $test -PathType Leaf) {
        $selectedTests += $test
    }
}

Write-Host "R52-R11 regression tests: $($selectedTests -join ', ')"
python -m pytest -q @selectedTests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Targeted tests passed; full pytest NOT run."
