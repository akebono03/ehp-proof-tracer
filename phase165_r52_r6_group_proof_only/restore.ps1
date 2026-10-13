$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'web_app.py'))) { throw 'Run from repository root' }
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundle 'install.py') --restore
if ($LASTEXITCODE -ne 0) { throw 'R52-R6 restore failed' }
