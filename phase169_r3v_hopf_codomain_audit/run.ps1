$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'R3V requires project Git root.' }
    $branch = (git branch --show-current).Trim()
    Write-Host "R3V_GIT_BRANCH=$branch"
    if ($branch -ne 'develop') { throw 'R3V requires develop branch.' }
    Write-Host 'R3V AUDIT_ONLY: production files, existing tests, and documents remain untouched'
    python -B -m phase169_r3v_hopf_codomain_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3V Hopf source audit failed' }
    python -B -m pytest -q -p no:cacheprovider .\phase169_r3v_hopf_codomain_audit\tests\test_phase169_r3v_hopf_codomain_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R3V focused pytest failed' }
    Write-Host 'R3V_COMPLETE: audit only; full pytest NOT run.'
} finally {
    Pop-Location
}
