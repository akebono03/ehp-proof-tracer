$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r5_2_frontier_required_depth_audit\audit_phase144_6_r5_2_frontier_required_depth.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R5-2 frontier required-depth audit failed."
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
