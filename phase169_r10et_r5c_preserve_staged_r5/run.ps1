param(
    [ValidateSet('focus','all')][string]$Cases = 'all'
)
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$Output = Join-Path $PSScriptRoot ('output\' + $Stamp)
Push-Location $Repo
try {
    & python -m phase169_r10et_r5c_preserve_staged_r5.run `
        --root $Repo --output $Output --cases $Cases
    $Code = $LASTEXITCODE
    Write-Host "R10ET_R5C_EXIT=$Code"
    if ($Code -ne 0) { exit $Code }
} finally {
    Pop-Location
}
