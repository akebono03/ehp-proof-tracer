from pathlib import Path
import ast
from install import NAMES

ROOT=Path(__file__).resolve().parent.parent

def test_specialized_factories_removed():
    tree=ast.parse((ROOT/'toda_rules.py').read_text(encoding='utf-8'))
    assert all(n.name not in NAMES for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))

def test_legacy_consumers_and_catalog_cleared():
    for relative in ('toda_upstream_bootstrap.py','probes/probe_phase49_capabilities.py','standard_production_applicability_catalog.py'):
        source=(ROOT/relative).read_text(encoding='utf-8')
        ast.parse(source)
        assert all(name not in source for name in NAMES),relative

def test_phase50_existing_hopf_source_selected():
    text=(ROOT/'toda_prop56_zero_bootstrap.py').read_text(encoding='utf-8')
    f=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='_build_prop51_step')
    seg=''.join(text.splitlines(keepends=True)[f.lineno-1:f.end_lineno])
    part=seg.split('  eta2_hopf_step = _find_unique_step(',1)[1].split('  delta_step = _find_unique_step(',1)[0]
    assert 'phase50[' in part and '"premise_steps"' in part
    assert 'phase49[' not in part
