$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
  python -m phase165_rule_registry_r10.install
  if ($LASTEXITCODE -ne 0) { throw 'R10 installation failed' }
  python -m pytest -q phase165_rule_registry_r10/test_r10.py tests/test_phase165_r8_rule_provider.py
  if ($LASTEXITCODE -ne 0) { throw 'R10 targeted tests failed' }
  python -c "from phase165_r8_rule_provider import discover_inference_rules; from phase165_r10_rule_registry import build_rule_registry; r, report=discover_inference_rules(); x=build_rule_registry(report.modules); print({'status':'CONNECTED','rules':len(r),'registry_entries':len(x.entries),'rule_ids_unique':len({z.rule_id for z in x.entries})==len(x.entries),'requires_input':sum(s.endswith(':requires-input') for s in x.skipped_factories),'full_pytest_run':False})"
  if ($LASTEXITCODE -ne 0) { throw 'R10 connectivity check failed' }
} finally {
  Pop-Location
}
