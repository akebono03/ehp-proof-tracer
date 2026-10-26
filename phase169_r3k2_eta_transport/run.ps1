$ErrorActionPreference = 'Stop'
$Repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $Repo '.git'))) {
    throw 'Execute run.ps1 from the ehp-proof-tracer repository root.'
}
Write-Host 'Phase 169 R3K2: typed eta-squared image projection'
Write-Host 'Scope: 2 presentation functions; search, registry, existing tests and documents untouched.'

# Check installer anchors before writing to production files.
python -m pytest -q .\phase169_r3k2_eta_transport\tests\test_r3k2a_anchor_guard.py
if ($LASTEXITCODE -ne 0) { throw "R3K2A installer regression failed: $LASTEXITCODE" }
Write-Host 'R3K2A_INSTALLER_PYTEST_EXIT_CODE=0'

python -m phase169_r3k2_eta_transport.apply
if ($LASTEXITCODE -ne 0) { throw "R3K2 guarded installation failed: $LASTEXITCODE" }

python -m pytest -q .\phase169_r3k2_eta_transport\tests\test_r3k2_eta_transport.py .\phase169_r3j1_narrative_import_isolation\tests\test_r3j_narrative_boundary_audit.py
if ($LASTEXITCODE -ne 0) { throw "R3K2 focused pytest failed: $LASTEXITCODE" }
Write-Host 'R3K2_FOCUSED_PYTEST_EXIT_CODE=0'

# Separate pytest process avoids EHP adapter import collisions from older test paths.
python -m pytest -q .\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py
if ($LASTEXITCODE -ne 0) { throw "R3K2 1-stem regression failed: $LASTEXITCODE" }
Write-Host 'R3K2_ONE_STEM_PYTEST_EXIT_CODE=0'

python -m phase169_r3k2_eta_transport.audit
if ($LASTEXITCODE -ne 0) { throw "R3K2 canonical Web audit failed: $LASTEXITCODE" }
Write-Host 'R3K2_COMPLETE: focused checks only; full pytest NOT run.'
