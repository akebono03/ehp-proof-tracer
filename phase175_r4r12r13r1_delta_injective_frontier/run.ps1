param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$module = 'phase175_r4r12r13r1_delta_injective_frontier.audit'
$arguments = @('-m', $module, '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q phase175_r4r12r13r1_delta_injective_frontier/tests/test_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
