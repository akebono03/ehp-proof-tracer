$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -B ".\phase162_r4_b3_reference_correction\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'Dedicated branch correction failed.' }
python -B -m pytest -q ".\phase162_r4_b3_reference_correction\tests\test_phase162_r4_b3_reference_correction.py"
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed.' }
python -B ".\phase162_r4_b3_full_text_check\check_phase162_r4_b3_full_text.py"
if ($LASTEXITCODE -ne 0) { throw 'Common renderer full-text audit failed.' }
Write-Host 'Common renderer restoration and audit complete; full suite not run.'
