$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r55_nk_only_goal.py'))) {
  throw 'Run this script from the ehp_proof repository root.'
}
$reportDir = Join-Path $root 'phase165_r6_audit_results\r6_15_final_pytest'
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMddTHHmmss'
$stdout = Join-Path $reportDir "pytest_${stamp}_stdout.txt"
$stderr = Join-Path $reportDir "pytest_${stamp}_stderr.txt"
$summary = Join-Path $reportDir "pytest_${stamp}_summary.json"
$started = (Get-Date).ToUniversalTime().ToString('o')
Write-Host 'Phase 165 final full tests: python -m pytest tests -q --tb=short'
Write-Host "Output: $stdout"
$previousPref = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try {
  & python -m pytest tests -q --tb=short 1> $stdout 2> $stderr
  $exitCode = $LASTEXITCODE
} finally {
  $ErrorActionPreference = $previousPref
}
$finished = (Get-Date).ToUniversalTime().ToString('o')
$report = [ordered]@{
  phase = '165 R6-15'
  command = 'python -m pytest tests -q --tb=short'
  exit_code = $exitCode
  status = $(if ($exitCode -eq 0) { 'FULL_PYTEST_PASS' } else { 'FULL_PYTEST_FAILED' })
  started_utc = $started
  finished_utc = $finished
  stdout_file = $stdout
  stderr_file = $stderr
  source_files_changed = $false
}
$report | ConvertTo-Json -Depth 4 | Set-Content -Path $summary -Encoding UTF8
Write-Host '--- pytest output tail ---'
Get-Content $stdout -Tail 35
if ((Test-Path $stderr) -and ((Get-Item $stderr).Length -gt 0)) {
  Write-Host '--- stderr tail ---'
  Get-Content $stderr -Tail 15
}
Write-Host '--- summary ---'
Get-Content $summary
if ($exitCode -ne 0) { exit $exitCode }
