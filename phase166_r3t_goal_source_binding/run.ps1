$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3t_goal_source_binding.apply
    if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
    python -m pytest -q phase166_r3t_goal_source_binding/test_connection.py test_phase165_r55_nk_only_goal.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed; restore backup before proceeding' }
    Write-Host 'R3-T source binding targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
