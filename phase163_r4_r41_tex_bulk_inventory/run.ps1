$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$here;$repo"
python -m pytest -q "$here\tests\test_phase163_r4_r41_tex_inventory.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$here\phase163_r4_r41_tex_inventory.py" --root "$repo" --output "$repo\phase163_r4_r41_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
