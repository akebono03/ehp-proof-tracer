$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path (Join-Path $repoRoot 'toda_group_proof_narrative_exactness_display_contributions.py'))) {
    throw 'Run in the EHP Proof Tracer repository root.'
}
if (-not (Test-Path (Join-Path $repoRoot 'phase162_pi5_3_renderer_audit\phase162_pi5_3_renderer_audit.py'))) {
    throw 'Required Phase 162 renderer audit module is missing.'
}
Push-Location $repoRoot
$previousPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$repoRoot;$repoRoot\tests;$repoRoot\phase162_pi5_3_renderer_audit;$previousPath"
    python -B (Join-Path $PSScriptRoot 'apply_fix.py')
    if ($LASTEXITCODE -ne 0) { throw "Apply failed: $LASTEXITCODE" }
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_exactness_window_source_fix.py') (Join-Path $repoRoot 'phase162_exactness_math_repair\test_phase162_exactness_math_repair.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    Write-Host 'Focused exactness tests passed; full suite not run.'
    Write-Host 'To view narrative again: powershell -ExecutionPolicy Bypass -File ".\phase162_pi5_3_renderer_audit\run_phase162_pi5_3_renderer_audit.ps1"'
} finally {
    $env:PYTHONPATH = $previousPath
    Pop-Location
}
