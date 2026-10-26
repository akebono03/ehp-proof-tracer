$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'R3X requires the Git repository root.' }
    $Branch = (git branch --show-current).Trim()
    Write-Host "R3X_GIT_BRANCH=$Branch"
    if ($Branch -ne 'develop') { throw 'R3X requires develop branch.' }
    Write-Host 'R3X AUDIT_ONLY: no production, existing tests, or project documents modified'
    python -B -m phase169_r3x_source_bound_eta_probe.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3X source-bound audit failed' }
    python -B -m pytest -q -p no:cacheprovider .\phase169_r3x_source_bound_eta_probe\tests\test_phase169_r3x_source_bound_eta_probe.py
    if ($LASTEXITCODE -ne 0) { throw 'R3X limited tests failed' }
    Write-Host 'R3X_COMPLETE: audit only; full pytest NOT run.'
} finally {
    Pop-Location
}
