$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")
Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  python ".\phase144_6_r4_duplicate_call_audit\audit_phase144_6_r4_duplicate_calls.py"
  if ($LASTEXITCODE -ne 0) { throw "duplicate-call audit failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
