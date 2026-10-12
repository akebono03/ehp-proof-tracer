$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$r77 = Join-Path $root 'phase163_r4_r77_output\proof_ownership.json'
$r75 = Join-Path $root 'phase163_r4_r75_output\ownership_proposals.json'
if (-not (Test-Path -LiteralPath $r77 -PathType Leaf)) { throw "Missing R77 input: $r77" }
if (-not (Test-Path -LiteralPath $r75 -PathType Leaf)) { throw "Missing R75 input: $r75" }
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r78_registry_preview\tests\test_phase163_r4_r78_registry_preview.py'
if ($LASTEXITCODE -ne 0) { throw 'R78 focused pytest failed' }
python '.\phase163_r4_r78_registry_preview\phase163_r4_r78_registry_preview.py' --r77 $r77 --r75 $r75 --output '.\phase163_r4_r78_output'
if ($LASTEXITCODE -ne 0) { throw 'R78 preview failed' }
Write-Output 'R78 complete. No production changes. Full pytest not run.'
