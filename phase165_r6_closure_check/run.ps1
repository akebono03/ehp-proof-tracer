$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$PSScriptRoot\audit.py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$PSScriptRoot\audit.py"
} else {
    throw 'Python 3 was not found on PATH.'
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
