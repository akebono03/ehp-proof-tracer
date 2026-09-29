$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")
Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  python ".\phase144_6_r5_3_root_argument_dependency_audit\audit_phase144_6_r5_3_root_argument_dependencies.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R5-3 root-argument dependency audit failed."
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
