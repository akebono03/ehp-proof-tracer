$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase162_r5_web_integration\apply_phase162_r5.py"
if ($LASTEXITCODE -ne 0) { throw 'R5 installation failed' }
python -B -m py_compile ".\phase162_web_narrative_integration.py" ".\web_group_proof.py" ".\tests\test_phase162_r5_web_integration.py"
if ($LASTEXITCODE -ne 0) { throw 'Syntax validation failed' }
python -B -m pytest -q ".\tests\test_phase162_r5_web_integration.py" ".\tests\test_phase162_r4_narrative_refinement.py" ".\tests\test_phase161_r7_premise_provenance_validation.py"
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Phase 162 R5 focused tests complete. Full suite not run.'
