$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
python '.\phase166_close_sharded_runner\run.py' --repo '.' --batch-size 12
exit $LASTEXITCODE
