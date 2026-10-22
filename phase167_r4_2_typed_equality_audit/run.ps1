$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$original = $env:PYTHONPATH
try {
  $env:PYTHONPATH = $root
  python ".\phase167_r4_2_typed_equality_audit\audit.py"
  if ($LASTEXITCODE -ne 0) { throw 'Typed equality audit failed' }
} finally {
  $env:PYTHONPATH = $original
}
