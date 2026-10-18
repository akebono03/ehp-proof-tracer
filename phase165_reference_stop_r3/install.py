from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r3_recursive_search.py"
OLD = """            if completed_internal_proofs:
                from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
                internal = find_reusable_internal_proof(target, goal, completed_internal_proofs)
                if internal is not None:
                    solved.append((target, internal))
                    report("proved", target, internal)
                    return internal
            if lookup_mode == "typed_reference_ordered":
"""
NEW = """            if lookup_mode == "typed_reference_ordered":
"""
ANCHOR = """            expansions = expansion_provider(target)
"""
BLOCK = """            if completed_internal_proofs:
                from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
                internal = find_reusable_internal_proof(target, goal, completed_internal_proofs)
                if internal is not None:
                    solved.append((target, internal))
                    report("proved", target, internal)
                    return internal
"""
MARKER = "# phase165_reference_stop_r3: direct eligible source before prior internal proof"

def install() -> None:
    source = TARGET.read_text(encoding="utf-8")
    if MARKER in source:
        print("R3 already installed")
        return
    if source.count(OLD) != 1 or source.count(ANCHOR) != 1:
        raise RuntimeError("Unexpected upstream search function; no patch applied")
    updated = source.replace(OLD, NEW, 1)
    old_stop = """                report("proved", target, step)
                return step
            expansions = expansion_provider(target)
"""
    new_stop = """                report("proved", target, step)
                return step
            """ + MARKER + """
""" + BLOCK + """            expansions = expansion_provider(target)
"""
    if updated.count(old_stop) != 1:
        raise RuntimeError("Expected typed-reference stop not found")
    updated = updated.replace(old_stop, new_stop, 1)
    ast.parse(updated)
    original=ast.parse(source)
    changed=ast.parse(updated)
    def signatures(tree):
        return [(node.name,ast.dump(node.args)) for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))]
    if signatures(original)!=signatures(changed):
        raise RuntimeError("Public API change rejected")
    backup=TARGET.with_suffix(".phase165_reference_stop_r3_backup.py")
    if backup.exists():
        raise RuntimeError("Backup already exists; manual review required")
    backup.write_text(source,encoding="utf-8")
    TARGET.write_text(updated,encoding="utf-8")
    tree=ast.parse(updated)
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="reconstruct_registered_goal")
    lines=updated.splitlines()
    body="\n".join(lines[function.lineno-1:function.end_lineno])
    (Path(__file__).parent/"CHANGED_CODE.md").write_text("# 変更後の関数全文\n\n変更対象: `phase165_r3_recursive_search.py` の `reconstruct_registered_goal()`。import 変更なし。\n\n```python\n"+body+"\n```\n",encoding="utf-8")
    print("Changed:",TARGET)
    print("Backup:",backup)
    print("Full function: phase165_reference_stop_r3/CHANGED_CODE.md")

if __name__=="__main__":
    install()
