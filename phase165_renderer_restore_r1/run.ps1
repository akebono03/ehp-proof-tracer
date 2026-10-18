$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
$previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = "$root;$previous"
  python -m phase165_renderer_restore_r1.install
  if ($LASTEXITCODE -ne 0) { throw 'Renderer restore installation failed' }
  python -m pytest -q '.\phase165_renderer_restore_r1\test_restore.py' '.\phase165_r56_r1_generator_suspension_fix\test_phase165_r56_r1_generator_suspension_fix.py'
  if ($LASTEXITCODE -ne 0) { throw 'Renderer restore targeted tests failed' }
} finally {
  $env:PYTHONPATH = $previous
  Pop-Location
}
