$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Write-Host 'Phase 169 R3M: prior DB group results independent of proof completion'
Write-Host 'R3M_READ_ONLY: no production, registry or existing tests are changed'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase169_r3m_prior_result_catalog'
if (-not (Test-Path -LiteralPath (Join-Path $package 'prior_results.py'))) {
    throw 'R3M package must be extracted under the repository root'
}
$branch = git branch --show-current
if ($LASTEXITCODE -ne 0) { throw 'Cannot determine git branch' }
Write-Host "R3M_GIT_BRANCH=$branch"
if ($branch -ne 'develop') { throw 'Please switch to develop before running' }
python -B -m pytest -q '.\phase169_r3m_prior_result_catalog\tests\test_prior_results.py'
$tests = $LASTEXITCODE
Write-Host "R3M_FOCUSED_PYTEST_EXIT_CODE=$tests"
if ($tests -ne 0) { throw 'R3M focused tests failed' }
python -B -m phase169_r3m_prior_result_catalog.audit
$audit = $LASTEXITCODE
Write-Host "R3M_AUDIT_EXIT_CODE=$audit"
if ($audit -ne 0) { throw 'R3M audit failed' }
Write-Host 'R3M_COMPLETE: result catalog implemented; search integration deferred; full pytest NOT run.'
