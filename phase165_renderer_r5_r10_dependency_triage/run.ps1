$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$project"
python -m pytest -q "$PSScriptRoot\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R10 scoped audit tests failed' }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R10 dependency triage precheck failed; see audit_output\review.md' }
Write-Host 'R5-R10 dependency ownership triage recorded. No application code changed; full pytest NOT run.'
