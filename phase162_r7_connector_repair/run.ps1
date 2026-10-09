$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$testsDir = Join-Path $repo 'tests'
$auditDir = Join-Path $repo 'phase162_pi5_3_renderer_audit'
$priorPath = $env:PYTHONPATH

if (-not (Test-Path (Join-Path $auditDir 'phase162_pi5_3_renderer_audit.py'))) {
    throw 'Phase 162 renderer audit module not found.'
}
if (-not (Test-Path (Join-Path $repo 'toda_group_proof_narrative_contribution_renderer.py'))) {
    throw 'Run from the EHP Proof Tracer repository root.'
}

try {
    $parts = @($auditDir, $repo, $testsDir)
    if (-not [string]::IsNullOrEmpty($priorPath)) {
        $parts += $priorPath
    }
    $env:PYTHONPATH = $parts -join ';'

    python -B -m pytest -q `
        (Join-Path $PSScriptRoot 'test_r7.py') `
        (Join-Path $testsDir 'test_phase157_r20_repair43_dangling_connector_cleanup.py')
    if ($LASTEXITCODE -ne 0) {
        throw "Focused pytest failed: $LASTEXITCODE"
    }
    Write-Host 'Phase 162 R7 focused tests passed. Full suite not run.'
} finally {
    $env:PYTHONPATH = $priorPath
}
