$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$priorPath = $env:PYTHONPATH
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$testsDir = Join-Path $repo 'tests'
try {
    $paths = @($auditDir, $repo, $testsDir)
    if ($priorPath) { $paths += $priorPath }
    $env:PYTHONPATH = $paths -join ';'
    python -B (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'Apply failed' }
    python -B -m pytest -q `
        (Join-Path $PSScriptRoot 'test_r7b.py') `
        (Join-Path $testsDir 'test_phase157_r20_repair43_dangling_connector_cleanup.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    Write-Host 'R7-B orphan exactness introduction focused tests passed. Full suite not run.'
} finally {
    $env:PYTHONPATH = $priorPath
}
