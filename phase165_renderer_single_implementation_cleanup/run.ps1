$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
# Python adds the script directory (the installer subfolder) to sys.path.
# Explicitly expose the project root to every child interpreter.
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) {
  $project
} else {
  "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH"
}
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
$baseline = Join-Path $package 'narrative_before.json'
& $python (Join-Path $package 'snapshot.py') before $baseline
if ($LASTEXITCODE -ne 0) { throw 'Pre-install Narrative snapshot failed. Nothing changed.' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Renderer cleanup installation failed.' }
& $python -m pytest -q (Join-Path $package 'test_cleanup.py')
$testExit = $LASTEXITCODE
if ($testExit -eq 0) {
  & $python (Join-Path $package 'snapshot.py') after $baseline
  $testExit = $LASTEXITCODE
}
if ($testExit -ne 0) {
  Write-Output 'Cleanup regression detected; restoring original renderer files.'
  & $python (Join-Path $package 'restore.py')
  if ($LASTEXITCODE -ne 0) { throw 'Regression found and automatic restore FAILED. Inspect backup directory.' }
  throw 'Targeted regression or exact Narrative comparison failed; original files restored.'
}
Write-Output 'Duplicate renderer implementation retired. 5 targeted tests passed; exact Narrative outputs unchanged. Full pytest NOT run.'
