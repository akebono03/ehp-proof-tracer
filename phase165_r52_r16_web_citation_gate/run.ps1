$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python ".\phase165_r52_r16_web_citation_gate\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R16 installation failed' }
python -m pytest -q `
  ".\phase165_r52_r16_web_citation_gate\test_phase165_r52_r16_web_citation_gate.py" `
  ".\test_phase165_r52_r9_shared_math.py" `
  ".\test_phase165_r52_r14_root_dependency_guard.py" `
  ".\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py"
if ($LASTEXITCODE -ne 0) { throw 'R16 targeted tests failed' }
Write-Host 'R52-R16 targeted tests passed; full pytest NOT run.'
