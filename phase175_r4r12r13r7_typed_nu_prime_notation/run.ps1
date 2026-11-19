param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$arguments = @('-m', 'phase175_r4r12r13r7_typed_nu_prime_notation.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q --import-mode=importlib phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
