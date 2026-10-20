$ErrorActionPreference = 'Stop'
$root=(Get-Location).Path
$folder=Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $root 'phase165_r52_r9_shared_math.py'))) { throw 'Run from repository root' }
$env:PYTHONPATH=$root + [IO.Path]::PathSeparator + $env:PYTHONPATH
python (Join-Path $folder 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-L install failed' }
python -m pytest -q (Join-Path $folder 'test_phase166_r3l.py') test_phase165_r52_r9_shared_math.py tests/test_phase166_r3b_publication_order_binding.py
if ($LASTEXITCODE -ne 0) { throw 'R3-L targeted tests failed' }
python (Join-Path $folder 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-L audit failed' }
Write-Host 'R3-L targeted PASS; full pytest NOT run.'
