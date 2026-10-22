$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase168_r2_4_nk_citation_binding\apply.py"
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q ".\phase168_r2_4_nk_citation_binding\test_binding.py" ".\phase166_r3t_goal_source_binding\test_connection.py"
    if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
    python -c "from phase165_r52_r9_shared_math import build_shared_typed_bridge; from phase165_r55_nk_only_goal import registered_group_goal_candidates; from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id; b=build_shared_typed_bridge(); [(print(f'n={n} k={k} matches=',[(resolve_specialized_goal_citing_id(b,g)) for g in registered_group_goal_candidates(b,n=n,k=k)])) for n,k in [(2,1),(3,1),(2,2),(3,2),(4,2),(5,2),(4,1)]]"
    if ($LASTEXITCODE -ne 0) { throw "Bridge audit failed" }
} finally { Pop-Location }
