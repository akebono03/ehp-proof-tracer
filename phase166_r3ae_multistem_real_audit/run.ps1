$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r55_nk_only_goal.py')) {
    throw 'Run from EHP Proof Tracer repository root.'
}
python -m phase166_r3ae_multistem_real_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AE audit execution failed' }
python -m pytest -q phase166_r3ae_multistem_real_audit/test_r3ae.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AE focused tests failed' }
Write-Host 'R3-AE read-only audit complete; full pytest NOT run.'
