$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q .\phase163_r4_r16_semantic_review\tests\test_review.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$source = '.\phase163_r4_r15_chapter1\Toda_01.tex'
if (-not (Test-Path $source)) { throw 'R4-R15 source TeX not found. Install the R4-R15 package first.' }
python -B -m phase163_r4_r16_semantic_review.review --source $source --output .\phase163_r4_r16_output --legacy .\toda_literature_statement_boundary.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R4-R16 review queue created. Existing project unchanged; full suite not run.'
