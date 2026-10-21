$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
Set-Location $project
python -m phase166_r3aa_publication_runtime_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AA runtime audit incomplete or failed: inspect report.json' }
python -m pytest -q phase166_r3aa_publication_runtime_audit/tests/test_r3aa_guards.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AA targeted tests failed' }
Write-Host 'R3-AA PASS; full pytest not run.'
