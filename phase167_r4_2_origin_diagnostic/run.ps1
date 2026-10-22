$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$root=Split-Path -Parent $here
Set-Location $root
$env:PYTHONPATH=$root + [IO.Path]::PathSeparator + $env:PYTHONPATH
python "$here\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Origin diagnostic failed' }
