$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
  python -m pytest -q `
    (Join-Path $package 'tests\test_audit.py') `
    '.\test_phase165_r52_r3_web_adapter.py' `
    '.\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py' `
    '.\phase168_r3_20_flask_actual_cutover\tests\test_phase168_r3_20_flask_actual_cutover.py'
  if ($LASTEXITCODE -ne 0) { throw 'R3-41A limited pytest failed' }
  python -m phase168_r3_41a_partial_model_gap_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R3-41A read-only audit failed' }
  Write-Host 'R3-41A complete. No implementation files modified. Full pytest NOT run.'
}
finally { Pop-Location }
