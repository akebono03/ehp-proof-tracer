$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q "$PSScriptRoot\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R9 audit tests failed' }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R9 audit preflight failed: inspect audit_output\review.md' }
Write-Host 'R5-R9 dependency decisions recorded. REVIEW REQUIRED. No application source changed; full pytest NOT run.'
