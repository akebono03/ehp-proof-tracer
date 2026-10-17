$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Split-Path -Parent $Root
Set-Location $Repo
$env:PYTHONPATH = "$Root;$Repo"
python "$Root\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$Root\tests\test_r12_gap_audit.py" "tests\test_phase165_r11_wiring.py" "tests\test_phase165_r8_rule_provider.py"
exit $LASTEXITCODE
