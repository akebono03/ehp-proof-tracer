$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Project
try {
    python -m pytest -q `
      ".\phase168_r3_41i_renderer_closure_audit\tests\test_audit.py" `
      ".\phase168_r3_39f_frozen_comparison\tests\test_audit.py" `
      ".\phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-41I limited pytest failed" }
    python -m phase168_r3_41i_renderer_closure_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-41I baseline capture failed; inspect audit.json" }
    Write-Host "R3-41I read-only frozen quality audit complete. Full pytest NOT run."
}
finally {
    Pop-Location
}
