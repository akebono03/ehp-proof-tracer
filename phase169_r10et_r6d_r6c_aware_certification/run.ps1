$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    & python -B -m phase169_r10et_r6d_r6c_aware_certification.run --repo $Repo
    $Code = $LASTEXITCODE
    exit $Code
} finally {
    Pop-Location
}
