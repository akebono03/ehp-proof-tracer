param([switch]$DryRun)
$ErrorActionPreference='Stop'
$root=(Resolve-Path '.').Path
python -m pytest -q phase175_r4r12r5_iterated_suspension_endpoints/tests/test_installer.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 installer tests failed' }
$argsList=@('--root',$root)
if ($DryRun) { $argsList+= '--dry-run' }
python -m phase175_r4r12r5_iterated_suspension_endpoints.audit @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 audit failed' }
if (-not $DryRun) {
    python -m pytest -q phase175_r4r12r5_iterated_suspension_endpoints/tests/test_endpoints.py phase175_r4r3_two_summand_quotient/tests/test_rule.py phase175_r4r12_public_two_summand_quotient/tests/test_provider.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 focused integration tests failed' }
}
