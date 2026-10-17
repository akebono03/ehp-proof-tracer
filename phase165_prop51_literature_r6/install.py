"""Guarded Phase 165 installer, upgrading previously installed R5 metadata."""
from __future__ import annotations
import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent

def main() -> None:
    ordered = ROOT / 'phase165_prop51_claim_order.py'
    registration = ROOT / 'phase165_r52_r13_reference_registration.py'
    if not ordered.is_file():
        subprocess.run([sys.executable, str(PACKAGE / 'r5_base' / 'install.py')], check=True)
    if not ordered.is_file() or not registration.is_file():
        raise SystemExit('Required files missing; no changes made')
    old = ordered.read_text(encoding='utf-8-sig')
    if 'OrderedProp51Item(4, "pi4_3_group_goal", "GOAL", pi4_3_goal())' not in old and 'OrderedProp51Item(4, "pi4_3_group_relation", "LITERATURE", pi4_3_goal())' not in old:
        raise SystemExit('UNEXPECTED R5 claim layout; no changes made')
    new = old.replace('"""Ordered Proposition 5.1 items: literature clauses plus one proof goal.\n\nThe fourth item is a goal, not an adopted literature claim or GIVEN step.\n"""', '"""Five ordered adopted literature claims; registration is not a proof certificate."""')
    new = new.replace('"""Return the complete five-position inventory without certifying the goal."""', '"""Return the five source-adopted claim positions; not a proof certificate."""')
    new = new.replace('OrderedProp51Item(4, "pi4_3_group_goal", "GOAL", pi4_3_goal())','OrderedProp51Item(4, "pi4_3_group_relation", "LITERATURE", pi4_3_goal())')
    new = new.replace('"""The unique explicitly adopted intermediate proof target, not a proof."""','"""Return the typed fourth claim as a target, not as established proof."""')
    reg = registration.read_text(encoding='utf-8-sig')
    anchor = '''    return register_adopted_composite_reference(
        assertion_id="toda:adopted:prop5.1:finite_dimensional",
        locator="Proposition 5.1",
        source_id="Toda translated TeX:Proposition 5.1 (user-adopted; original edition unverified)",
        content=content,
    )'''
    replacement = '''    bridge = register_adopted_composite_reference(
        assertion_id="toda:adopted:prop5.1:finite_dimensional",
        locator="Proposition 5.1",
        source_id="Toda translated TeX:Proposition 5.1 (user-adopted; original edition unverified)",
        content=content,
    )
    # A separately typed fourth literature claim, ordered before higher eta.
    # NO proof link: internal reconstruction must not cite its own conclusion.
    from phase165_prop51_claim_order import pi4_3_goal
    bridge.registry.add_assertion(AssertionEntry(
        assertion_id="toda:adopted:prop5.1:pi4_3",
        reference_id="adopted:toda:adopted:prop5.1:finite_dimensional",
        kind=AssertionKind.STATEMENT,
        content=pi4_3_goal(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=4,
        scope=("user_adopted_claim_without_given_proof",),
    ))
    return bridge'''
    if 'assertion_id="toda:adopted:prop5.1:pi4_3"' not in reg:
        if anchor not in reg:
            raise SystemExit('UNEXPECTED registration function; no changes made')
        reg = reg.replace(anchor,replacement,1)
    if 'AssertionOrigin' not in reg.split('def build_adopted_prop51_reference')[0]:
        reg=reg.replace('AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,', 'AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,')
        if 'AssertionOrigin' not in reg.split('def build_adopted_prop51_reference')[0]:
            reg=reg.replace('AssertionEntry, AssertionKind, LiteratureEntry,','AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,',1)
    ast.parse(new);ast.parse(reg)
    updates=((ordered,new),(registration,reg))
    for path,text in updates:
        if path.read_text(encoding='utf-8-sig')!=text:
            backup=path.with_name(path.name+'.prop51_literature_r6.bak')
            if not backup.exists():shutil.copy2(path,backup)
            path.write_text(text,encoding='utf-8')
    print(json.dumps({'status':'INSTALLED','claim_count':5,'position_4':'LITERATURE','position_4_given_link':False,'full_pytest_run':False}))

if __name__=='__main__':main()
