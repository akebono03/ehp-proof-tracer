$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q .\phase163_r4_r27_page_ledger\tests\test_ledger.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = Join-Path $root 'phase163_r4_r26_output\Toda_01_corrected.tex'
if (-not (Test-Path $source)) { throw 'R4-R26 output missing. Run R4-R26 first.' }
python -B -m phase163_r4_r27_page_ledger.ledger --source "$source" --output '.\phase163_r4_r27_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R27 page review ledger generated. No production changes; full suite not run.'
