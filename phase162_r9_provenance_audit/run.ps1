$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oldPath = $env:PYTHONPATH
try {
    Push-Location $repo
    try {
        $parts = @($repo, (Join-Path $repo 'tests'), $PSScriptRoot)
        if (-not [string]::IsNullOrEmpty($oldPath)) { $parts += $oldPath }
        $env:PYTHONPATH = $parts -join ';'
        $testPath = Join-Path $PSScriptRoot 'test_audit.py'
        python -B -m pytest -q --import-mode=importlib $testPath
        if ($LASTEXITCODE -ne 0) { throw "R9 focused pytest failed: $LASTEXITCODE" }
        $auditPath = Join-Path $PSScriptRoot 'audit.py'
        python -B $auditPath
        if ($LASTEXITCODE -ne 0) { throw "R9 audit failed: $LASTEXITCODE" }
    } finally { Pop-Location }
} finally { $env:PYTHONPATH = $oldPath }
