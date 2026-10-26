$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path .git)) { throw 'Expected project Git root.' }
    $branch = (git branch --show-current).Trim()
    Write-Host "R3T_GIT_BRANCH=$branch"
    if ($branch -ne 'develop') { throw 'Audit requires develop branch.' }
    Write-Host 'R3T AUDIT_ONLY: no production, existing test or documentation changes'
    python -B -m phase169_r3t_diagonal_premise_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3T audit failed' }
    python -B -m pytest -q -p no:cacheprovider .\phase169_r3t_diagonal_premise_audit\tests\test_phase169_r3t_diagonal_premise_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R3T focused tests failed' }
    Write-Host 'R3T_COMPLETE: audit-only; full pytest NOT run'
} finally {
    Pop-Location
}
