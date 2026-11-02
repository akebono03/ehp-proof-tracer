param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
Write-Output 'PHASE173_R4_R1_DIAGONAL_OFFLINE_PYTEST_START'
python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_install.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal install tests failed' }
if ($DryRun) {
    python -m phase173_r4_r1_diagonal_inference_fix.install --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal preflight failed' }
    exit 0
}
python -m phase173_r4_r1_diagonal_inference_fix.install --root $Root
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal installer failed' }
Write-Output 'PHASE173_R4_R1_DIAGONAL_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider `
  phase173_r4_r1_diagonal_inference_fix/tests/test_scoped_diagonal.py `
  phase173_r4_r1_source_bound_56/tests/test_rule.py `
  phase173_r4_r1_lemma54_source_bridge/tests/test_source.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 focused verification failed' }
python -m phase173_r4_r1_diagonal_inference_fix.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 checked proof is incomplete' }
Write-Output 'PHASE173_R4_R1_DIAGONAL_INSTALL_AND_PROOF=PASS'
