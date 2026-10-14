$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$Package\prune.py" --root "$Root" --output "$Package" --apply
if ($LASTEXITCODE -ne 0) { throw 'R27-R20 guarded removal failed' }
python -m pytest -q "$Package\test_prune.py"
if ($LASTEXITCODE -ne 0) { throw 'R27-R20 targeted tests failed' }
Write-Host 'R27-R20 complete; removed backups preserved in removed_files_backup; full pytest NOT run.'
