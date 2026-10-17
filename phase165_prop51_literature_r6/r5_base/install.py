"""Guarded local installer; preserves previously applied Phase 165 changes."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent.parent
PACKAGE = Path(__file__).resolve().parent
FILES = {
    'phase165_r52_r13_reference_registration.py': ('def build_adopted_prop51_reference()',),
    'phase165_r57_r16_web_proof_order.py': ('def resolve_reviewed_order_catalog(',),
}

def main():
    for name, markers in FILES.items():
        path = ROOT / name
        if not path.is_file():
            raise SystemExit('MISSING: ' + name)
        value = path.read_text(encoding='utf-8-sig')
        if any(marker not in value for marker in markers):
            raise SystemExit('SOURCE_MISMATCH: ' + name)
    target = ROOT / 'phase165_prop51_claim_order.py'
    source = (PACKAGE / target.name).read_text(encoding='utf-8')
    if target.exists() and target.read_text(encoding='utf-8') != source:
        raise SystemExit('CONFLICT: ' + target.name)
    edits = {}
    registration = ROOT / 'phase165_r52_r13_reference_registration.py'
    data = registration.read_text(encoding='utf-8-sig')
    anchor = 'def build_adopted_prop51_reference() -> RegistryBridgeResult:'
    prefix = '''def registered_prop51_items():
    """List all five proposition positions; position four remains an unproved GOAL."""
    from phase165_prop51_claim_order import ordered_prop51_items
    bridge = build_adopted_prop51_reference()
    content = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional").content
    return ordered_prop51_items(content)


'''
    if 'def registered_prop51_items():' not in data:
        data = data.replace(anchor, prefix + anchor, 1)
    edits[registration] = data
    order = ROOT / 'phase165_r57_r16_web_proof_order.py'
    data = order.read_text(encoding='utf-8-sig')
    before = '''        candidates = registered_group_goal_candidates(
            bridge, n=source_n, k=source_k,
        )
'''
    after = '''        candidates = registered_group_goal_candidates(
            bridge, n=source_n, k=source_k,
        )
        from phase165_prop51_claim_order import prop51_intermediate_goal
        declared_goal = prop51_intermediate_goal(n=source_n, k=source_k)
        if declared_goal is not None:
            # The intermediate target is goal metadata, NEVER a GIVEN premise.
            candidates = (declared_goal,)
'''
    if 'declared_goal = prop51_intermediate_goal' not in data:
        if before not in data:
            raise SystemExit('ANCHOR_MISMATCH: ' + order.name)
        data = data.replace(before, after, 1)
    edits[order] = data
    for path, data in edits.items():
        ast.parse(data, filename=str(path))
    ast.parse(source)
    for path, data in edits.items():
        old = path.read_text(encoding='utf-8-sig')
        if old != data:
            bak = path.with_name(path.name + '.prop51_order_r5.bak')
            if not bak.exists():
                shutil.copy2(path, bak)
            path.write_text(data, encoding='utf-8')
    if not target.exists():
        target.write_text(source, encoding='utf-8')
    print(json.dumps({'status':'INSTALLED','ordered_positions':5,'goal_at_position':4,'given_promoted':False,'full_pytest_run':False}))

if __name__ == '__main__':
    main()
