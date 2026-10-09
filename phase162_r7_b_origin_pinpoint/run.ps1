$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$priorPath = $env:PYTHONPATH
if (-not (Test-Path (Join-Path $auditDir 'phase162_pi5_3_renderer_audit.py'))) { throw 'Phase 162 renderer audit module is missing.' }
if (-not (Test-Path (Join-Path $repo 'phase162_r7_b_selection_audit\audit_r7_b.py'))) { throw 'Prior R7-B selection audit is missing.' }
try {
    $parts = @($PSScriptRoot, (Join-Path $repo 'phase162_r7_b_selection_audit'), $auditDir, $repo, (Join-Path $repo 'tests'))
    if (-not [string]::IsNullOrEmpty($priorPath)) { $parts += $priorPath }
    $env:PYTHONPATH = $parts -join ';'
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_pinpoint.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    python -B (Join-Path $PSScriptRoot 'pinpoint.py')
    if ($LASTEXITCODE -ne 0) { throw "R7-B pinpoint failed: $LASTEXITCODE" }
} finally {
    $env:PYTHONPATH = $priorPath
}
