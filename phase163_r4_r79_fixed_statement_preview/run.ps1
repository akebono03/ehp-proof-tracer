$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$r78 = Join-Path $root 'phase163_r4_r78_output\registry_preview.json'
$sources = Join-Path $root 'phase163_r4_r42_tex_extract\inputs'
if (-not (Test-Path -LiteralPath $r78 -PathType Leaf)) { throw "Missing R78 input: $r78" }
foreach ($name in @('Toda_01_corrected.tex', 'Toda_02_2(2).tex', 'Toda_04_2(2).tex')) {
  if (-not (Test-Path -LiteralPath (Join-Path $sources $name) -PathType Leaf)) { throw "Missing TeX source: $name" }
}
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q '.\phase163_r4_r79_fixed_statement_preview\tests\test_phase163_r4_r79_fixed_statement_preview.py'
if ($LASTEXITCODE -ne 0) { throw 'R79 focused pytest failed' }
python '.\phase163_r4_r79_fixed_statement_preview\phase163_r4_r79_fixed_statement_preview.py' --r78 $r78 --sources $sources --output '.\phase163_r4_r79_output'
if ($LASTEXITCODE -ne 0) { throw 'R79 preview failed' }
Write-Output 'R79 complete. No production changes. Full pytest not run.'
