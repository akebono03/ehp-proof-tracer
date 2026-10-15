$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
python ".\phase165_r5_r15_deduplicate_legacy_ehp\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R15 guarded installation failed' }
python -m pytest -q ".\phase165_r5_r15_deduplicate_legacy_ehp\test_r5_r15.py"
if ($LASTEXITCODE -ne 0) {
    python ".\phase165_r5_r15_deduplicate_legacy_ehp\restore.py"
    throw 'R5-R15 focused regression failed; application source rolled back.'
}
python -m pytest -q ".\tests\test_phase162_r5_6_narrative_final_format.py" -k "prose_uses_ascii or group_conclusion_only"
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Targeted tests failed; restoring original application code.'
    python ".\phase165_r5_r15_deduplicate_legacy_ehp\restore.py"
    throw 'R5-R15 targeted regression failed; application source rolled back.'
}
Write-Host 'R5-R15 targeted tests PASS; duplicate legacy EHP construction removed. Legacy renderer remains; full pytest NOT run.'
