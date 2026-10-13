$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repo
$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
$pythonExe = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $pyLauncher) {
    & py -3 (Join-Path $PSScriptRoot 'audit.py')
} elseif ($null -ne $pythonExe) {
    & python (Join-Path $PSScriptRoot 'audit.py')
} else {
    throw 'Python 3 was not found.'
}
if ($LASTEXITCODE -ne 0) {
    throw 'R49 audit failed.'
}
