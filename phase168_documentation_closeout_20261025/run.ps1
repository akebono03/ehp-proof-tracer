$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    & python -B -m phase168_documentation_closeout_20261025.update_docs apply
    if ($LASTEXITCODE -ne 0) { throw 'Phase 168 documentation application failed' }
    & python -B -m phase168_documentation_closeout_20261025.update_docs verify
    if ($LASTEXITCODE -ne 0) { throw 'Phase 168 documentation verification failed' }
    Write-Host 'PHASE_168_DOCUMENTATION_COMPLETE'
    Write-Host "FULL_DOCUMENTS $(Join-Path $Package 'output\full_files')"
    Write-Host 'FULL_PYTEST_NOT_RERUN: documentation-only update after final test closure'
}
finally {
    Pop-Location
}
