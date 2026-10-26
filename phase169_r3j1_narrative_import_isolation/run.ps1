$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase169_r3j1_narrative_import_isolation'
Write-Host 'Phase 169 R3J1: isolate legacy EHP adapter pytest import path from public narrative audit'
Write-Host 'R3J1_AUDIT_ONLY: no production, existing tests or docs will be modified'
Write-Host 'Git HEAD:'
git rev-parse --short HEAD
if ($LASTEXITCODE -ne 0) { throw 'Git revision cannot be resolved' }
$paths = @(
    (Join-Path $package 'audit.py'),
    (Join-Path $package 'preflight.py'),
    (Join-Path $package 'tests\test_r3j_narrative_boundary_audit.py'),
    (Join-Path $package 'tests\test_r3j1_import_isolation.py'),
    (Join-Path $repo 'phase168_r3_5_model_renderer.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\phase165_r14_r5_ehp_connection.py'),
    (Join-Path $repo 'phase169_r3h_source_registry.py'),
    (Join-Path $repo 'phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py')
)
foreach ($path in $paths) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "R3J1_MISSING_PATH: $path"
    }
}
# Check the actual module path in a clean process from the repository root.
# Running a module avoids PowerShell native-argument quote translation.
python -B -m phase169_r3j1_narrative_import_isolation.preflight
if ($LASTEXITCODE -ne 0) { throw 'R3J1_ROOT_EHP_MODULE_CHECK_FAILED' }
Write-Host 'R3J1_ROOT_EHP_MODULE_OK=True'
Write-Host 'R3J1_PREFLIGHT_OK=True'
Write-Host '[1/3] Focused existing EHP adapter tests in an isolated pytest process (no full suite)'
python -B -m pytest -q '.\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py'
$adapterCode = $LASTEXITCODE
Write-Host "R3J1_EHP_ADAPTER_PYTEST_EXIT_CODE=$adapterCode"
if ($adapterCode -ne 0) { throw "R3J1_EHP_ADAPTER_PYTEST_EXIT_CODE=$adapterCode" }
Write-Host '[2/3] Focused narrative audit and import-route tests in a fresh pytest process'
python -B -m pytest -q `
    '.\phase169_r3j1_narrative_import_isolation\tests\test_r3j_narrative_boundary_audit.py' `
    '.\phase169_r3j1_narrative_import_isolation\tests\test_r3j1_import_isolation.py'
$narrativeCode = $LASTEXITCODE
Write-Host "R3J1_NARRATIVE_PYTEST_EXIT_CODE=$narrativeCode"
if ($narrativeCode -ne 0) { throw "R3J1_NARRATIVE_PYTEST_EXIT_CODE=$narrativeCode" }
Write-Host 'R3J1_FOCUSED_PYTEST_EXIT_CODE=0'
Write-Host '[3/3] Capture canonical Web narrative, citation IDs, steps and anomalies'
python -B -m phase169_r3j1_narrative_import_isolation.audit
$auditCode = $LASTEXITCODE
Write-Host "R3J1_AUDIT_EXIT_CODE=$auditCode"
if ($auditCode -ne 0) { throw "R3J1_AUDIT_EXIT_CODE=$auditCode" }
Write-Host 'R3J1_COMPLETE: Narrative diagnosis saved; no code patched; full suite NOT run.'
