$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
$previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = "$root;$previous"
  python -m phase165_renderer_restore_r1_test_fix.install
  if ($LASTEXITCODE -ne 0) { throw 'Renderer restore installation failed' }
  python -m pytest -q '.\phase165_renderer_restore_r1_test_fix\test_restore.py' '.\phase165_renderer_restore_r1_test_fix\test_shared_generator_suspension.py'
  if ($LASTEXITCODE -ne 0) { throw 'Renderer restore targeted tests failed' }
} finally {
  $env:PYTHONPATH = $previous
  Pop-Location
}
