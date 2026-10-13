$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $projectRoot

$requiredTest = "test_phase165_r52_r11_common_renderer.py"
if (-not (Test-Path -LiteralPath $requiredTest -PathType Leaf)) {
    throw "R52-R11 test is not installed: $requiredTest"
}

$optionalTests = @(
    "test_phase165_r52_r10_readable_partial.py",
    "test_phase165_r52_partial_proof.py",
    "test_phase165_r52_r9_shared_math.py",
    "test_phase165_r52_r8_show_proof_route.py"
)
$selectedTests = @($requiredTest)
foreach ($candidate in $optionalTests) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $selectedTests += $candidate
    } else {
        Write-Host "Optional test not installed; skipping: $candidate"
    }
}

Write-Host "R52-R11 targeted tests: $($selectedTests -join ', ')"
python -m pytest -q @selectedTests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R52-R11 targeted tests passed; full pytest NOT run."
