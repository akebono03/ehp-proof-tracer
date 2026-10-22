$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root
python ".\phase168_r2_toda52_transport\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest ".\phase168_r2_toda52_transport\tests\test_phase168_r2_toda52_transport.py" -q --tb=short
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -c "from phase165_r55_nk_only_goal import search_group_from_registered_goal; r=search_group_from_registered_goal(n=2,k=2); print('ACTIVE_STATUS:',r.status); print('PROVEN:',len(r.proven_steps)); print('OPEN:',len(r.open_goals)); print('DIAGNOSTICS:',r.diagnostics)"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
