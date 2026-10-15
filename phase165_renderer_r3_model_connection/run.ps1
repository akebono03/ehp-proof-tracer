$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $project } else { "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
$baseline = Join-Path $package 'baseline.json'
& $python (Join-Path $package 'snapshot.py') before $baseline
if ($LASTEXITCODE -ne 0) { throw 'R3 baseline failed; no changes made' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R3 installation failed' }
& $python -m pytest -q (Join-Path $package 'test_r3.py')
$code = $LASTEXITCODE
if ($code -eq 0) {
    & $python (Join-Path $package 'snapshot.py') after $baseline
    $code = $LASTEXITCODE
}
if ($code -ne 0) {
    Write-Output 'R3 regression; restoring two files'
    & $python (Join-Path $package 'restore.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3 rollback failed; inspect .phase165_renderer_r3_backup' }
    throw 'R3 targeted test or exact Markdown regression; original files restored'
}
Write-Output 'R3 shared model entry connected; 7 targeted tests passed; full pytest NOT run.'
