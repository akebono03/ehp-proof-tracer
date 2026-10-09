$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$selectionDir = Join-Path $repo 'phase162_r7_b_selection_audit'
$previousPythonPath = $env:PYTHONPATH
if (-not (Test-Path (Join-Path $auditDir 'phase162_pi5_3_renderer_audit.py'))) {
    throw 'Renderer audit module is missing. Apply the earlier Phase 162 renderer audit ZIP first.'
}
if (-not (Test-Path (Join-Path $selectionDir 'audit_r7_b.py'))) {
    throw 'R7-B selection audit module is missing. Apply the earlier R7-B selection ZIP first.'
}
try {
    $paths = @($PSScriptRoot, $selectionDir, $auditDir, $repo, (Join-Path $repo 'tests'))
    if (-not [string]::IsNullOrEmpty($previousPythonPath)) {
        $paths += $previousPythonPath
    }
    $env:PYTHONPATH = $paths -join ';'
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    python -B (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) { throw "R7-B Delta provenance audit failed: $LASTEXITCODE" }
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
