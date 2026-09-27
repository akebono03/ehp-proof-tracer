$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  python ".\phase144_6_r4_dependency_distance_audit\audit_phase144_6_r4_dependency_distance.py"
  if ($LASTEXITCODE -ne 0) { throw "Dependency-distance audit failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
