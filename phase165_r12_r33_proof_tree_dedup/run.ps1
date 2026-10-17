$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
Set-Location $project
$env:PYTHONPATH = $project + [IO.Path]::PathSeparator + $env:PYTHONPATH
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q "$PSScriptRoot\test_phase165_r12_r33_proof_tree_dedup.py" "tests\test_map_property_rules.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot\audit.py"
exit $LASTEXITCODE
