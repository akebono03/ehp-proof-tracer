$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $python) {
    & python (Join-Path $PSScriptRoot 'audit.py')
} else {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($null -eq $py) { throw 'Python executable not found' }
    & py -3 (Join-Path $PSScriptRoot 'audit.py')
}
if ($LASTEXITCODE -ne 0) { throw 'Renderer audit failed' }
