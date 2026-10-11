$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q .\phase163_r4_r15_chapter1\tests\test_inventory.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = '.\phase163_r4_r15_chapter1\Toda_01.tex'
$legacy = '.\toda_literature_statement_boundary.py'
python -B -m phase163_r4_r15_chapter1.inventory --source $source --output '.\phase163_r4_r15_output' --legacy $legacy
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R4-R15 inventory generated. Existing project unchanged; full suite not run.'
