$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    & python -B -m phase168_documentation_closeout_20261025.update_docs restore
    if ($LASTEXITCODE -ne 0) { throw 'Phase 168 documentation restoration refused or failed' }
}
finally {
    Pop-Location
}
