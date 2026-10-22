$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $package
Set-Location $repo
python "$package\patch.py"
if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
python -m pytest "$package\test_phase167_r4_9.py" -q
if ($LASTEXITCODE -ne 0) { throw "R4-9 limited test failed" }
python -m pytest ".\phase167_r4_6_unified_reference_proof_newline_fix\test_phase167_r4_6_unified_reference_proof.py" -q
if ($LASTEXITCODE -ne 0) { throw "R4-6 regression failed" }
Write-Host "Focused checks done; full suite not run."
