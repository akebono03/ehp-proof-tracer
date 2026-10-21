$ErrorActionPreference = "Stop"
if (-not (Test-Path "phase165_r52_r9_shared_math.py")) { throw "Run in EHP Proof Tracer root" }
python ".\phase166_r3ac_r3v_test_alignment\install.py"
if ($LASTEXITCODE -ne 0) { throw "Installation stopped" }
python -m pytest -q "phase166_r3v_test_repair/test_r3v.py" "phase166_r3ac_stable_notation/test_r3ac.py"
if ($LASTEXITCODE -ne 0) { throw "R3-AC focused pytest FAILED" }
python -m phase166_r3ab_pi65_audit.audit
if ($LASTEXITCODE -ne 0) { throw "Pi65 audit failed" }
Write-Host "Focused tests completed; full pytest NOT run."
