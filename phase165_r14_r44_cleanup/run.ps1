$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = if ($Old) { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot$([IO.Path]::PathSeparator)$Old" } else { "$Root$([IO.Path]::PathSeparator)$PSScriptRoot" }
  python (Join-Path $PSScriptRoot "cleanup.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q (Join-Path $PSScriptRoot "test_cleanup.py")
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  $env:PYTHONPATH = $Old
}
Write-Host "R44 cleanup targeted checks complete; full pytest NOT run."
