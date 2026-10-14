$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    python "$package\audit_routes.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $testNames = @(
        "test_phase165_r57_r1_single_entry.py",
        "test_phase165_r56_r2_public_renderer.py",
        "test_phase165_r56_common_renderer.py",
        "test_phase165_r55_nk_only_goal.py"
    )

    $tests = @()
    foreach ($name in $testNames) {
        $rootTest = Join-Path $root $name
        $ownTest = Join-Path $package $name
        if (Test-Path -LiteralPath $rootTest -PathType Leaf) {
            $tests += $rootTest
        }
        elseif (Test-Path -LiteralPath $ownTest -PathType Leaf) {
            $tests += $ownTest
        }
        else {
            $relativePackages = @{
                "test_phase165_r57_r1_single_entry.py" = "phase165_r57_r1_single_entry"
                "test_phase165_r56_r2_public_renderer.py" = "phase165_r56_r2_public_renderer"
                "test_phase165_r56_common_renderer.py" = "phase165_r56_common_renderer"
                "test_phase165_r55_nk_only_goal.py" = "phase165_r55_nk_only_web"
            }
            $nestedTest = Join-Path (Join-Path $root $relativePackages[$name]) $name
            if (Test-Path -LiteralPath $nestedTest -PathType Leaf) {
                $tests += $nestedTest
            }
            else {
                throw "Required targeted test not found in project root or Phase package: $name"
            }
        }
    }

    python -m pytest -q @tests
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "R57-R1 targeted tests passed; no legacy files auto-deleted; full pytest NOT run."
}
finally {
    Pop-Location
}
