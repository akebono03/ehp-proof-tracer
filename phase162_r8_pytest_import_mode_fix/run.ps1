$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oldPath = $env:PYTHONPATH

try {
    Push-Location $repo
    try {
        $modulePath = Join-Path $repo 'phase162_pi5_3_web_replay.py'
        if (-not (Test-Path -LiteralPath $modulePath -PathType Leaf)) {
            throw 'Required Phase 162 module is missing from repository root.'
        }

        $testDirectory = Join-Path $repo 'phase162_r8_module_install_fix'
        $testPath = Join-Path $testDirectory 'test_module_install.py'
        if (-not (Test-Path -LiteralPath $testPath -PathType Leaf)) {
            throw "Required focused test file is missing: $testPath"
        }

        $paths = @($repo, (Join-Path $repo 'tests'))
        if (-not [string]::IsNullOrEmpty($oldPath)) {
            $paths += $oldPath
        }
        $env:PYTHONPATH = $paths -join ';'

        # Import test files without prepending their directories to sys.path.
        # A same-named module in the test package must not shadow the installed root module.
        python -B -m pytest -q --import-mode=importlib $testPath
        if ($LASTEXITCODE -ne 0) {
            throw "R8 focused pytest failed: $LASTEXITCODE"
        }

        Write-Host 'R8 module import and Web routing tests passed. Full suite not run.'
    } finally {
        Pop-Location
    }
} finally {
    $env:PYTHONPATH = $oldPath
}
