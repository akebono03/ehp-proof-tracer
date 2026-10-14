$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R18 installation failed' }
$tests = @('test_phase165_r52_r18_proof_order.py', 'test_phase165_r52_r17_internal_dependency.py', 'test_phase165_r52_r9_shared_math.py', 'test_phase165_r52_r14_root_dependency_guard.py', 'phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py', 'phase165_r52_r16_web_citation_gate\test_phase165_r52_r16_web_citation_gate.py')
foreach ($test in $tests) { if (-not (Test-Path $test)) { throw "Missing required targeted test: $test" } }
python -m pytest -q @tests
if ($LASTEXITCODE -ne 0) { throw 'R18 targeted tests failed' }
Write-Host 'R18 targeted tests passed; full pytest NOT run.'
