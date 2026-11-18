param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python -m pytest -q phase175_r4r12r6_public_candidate_trace/tests/test_trace.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R6 focused pytest failed' }
$argsList = @('-m', 'phase175_r4r12r6_public_candidate_trace.trace', '--root', $root)
if ($DryRun) { $argsList += '--dry-run' }
python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R6 read-only trace failed' }
