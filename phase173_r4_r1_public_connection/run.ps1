param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
Write-Output 'PHASE173_R4_R1_PUBLIC_OFFLINE_PYTEST_START'
python -m pytest -q -p no:cacheprovider phase173_r4_r1_public_connection/tests/test_install.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 public installer tests failed' }
if ($DryRun) {
    python -m phase173_r4_r1_public_connection.install --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 public DryRun failed' }
    exit 0
}
python -m phase173_r4_r1_public_connection.install --root $Root
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 public install failed' }
Write-Output 'PHASE173_R4_R1_PUBLIC_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider `
  phase173_r4_r1_public_connection/tests/test_install.py `
  phase173_r4_r1_source_bound_56/tests/test_rule.py `
  phase173_r4_r1_lemma54_source_bridge/tests/test_source.py `
  phase173_r4_r1_diagonal_inference_fix/tests/test_scoped_diagonal.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 public focused pytest failed' }
python -m phase173_r4_r1_public_connection.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 public verification failed' }
Write-Output 'PHASE173_R4_R1_PUBLIC_INSTALL_AND_PROOF=PASS'
