$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path (Join-Path $repoRoot 'phase162_pi5_3_renderer_audit\phase162_pi5_3_renderer_audit.py'))) {
    throw 'Run this from the repository with Phase162 renderer audit installed.'
}
$oldPath = $env:PYTHONPATH
Push-Location $repoRoot
try {
    $env:PYTHONPATH = "$repoRoot;$repoRoot\tests;$repoRoot\phase162_pi5_3_renderer_audit;$oldPath"
    python -B (Join-Path $PSScriptRoot 'trace.py')
    if ($LASTEXITCODE -ne 0) { throw "Trace failed: $LASTEXITCODE" }
} finally {
    $env:PYTHONPATH = $oldPath
    Pop-Location
}
