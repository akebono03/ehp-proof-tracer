$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase144_6_r5_4_r1_group_result_fix\audit_phase144_6_r5_4_argument_dependency_gap.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Phase 144-6-R5-4-R1 audit failed."
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
