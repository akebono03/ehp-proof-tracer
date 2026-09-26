$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\phase143_75a\audit_phase143_75a_rule_name_fallback.py")) {
  throw "phase143_75a audit script was not found."
}

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase143_75a\audit_phase143_75a_rule_name_fallback.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
