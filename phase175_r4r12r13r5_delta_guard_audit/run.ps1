param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$arguments = @('-m', 'phase175_r4r12r13r5_delta_guard_audit.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q --import-mode=importlib phase175_r4r12r13r5_delta_guard_audit/tests/test_r13r5_delta_diagnostics.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
