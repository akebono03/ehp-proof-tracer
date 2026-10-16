"""Install a source-anchored generic premise expansion in the shared provider."""
from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / 'phase165_r52_r9_shared_math.py'
MODULE = ROOT / 'phase165_r6_2_r4_seeded_goals.py'
LOCAL_MODULE = Path(__file__).with_name(MODULE.name)
MARKER = '    # R6-2 R4: cited source anchors bind otherwise unknown premise variables.'
INSERT = '''    # R6-2 R4: cited source anchors bind otherwise unknown premise variables.
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
    from phase165_r8_rule_provider import discover_inference_rules as _discover_seeded_rules
    seeded_rules, _seeded_report = _discover_seeded_rules()
    seeded_steps = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
    )
'''
OLD = '        return retain_ordered_root_expansions(proof_target, goal, merged)'
NEW = '''        try:
            seeded_options = generate_seeded_backward_goals(
                goal, seeded_rules, seeded_steps, max_candidates=2048,
            )
        except ValueError as exc:
            if str(exc) != "seeded backward search budget exceeded":
                raise
            seeded_options = ()
        merged = merge_backward_expansions(merged, seeded_options)
        return retain_ordered_root_expansions(proof_target, goal, merged)'''


def main():
    if not SHARED.is_file() or not LOCAL_MODULE.is_file():
        raise RuntimeError('Missing shared provider or R4 module')
    old = SHARED.read_text(encoding='utf-8-sig')
    tree = ast.parse(old)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'shared_expansion_provider']
    if len(nodes) != 1:
        raise RuntimeError('Expected one shared_expansion_provider')
    if MARKER in old:
        print(json.dumps({'status':'ALREADY_CONNECTED','full_pytest_run':False}))
        return
    anchor = '    generic_provider = build_generic_backward_expansion_provider()'
    if old.count(anchor) != 1 or old.count(OLD) != 1:
        raise RuntimeError('Shared provider changed, refusing to patch')
    if 'reverse_rules_from_witnesses' not in old:
        raise RuntimeError('R6-2 R3 must be installed first')
    if MODULE.exists() and MODULE.read_bytes() != LOCAL_MODULE.read_bytes():
        raise RuntimeError('Conflicting existing R4 module')
    revised = old.replace(anchor, anchor+'\n\n'+INSERT.rstrip('\n')).replace(OLD, NEW)
    ast.parse(revised)
    if not MODULE.exists():
        shutil.copy2(LOCAL_MODULE, MODULE)
    backup = SHARED.with_name(SHARED.name+'.r6_2_r4_before.bak')
    if not backup.exists():
        shutil.copy2(SHARED,backup)
    SHARED.write_text(revised, encoding='utf-8')
    print(json.dumps({'status':'CONNECTED','modified':SHARED.name,'added':MODULE.name,
                     'pi43_adapter_retained':True,'full_pytest_run':False},indent=2))


if __name__ == '__main__':
    main()
