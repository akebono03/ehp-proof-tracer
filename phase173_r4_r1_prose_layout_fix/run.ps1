param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
Write-Output 'PHASE173_R4_R1_PROSE_OFFLINE_PYTEST_START'
python -m pytest -q -p no:cacheprovider --import-mode=importlib phase173_r4_r1_prose_layout_fix/tests/test_install.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 prose offline tests failed' }
if ($DryRun) {
    python -m phase173_r4_r1_prose_layout_fix.install --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 prose DryRun failed' }
    exit 0
}
python -m phase173_r4_r1_prose_layout_fix.install --root $Root
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 prose installation failed' }
Write-Output 'PHASE173_R4_R1_PROSE_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider --import-mode=importlib `
    phase173_r4_r1_prose_layout_fix/tests/test_install.py `
    phase173_r4_r1_prose_layout_fix/tests/test_live.py `
    phase173_r4_r1_narrative_source_fix/tests/test_live.py `
    phase173_r4_r1_alpha_literal_fix/tests/test_live.py `
    phase173_r4_r1_alpha_literal_fix/tests/test_install.py `
    phase173_r4_r1_source_bound_56/tests/test_rule.py `
    phase173_r4_r1_lemma54_source_bridge/tests/test_source.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 prose focused pytest failed' }
python -m phase173_r4_r1_narrative_source_fix.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 revised narrative verifier failed' }
python -m phase173_r4_r1_alpha_literal_fix.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 alpha verifier failed' }
python -m phase173_r4_r1_prose_layout_fix.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 prose verification failed' }
Write-Output 'PHASE173_R4_R1_PROSE_INSTALL_AND_PROOF=PASS'
