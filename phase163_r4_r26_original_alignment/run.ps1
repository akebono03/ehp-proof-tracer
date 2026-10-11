$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q .\phase163_r4_r26_original_alignment\tests\test_align.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = Join-Path $root 'phase163_r4_r25_output\Toda_01_corrected.tex'
if (-not (Test-Path $source)) { throw 'R4-R25 output missing. Run R4-R25 first.' }
python -B -m phase163_r4_r26_original_alignment.align --source "$source" --output '.\phase163_r4_r26_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R26 focused verification complete; full suite not run.'
