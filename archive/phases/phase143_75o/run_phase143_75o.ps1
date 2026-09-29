$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python `
    ".\phase143_75o\audit_phase143_75o_prop44_suspension_injective.py"
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
}
