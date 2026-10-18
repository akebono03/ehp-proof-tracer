$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
$previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = "$root;$previous"
  python -m phase165_reference_stop_r3.install
  if ($LASTEXITCODE -ne 0) { throw "R3 install failed" }
  python -m pytest -q ".\phase165_reference_stop_r3\test_reference_priority.py" ".\phase165_r52_r16_web_citation_gate\test_phase165_r52_r16_web_citation_gate.py"
  if ($LASTEXITCODE -ne 0) { throw "R3 targeted pytest failed" }
} finally {
  $env:PYTHONPATH = $previous
  Pop-Location
}
