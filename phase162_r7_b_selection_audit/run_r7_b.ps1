$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$testsDir = Join-Path $repo 'tests'
if (-not (Test-Path (Join-Path $auditDir 'phase162_pi5_3_renderer_audit.py'))) {
    throw 'Previous Phase 162 renderer audit module is missing.'
}
if (-not (Test-Path (Join-Path $repo 'phase162_pi5_3_backward_selection.py'))) {
    throw 'Phase 162 reconstructed proof module is missing.'
}
$oldPythonPath = $env:PYTHONPATH
try {
    $parts = @($PSScriptRoot, $auditDir, $repo, $testsDir)
    if (-not [string]::IsNullOrEmpty($oldPythonPath)) { $parts += $oldPythonPath }
    $env:PYTHONPATH = $parts -join ';'
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_r7_b.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    python -B (Join-Path $PSScriptRoot 'audit_r7_b.py')
    if ($LASTEXITCODE -ne 0) { throw "R7-B audit failed: $LASTEXITCODE" }
} finally {
    $env:PYTHONPATH = $oldPythonPath
}
