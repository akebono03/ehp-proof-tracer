$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'R3W requires the Git repository root.' }
    $Branch = (git branch --show-current).Trim()
    Write-Host "R3W_GIT_BRANCH=$Branch"
    if ($Branch -ne 'develop') { throw 'R3W requires develop branch.' }
    Write-Host 'R3W AUDIT_ONLY: no production file, existing test, or documentation changes'
    python -B -m phase169_r3w_duplicate_derivation_trace.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3W proof derivation diagnostic failed' }
    python -B -m pytest -q -p no:cacheprovider .\phase169_r3w_duplicate_derivation_trace\tests\test_phase169_r3w_duplicate_derivation_trace.py
    if ($LASTEXITCODE -ne 0) { throw 'R3W limited pytest failed' }
    Write-Host 'R3W_COMPLETE: audit only; full pytest NOT run.'
} finally {
    Pop-Location
}
