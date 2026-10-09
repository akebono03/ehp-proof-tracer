$ErrorActionPreference = 'Stop'
$Repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $Repo 'proof.py'))) {
    throw 'Run this script from the EHP Proof Tracer repository root.'
}
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m phase162_r10_boundary_path_audit.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m pytest -q phase162_r10_boundary_path_audit/tests/test_audit.py
exit $LASTEXITCODE
