$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $PackageDir
Set-Location $RepoDir
python ".\phase166_close_test_module_inventory\close.py" --repo "."
exit $LASTEXITCODE
