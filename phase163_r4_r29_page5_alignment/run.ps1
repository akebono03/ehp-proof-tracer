$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q '.\phase163_r4_r29_page5_alignment\tests\test_align.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = Join-Path $root 'phase163_r4_r28_output\Toda_01_corrected.tex'
$ledger = Join-Path $root 'phase163_r4_r28_output\page_ledger.json'
if (-not (Test-Path $source)) { throw 'R4-R28 corrected TeX missing.' }
if (-not (Test-Path $ledger)) { throw 'R4-R28 page ledger missing.' }
python -B -m phase163_r4_r29_page5_alignment.align --source "$source" --ledger "$ledger" --output '.\phase163_r4_r29_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R29 page 5 partial alignment complete. Full suite not run.'
