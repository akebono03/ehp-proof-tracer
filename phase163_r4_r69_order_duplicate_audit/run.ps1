$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$inputFile = Join-Path $root 'phase163_r4_r68_output\unnumbered_reference_proposals.json'
if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf)) {
    throw "Missing R4-R68 input: $inputFile"
}
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r69_order_duplicate_audit\tests\test_phase163_r4_r69_order_duplicate_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed.' }
python '.\phase163_r4_r69_order_duplicate_audit\phase163_r4_r69_order_duplicate_audit.py' --source $inputFile --output '.\phase163_r4_r69_output'
if ($LASTEXITCODE -ne 0) { throw 'Audit failed.' }
Write-Output 'R4-R69 read-only order and duplicate audit complete. Full pytest not run.'
