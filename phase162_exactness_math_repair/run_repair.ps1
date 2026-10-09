$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path (Join-Path $repoRoot 'toda_group_proof_narrative_renderer.py'))) { throw 'Repository root not found' }
if (-not (Test-Path (Join-Path $repoRoot 'phase162_pi5_3_renderer_audit\phase162_pi5_3_renderer_audit.py'))) { throw 'Prior Phase162 renderer audit is missing' }
Push-Location $repoRoot
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$repoRoot;$repoRoot\tests;$repoRoot\phase162_pi5_3_renderer_audit;$oldPythonPath"
    python -B (Join-Path $PSScriptRoot 'apply_repair.py')
    if ($LASTEXITCODE -ne 0) { throw "Apply failed: $LASTEXITCODE" }
    python -B -m pytest -q (Join-Path $PSScriptRoot 'test_phase162_exactness_math_repair.py')
    if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
    Write-Host 'Focused tests passed. Re-run prior public narrative audit to inspect the rendered text:'
    Write-Host 'powershell -ExecutionPolicy Bypass -File ".\phase162_pi5_3_renderer_audit\run_phase162_pi5_3_renderer_audit.ps1"'

} finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
Write-Host 'Focused exactness math repair complete. Full suite not run.'
