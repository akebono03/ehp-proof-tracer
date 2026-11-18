param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$env:PYTHONPATH = $root
python -m pytest -q phase175_r4r12r4_generator_endpoint_audit/tests/test_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R4 focused pytest failed' }
$argsList = @('--root', $root)
if ($DryRun) { $argsList += '--dry-run' }
python -m phase175_r4r12r4_generator_endpoint_audit.audit @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R4 read-only audit failed' }
