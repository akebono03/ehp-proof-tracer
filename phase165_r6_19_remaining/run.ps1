$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python -m pytest -q (Join-Path $PSScriptRoot 'test_apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R6-19 package tests failed; no changes made' }
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R6-19 apply failed; inspect files and backup' }
python -m pytest -q tests/test_phase164_r5_r1_common_renderer.py tests/test_phase157_r2_literature_statement_boundary.py tests/test_phase150_rc4_5b_3_r1_beta_latex.py tests/test_phase148_rc2_4_repair_r4_1_r1.py tests/test_proof_repository.py
if ($LASTEXITCODE -ne 0) { throw 'R6-19 targeted tests failed; full pytest NOT run' }
Write-Host 'R6-19 targeted tests PASS. Reference selection case held for separate judgement. Full pytest NOT run.'
