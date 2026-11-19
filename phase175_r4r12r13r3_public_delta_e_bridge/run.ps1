param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$argsPython = @('-m', 'phase175_r4r12r13r3_public_delta_e_bridge.audit', '--root', $root)
if ($DryRun) { $argsPython += '--dry-run' }
python @argsPython
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
