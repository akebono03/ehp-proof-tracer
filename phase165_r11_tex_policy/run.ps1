$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Files = @(
    @{ Source = 'phase165_tex_citation_policy.py'; Dest = 'phase165_tex_citation_policy.py' },
    @{ Source = 'phase165_r9_production_wiring.py'; Dest = 'phase165_r9_production_wiring.py' },
    @{ Source = 'tests/test_phase165_tex_citation_policy.py'; Dest = 'tests/test_phase165_tex_citation_policy.py' },
    @{ Source = 'tests/test_phase165_r11_wiring.py'; Dest = 'tests/test_phase165_r11_wiring.py' }
)
foreach ($File in $Files) {
    $src = Join-Path $PSScriptRoot $File.Source
    if (-not (Test-Path $src)) { throw "Package file missing: $src" }
    $dest = Join-Path $Root $File.Dest
    $dir = Split-Path -Parent $dest
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    if (Test-Path $dest) { Copy-Item $dest "$dest.phase165_r11_backup" -Force }
    Copy-Item $src $dest -Force
}
$manifest = Join-Path $Root 'phase163_r4_r94_output/manifest.json'
if (-not (Test-Path $manifest)) { throw "Source manifest missing: $manifest" }
python -m py_compile 'phase165_tex_citation_policy.py' 'phase165_r9_production_wiring.py'
if ($LASTEXITCODE -ne 0) { throw 'Syntax check failed' }
python -m pytest -q 'tests/test_phase165_tex_citation_policy.py' 'tests/test_phase165_r11_wiring.py' 'tests/test_phase165_r9_production_wiring.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
python -c "from phase165_r9_production_wiring import discover_goal_search_inputs; from phase165_tex_citation_policy import assess_adopted_tex_citation; x=discover_goal_search_inputs(); ids=[a.assertion_id for a in x.bridge.registry._assertions.values() if a.assertion_id.startswith('phase163:archive:')]; assert len(ids)==117, len(ids); allowed=sum(assess_adopted_tex_citation(x.bridge, i).usable_as_reference for i in ids); print('Adopted TeX reference citations:',allowed,'/ 117; typed proof auto-approval: 0; full pytest NOT run')"
if ($LASTEXITCODE -ne 0) { throw 'Production TeX citation audit failed' }
