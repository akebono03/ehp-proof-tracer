$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    python "$package\install.py"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $tests = @(
        (Join-Path $package 'test_phase165_r56_r1_generator_suspension_fix.py'),
        (Join-Path $root 'test_phase165_r56_common_renderer.py'),
        (Join-Path $root 'test_phase165_r55_nk_only_goal.py')
    )
    foreach ($test in $tests) {
        if (-not (Test-Path -LiteralPath $test -PathType Leaf)) {
            throw "Required targeted test not found: $test"
        }
    }
    python -m pytest -q @tests
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host 'R56-R1 targeted tests passed. Full pytest NOT run.'
}
finally {
    Pop-Location
}
