from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R34 = "phase165_r14_r34_backward_search.py"
R35 = "phase165_r14_r35_leaf_binding.py"
R36 = "phase165_r14_r36_adopted_backward.py"
R38 = "phase165_r14_r38_direct_registry.py"
LEGACY_NAMES = {
    "pi32_goal", "phase165_r34_expansions", "backward_leaf_goals",
    "reconstruct_registered_pi32", "reconstruct_adopted_tex_goal",
    "trace_goal_frontier", "audit_r34", "audit_r35", "audit_r36",
    "audit_completion",
}
CHANGES = {}
REMOVALS = set()

def parse(src, name):
    return ast.parse(src,filename=name)

def remove_definitions(source, names, name):
    lines=source.splitlines(keepends=True)
    tree=parse(source,name)
    ranges=[]
    found=set()
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.name in names:
            start=node.lineno
            if start>1 and lines[start-2].lstrip().startswith("@"):
                start-=1
            ranges.append((start,node.end_lineno))
            found.add(node.name)
    if found!=names:
        raise RuntimeError(f"{name}: expected definitions {sorted(names)}, found {sorted(found)}")
    for a,b in reversed(ranges):
        lines[a-1:b]=[]
    return "".join(lines)

def remove_imports(source, forbidden, name):
    lines=source.splitlines(keepends=True)
    tree=parse(source,name)
    for node in sorted((x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom))),key=lambda x:x.lineno,reverse=True):
        if isinstance(node,ast.ImportFrom):
            if node.module in forbidden:
                del lines[node.lineno-1:node.end_lineno]
                continue
            names={alias.name for alias in node.names}
            to_remove={x for x in names if x in LEGACY_NAMES}
            if to_remove:
                if names == to_remove:
                    del lines[node.lineno-1:node.end_lineno]
                else:
                    keep=[a for a in node.names if a.name not in to_remove]
                    rewritten="from "+node.module+" import "+", ".join(
                        a.name+(" as "+a.asname if a.asname else "") for a in keep
                    )+"\n"
                    lines[node.lineno-1:node.end_lineno]=[rewritten]
    return "".join(lines)

def edit_registry(source):
    name=R38
    if "leaves = backward_leaf_goals(pi32_goal())" in source:
        source=source.replace("    leaves = backward_leaf_goals(pi32_goal())\n","")
        source=source.replace("    steps = adopted_leaf_steps(Path(tex_path))\n",
                              "    steps = adopted_leaf_steps(Path(tex_path))\n    leaves = tuple(step.conclusion for step in steps)\n")
    elif "leaves = tuple(step.conclusion for step in steps)" not in source:
        raise RuntimeError("R38 source registration has unknown leaf join")
    lines=source.splitlines(keepends=True)
    tree=parse(source,name)
    fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=="build_adopted_typed_reference_registry")
    stmts=fn.body
    start=None;end=None
    for i,item in enumerate(stmts):
        if isinstance(item,ast.Expr) and isinstance(item.value,ast.Call) and isinstance(item.value.func,ast.Attribute) and item.value.func.attr=="add_reference":
            if "goal:pi32" in ast.get_source_segment(source,item):
                start=item.lineno
                next_stmt=stmts[i+1]
                if "goal:pi32" not in ast.get_source_segment(source,next_stmt):
                    raise RuntimeError("R38 goal assertion expected after goal reference")
                end=next_stmt.end_lineno
                break
    if start is not None:
        lines[start-1:end]=[]
        source="".join(lines)
    elif '"goal:pi32", ReferenceKind.PROPOSITION' in source:
        raise RuntimeError("R38 unexpected historical goal registration")
    source=remove_definitions(source,{"reconstruct_registered_pi32","audit_completion"},name)
    source=remove_imports(source,{"phase165_r14_r34_backward_search","phase165_r3_recursive_search"},name)
    source=remove_imports(source,set(),name)
    parse(source,name)
    if "pi32_goal(" in source or "phase165_r34_expansions(" in source:
        raise RuntimeError("R38 old goal remains")
    return source

def edit_r35(source):
    name=R35
    source=remove_definitions(source,{"backward_leaf_goals","audit_r35"},name)
    source=remove_imports(source,{"phase165_r14_r34_backward_search"},name)
    parse(source,name)
    return source

def edit_r36(source):
    name=R36
    if "foundation_goal = instantiate_foundational_identity_suspension(1).statement" not in source:
        raise RuntimeError("R36 independent source inventory not installed; refusing destructive migration")
    source=remove_definitions(source,{"reconstruct_adopted_tex_goal","audit_r36"},name)
    source=remove_imports(source,{"phase165_r14_r34_backward_search"},name)
    source=remove_imports(source,set(),name)
    if "backward_leaf_goals(" in source or "pi32_goal(" in source:
        raise RuntimeError("R36 source inventory unexpectedly still depends on old search")
    parse(source,name)
    return source

def active_imports(path):
    tree=parse(path.read_text(encoding="utf-8-sig"),str(path))
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.ImportFrom) and node.module:
            if node.module in {
                "phase165_r14_r34_backward_search",
                "phase165_r14_r37_closure",
                "phase165_r14_r40_replay",
                "phase165_r14_r41_proof_transfer",
            }:
                imports.append(node.module)
    return imports

def main():
    for n in (R34,R35,R36,R38):
        if not (ROOT/n).is_file():
            raise RuntimeError("Missing production file: "+n)
    for name,func in ((R35,edit_r35),(R36,edit_r36),(R38,edit_registry)):
        old=(ROOT/name).read_text(encoding="utf-8-sig")
        CHANGES[name]=func(old)
    REMOVALS.add(R34)

    # Only history-specific tests are retired, never entire shared-test modules.
    history_tests=[
        "phase165_r14_r34_backward_search/test_phase165_r14_r34_backward_search.py",
        "phase165_r14_r35_leaf_binding/test_phase165_r14_r35_leaf_binding.py",
        "phase165_r14_r36_adopted_backward/test_phase165_r14_r36_adopted_backward.py",
        "phase165_r14_r38_direct_registry/test_phase165_r14_r38_direct_registry.py",
    ]
    REMOVALS.update(p for p in history_tests if (ROOT/p).is_file())

    # Remove the single historical replay test from shared tests, preserving
    # the other tests that exercise the active common entry.
    for p in ("test_phase165_r52_r9_shared_math.py",
              "phase165_r52_r9_shared_math/test_phase165_r52_r9_shared_math.py"):
        path=ROOT/p
        if not path.is_file():
            continue
        old=path.read_text(encoding="utf-8-sig")
        if "def test_r9_historical_r38_proof_still_generates" not in old:
            continue
        CHANGES[p]=remove_definitions(old,{"test_r9_historical_r38_proof_still_generates"},p)
    # Guard active root modules: they must no longer import the deleted R34.
    blockers={}
    for p in ROOT.glob("*.py"):
        if p.name in CHANGES or p.name in REMOVALS or "backup" in p.name.lower():
            continue
        imports=active_imports(p)
        if imports:
            blockers[p.name]=imports
    if blockers:
        raise RuntimeError("Active root imports block deletion: "+repr(blockers))
    # Preserve all pre-existing files in the backup; do not silently clobber.
    backup=ROOT/"phase165_r6_1_pi32_retirement_backup"
    all_targets=sorted(set(CHANGES)|REMOVALS)
    for p in all_targets:
        if (backup/p).exists():
            raise RuntimeError("Backup already exists; abort: "+p)
    for p in all_targets:
        if not (ROOT/p).is_file():
            raise RuntimeError("Missing target: "+p)
        (backup/p).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/p,backup/p)
    for p,source in CHANGES.items():
        (ROOT/p).write_text(source,encoding="utf-8")
    for p in sorted(REMOVALS):
        (ROOT/p).unlink()
    print(json.dumps({
        "status":"MIGRATED",
        "modified":sorted(CHANGES),
        "deleted":sorted(REMOVALS),
        "backup":str(backup),
        "full_pytest_run":False,
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
