$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$source = Join-Path $root 'phase163_r4_r63_output\source_boundaries.json'
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing R4-R63 source-span audit: $source" }
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r64_reference_assertion_split\tests\test_phase163_r4_r64_reference_assertion_split.py'
if ($LASTEXITCODE -ne 0) { throw 'R4-R64 focused pytest failed.' }
python '.\phase163_r4_r64_reference_assertion_split\phase163_r4_r64_reference_assertion_split.py' --source $source --output '.\phase163_r4_r64_output'
if ($LASTEXITCODE -ne 0) { throw 'R4-R64 split audit failed.' }
Write-Output 'R4-R64 split proposal complete. No production changes. Full pytest not run.'
