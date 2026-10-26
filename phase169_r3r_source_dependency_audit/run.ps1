$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run inside repository root' }
    $Branch = (& git branch --show-current).Trim()
    Write-Host "R3R_GIT_BRANCH=$Branch"
    if ($Branch -ne 'develop') { throw 'R3R requires develop' }
    Write-Host 'R3R AUDIT_ONLY: no production file, test, or document is modified'
    python -B -m phase169_r3r_source_dependency_audit.audit
    if ($LASTEXITCODE -ne 0) { throw "R3R audit failed: $LASTEXITCODE" }
    Write-Host 'R3R_COMPLETE: report saved; full pytest NOT run.'
} finally {
    Pop-Location
}
