$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python '.\phase167_r5_beta_test_fix\patch.py'
if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
python -m pytest tests/test_phase150_rc4_5b_3_r1_beta_latex.py -q --tb=short
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Host 'Focused pytest PASS. The full suite was not rerun.'
