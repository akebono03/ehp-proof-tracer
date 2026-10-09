$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$testsDir = Join-Path $repo 'tests'
$priorPath = $env:PYTHONPATH
try {
    $parts = @($auditDir, $repo, $testsDir)
    if ($priorPath) { $parts += $priorPath }
    $env:PYTHONPATH = $parts -join ';'
    python -B (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw "Apply failed: $LASTEXITCODE" }
    python -B -m pytest -q `
        (Join-Path $PSScriptRoot 'test_r7b_final.py') `
        (Join-Path (Join-Path $repo 'phase162_r7b_orphan_exactness_fix') 'test_r7b.py') `
        (Join-Path $testsDir 'test_phase157_r20_repair43_dangling_connector_cleanup.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    Write-Host 'R7-B final public narrative boundary tests passed. Full suite not run.'
} finally {
    $env:PYTHONPATH = $priorPath
}
