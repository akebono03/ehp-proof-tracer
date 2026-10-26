$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase169_r3j_narrative_boundary_audit'
Write-Host 'Phase 169 R3J: AUDIT_ONLY completed pi5_3 Narrative vs Proof Tree'
Write-Host 'R3J_AUDIT_ONLY: no production, tests, or docs will be modified'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'Git revision cannot be resolved' }
$paths = @(
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'tests\test_r3j_narrative_boundary_audit.py'),
    (Join-Path $repo 'phase168_r3_5_model_renderer.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase169_r3h_source_registry.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py')
)
foreach ($path in $paths) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "R3J_MISSING_PATH: $path"
    }
}
# Avoid passing Python double-quoted literals through PowerShell's native argv.
python -B -c 'from phase165_r14_r5_ehp_connection import expand_cited_ehp_terminal_goal; assert callable(expand_cited_ehp_terminal_goal)'
if ($LASTEXITCODE -ne 0) { throw 'R3J needs successfully installed R3I2' }
Write-Host 'R3J_PREFLIGHT_OK=True'
Write-Host '[1/2] Focused tests only (no full suite)'
python -B -m pytest -q `
    '.\phase169_r3j_narrative_boundary_audit\tests\test_r3j_narrative_boundary_audit.py' `
    '.\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'
$testCode = $LASTEXITCODE
Write-Host "R3J_FOCUSED_PYTEST_EXIT_CODE=$testCode"
if ($testCode -ne 0) { throw "R3J_FOCUSED_PYTEST_EXIT_CODE=$testCode" }
Write-Host '[2/2] Capture canonical Web narrative, citation IDs, steps and anomalies'
python -B -m phase169_r3j_narrative_boundary_audit.audit
$auditCode = $LASTEXITCODE
Write-Host "R3J_AUDIT_EXIT_CODE=$auditCode"
if ($auditCode -ne 0) { throw "R3J_AUDIT_EXIT_CODE=$auditCode" }
Write-Host 'R3J_COMPLETE: Narrative diagnosis saved; no code patched; full suite NOT run.'
