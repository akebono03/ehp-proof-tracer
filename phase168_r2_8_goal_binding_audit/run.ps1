$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $repo
try {
    python -m pytest -q phase168_r2_8_goal_binding_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    python -m phase168_r2_8_goal_binding_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "Goal audit failed" }
} finally {
    Pop-Location
}
