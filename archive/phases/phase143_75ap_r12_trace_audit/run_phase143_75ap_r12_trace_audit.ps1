$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase143_75ap_r12_trace_audit\audit_phase143_75ap_r12_trace.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
