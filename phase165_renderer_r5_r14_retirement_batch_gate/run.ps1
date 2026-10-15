$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$here;$(Split-Path -Parent $here);$env:PYTHONPATH"
python -m pytest -q "$here\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw "R5-R14 audit self-tests failed" }
python "$here\audit.py"
if ($LASTEXITCODE -ne 0) { throw "R5-R14 precondition failed; inspect audit_output\review.md" }
Write-Host "R5-R14 retirement gate recorded. No application code modified; full pytest NOT run."
