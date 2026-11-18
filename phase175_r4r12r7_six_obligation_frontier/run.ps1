param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python -m pytest -q phase175_r4r12r7_six_obligation_frontier/tests/test_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R7 focused pytest failed' }
$arguments = @('-m', 'phase175_r4r12r7_six_obligation_frontier.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { throw 'R4R12R7 six-obligation audit failed' }
