$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r4_helper_source_audit\audit_phase144_6_r4_helper_source.py"
  if ($LASTEXITCODE -ne 0) {
    throw "R4 helper-source audit failed."
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
