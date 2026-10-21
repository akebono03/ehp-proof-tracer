$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
python ".\phase166_docs_closure\apply.py" --root "."
exit $LASTEXITCODE
