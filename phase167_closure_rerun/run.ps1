$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase167_closure_rerun'
$log = Join-Path $folder 'pytest_full.log'
$status = Join-Path $folder 'pytest_exit_code.txt'
$arguments = @(
  '-m', 'pytest', 'tests', '-q', '--tb=short', '--disable-warnings',
  '--ignore=tests/test_phase144_6_pi6_generic_production_route.py',
  '--ignore=tests/test_phase144_6_public_route_cutover.py'
)
if (-not (Test-Path (Join-Path $root 'tests'))) { throw 'Run from repository root' }
$python = (Get-Command python -ErrorAction Stop).Source
Write-Host "ROOT: $root"
Write-Host "COMMAND: $python $($arguments -join ' ')"
Write-Host "LOG: $log"
$process = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -RedirectStandardOutput $log -RedirectStandardError (Join-Path $folder 'pytest_stderr.log') -NoNewWindow -PassThru -Wait
Set-Content -Path $status -Value ([string]$process.ExitCode) -Encoding ascii
Get-Content -Path $log -Tail 40
if (Test-Path (Join-Path $folder 'pytest_stderr.log')) { Get-Content (Join-Path $folder 'pytest_stderr.log') -Tail 15 }
Write-Host "EXIT_CODE: $($process.ExitCode)"
if ($process.ExitCode -ne 0) { Write-Host 'Full active test suite did not pass; consult logs.' }
