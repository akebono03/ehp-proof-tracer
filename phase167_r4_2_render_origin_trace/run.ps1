$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$previous = $env:PYTHONPATH
try {
  $env:PYTHONPATH = $root
  python '.\phase167_r4_2_render_origin_trace\trace.py'
  if ($LASTEXITCODE -ne 0) { throw 'R4-2 trace failed' }
} finally {
  $env:PYTHONPATH = $previous
}
