$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$testsDir = Join-Path $repo 'tests'
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$priorPath = $env:PYTHONPATH
try {
    $parts = @($auditDir, $repo, $testsDir)
    if ($priorPath) { $parts += $priorPath }
    $env:PYTHONPATH = $parts -join ';'
    python -B (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw "Apply failed: $LASTEXITCODE" }
    python -B -m pytest -q `
        (Join-Path $PSScriptRoot 'test_r7b_delta.py') `
        (Join-Path $repo 'phase162_r7b_orphan_exactness_final_fix/test_r7b_final.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    Write-Host 'R7-B Delta premise reuse focused tests passed. Full suite not run.'
} finally {
    $env:PYTHONPATH = $priorPath
}
