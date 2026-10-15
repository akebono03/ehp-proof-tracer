$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$originalPythonPath = $env:PYTHONPATH
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $tests = @(
        (Join-Path $package "test_phase165_r57_r5_backup_reference_cleanup.py"),
        (Join-Path (Join-Path $root "phase165_r57_r4_shadowed_branch_cleanup") "test_phase165_r57_r4_shadowed_branch_cleanup.py"),
        (Join-Path (Join-Path $root "phase165_r57_r3_legacy_renderer_retirement") "test_phase165_r57_r3_legacy_renderer_retirement.py"),
        (Join-Path (Join-Path $root "phase165_r57_r2_public_single_renderer") "test_phase165_r57_r2_public_single_renderer.py"),
        (Join-Path (Join-Path $root "phase165_r56_r2_public_renderer") "test_phase165_r56_r2_public_renderer.py")
    )

    foreach ($test in $tests) {
        if (-not (Test-Path -LiteralPath $test -PathType Leaf)) {
            throw "Required targeted test missing: $test"
        }
    }

    foreach ($test in $tests) {
        $testDirectory = Split-Path -Parent $test
        $env:PYTHONPATH = "$testDirectory;$root"
        Write-Host "Running focused pytest: $test"
        python -m pytest -q "$test"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    Write-Host "R57-R5 targeted tests passed; full pytest NOT run."
}
finally {
    $env:PYTHONPATH = $originalPythonPath
    Pop-Location
}
