$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
python ".\phase165_r52_r16_r2_nullable_record_fix\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R16-R2 installation failed' }
python -m pytest -q `
  ".\phase165_r52_r16_r2_nullable_record_fix\test_phase165_r52_r16_r2_nullable_record_fix.py" `
  ".\phase165_r52_r16_r1_install_fix\test_phase165_r52_r16_web_citation_gate.py" `
  ".\test_phase165_r52_r9_shared_math.py" `
  ".\test_phase165_r52_r14_root_dependency_guard.py" `
  ".\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py"
if ($LASTEXITCODE -ne 0) { throw 'R16-R2 targeted tests failed' }
Write-Host 'R52-R16-R2 targeted tests passed; full pytest NOT run.'
