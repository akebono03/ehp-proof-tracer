$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $project
$env:PYTHONPATH = "$project;$PSScriptRoot"
$testDir = '.\phase165_r5_r17_r1_runner_recovery_fix'
python -m pytest -q "$testDir\test_installer.py" "$testDir\test_recovery.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R17-R1 installer tests failed before deletion.' }
python "$testDir\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R17-R1 preflight failed; no deletion performed.' }
python -m pytest -q "$testDir\test_canonical_smoke.py"
if ($LASTEXITCODE -ne 0) {
    python "$testDir\restore.py"
    throw 'R5-R17-R1 canonical Renderer regression failed. Deleted files restored.'
}
Write-Host 'R5-R17-R1 old Renderer modules removed; canonical smoke tests PASS; full pytest NOT run.'
