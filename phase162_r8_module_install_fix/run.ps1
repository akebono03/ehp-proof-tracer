$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oldPath = $env:PYTHONPATH
try {
    python -B (Join-Path $PSScriptRoot 'install.py')
    if ($LASTEXITCODE -ne 0) { throw 'Module installation failed' }
    Push-Location $repo
    try {
        $env:PYTHONPATH = @($repo, (Join-Path $repo 'tests'), $oldPath) -join ';'
        python -B -c 'from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay; print("Root import OK:", build_phase162_pi5_3_web_replay.__module__)'
        if ($LASTEXITCODE -ne 0) { throw 'Root import failed' }
        python -B -m pytest -q (Join-Path $PSScriptRoot 'test_module_install.py')
        if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
        Write-Host 'R8 missing-module repair verified. Full suite not run.'
    } finally {
        Pop-Location
    }
} finally {
    $env:PYTHONPATH = $oldPath
}
