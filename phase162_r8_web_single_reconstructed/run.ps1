$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oldPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = @($repo, (Join-Path $repo 'tests'), $oldPath) -join ';'
    python -B (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'Apply failed' }
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_r8.py')
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
    Write-Host 'Phase 162 R8 focused web routing tests passed. Full suite not run.'
} finally { $env:PYTHONPATH = $oldPath }
