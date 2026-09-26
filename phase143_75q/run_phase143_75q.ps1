$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python `
    ".\phase143_75q\audit_phase143_75q_full_fallback.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
