from __future__ import annotations
import ast
from pathlib import Path
import phase165_r52_r9_shared_math as shared

ROOT = Path(__file__).resolve().parent.parent

def test_live_shared_provider_has_no_pi43_adapter():
    source = (ROOT / 'phase165_r52_r9_shared_math.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    assert not any(isinstance(n, ast.Name) and n.id == 'expand_existing_pi43_rules' for n in ast.walk(tree))
    assert callable(shared.shared_expansion_provider)

def test_pi43_adapter_module_is_removed():
    assert not (ROOT / 'phase165_r52_r23_existing_rule_adapter.py').exists()

def test_common_provider_still_exposes_rule_discovery():
    source = (ROOT / 'phase165_r52_r9_shared_math.py').read_text(encoding='utf-8')
    assert 'build_generic_backward_expansion_provider' in source
    assert 'reverse_rules_from_witnesses' in source
    assert 'generate_seeded_backward_goals' in source
