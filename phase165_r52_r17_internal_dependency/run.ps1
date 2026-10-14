$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R17 installation failed' }
python -m pytest -q test_phase165_r52_r17_internal_dependency.py test_phase165_r52_r9_shared_math.py test_phase165_r52_r14_root_dependency_guard.py test_phase165_r52_r15_ordered_citation.py test_phase165_r52_r16_web_citation_gate.py
if ($LASTEXITCODE -ne 0) { throw 'R17 targeted tests failed' }
Write-Host 'R52-R17 targeted tests passed; full pytest NOT run.'
