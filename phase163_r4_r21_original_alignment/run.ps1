$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q .\phase163_r4_r21_original_alignment\tests\test_align.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = Join-Path $PSScriptRoot 'Toda_01.tex'
python -B -m phase163_r4_r21_original_alignment.align --source "$source" --output '.\phase163_r4_r21_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R21: corrected TeX and review report created. No production code changed. Full suite not run.'
