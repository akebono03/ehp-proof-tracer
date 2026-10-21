$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$old = $env:PYTHONPATH
try {
  $env:PYTHONPATH = $root
  python '.\phase167_r4_2_render_origin_trace_v2\trace.py'
  if ($LASTEXITCODE -ne 0) { throw 'Trace failed' }
} finally {
  $env:PYTHONPATH = $old
}
