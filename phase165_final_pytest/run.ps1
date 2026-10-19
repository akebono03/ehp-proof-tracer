$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$outdir = Join-Path $root 'phase165_r6_audit_results\final_pytest'
New-Item -ItemType Directory -Path $outdir -Force | Out-Null
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$stdout = Join-Path $outdir "pytest_${stamp}_stdout.txt"
$stderr = Join-Path $outdir "pytest_${stamp}_stderr.txt"
Write-Host 'Phase 165 final full pytest: python -m pytest tests -q --tb=short'
Write-Host "Output: $stdout"
$started = (Get-Date).ToUniversalTime().ToString('o')
$p = Start-Process -FilePath 'python' -ArgumentList @('-m','pytest','tests','-q','--tb=short') -WorkingDirectory $root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$finished = (Get-Date).ToUniversalTime().ToString('o')
$tail = @(Get-Content -LiteralPath $stdout -Tail 45 -ErrorAction SilentlyContinue)
Write-Host '--- pytest output tail ---'
$tail | ForEach-Object { Write-Host $_ }
$report = [ordered]@{
  phase = '165 final pytest'
  command = 'python -m pytest tests -q --tb=short'
  status = $(if ($p.ExitCode -eq 0) { 'FULL_PYTEST_PASS' } else { 'FULL_PYTEST_FAILED' })
  exit_code = $p.ExitCode
  started_utc = $started
  finished_utc = $finished
  stdout_file = $stdout
  stderr_file = $stderr
  source_files_changed = $false
}
$reportFile = Join-Path $outdir "pytest_${stamp}_summary.json"
$report | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $reportFile -Encoding UTF8
Write-Host '--- summary ---'
$report | ConvertTo-Json -Depth 4 | Write-Host
if ($p.ExitCode -ne 0) { exit $p.ExitCode }
