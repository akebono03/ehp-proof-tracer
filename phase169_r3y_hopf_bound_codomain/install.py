"""Guarded Phase 169 R3Y installation and rollback."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
CORE = Path("phase165_r3_recursive_search.py")
EHP = Path("phase165_r14_r5_ehp_connection.py")
TESTS = (
    Path("phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py"),
    Path("phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py"),
    Path("phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py"),
)
FUNCTIONS = (
    "test_r3i_only_exact_screened_claims_propose_cited_rules",
    "test_r3i_derived_terminal_steps_have_exact_cited_ancestors",
    "test_r3i_historical_inference_only_rules_remain_intact",
    "test_r3i_real_recursive_proof_of_terminal_goals",
)
REPLACEMENTS = {
    CORE: {"reconstruct_registered_goal": PACKAGE / "full_functions/reconstruct_registered_goal_FULL.py"},
    EHP: {"expand_cited_ehp_terminal_goal": PACKAGE / "full_functions/expand_cited_ehp_terminal_goal_FULL.py"},
    **{file: {name: PACKAGE / "full_functions" / (name + "_FULL.py") for name in FUNCTIONS} for file in TESTS},
}


def span(source: str, name: str):
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise ValueError("Missing expected unique function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    return node.lineno, node.end_lineno, "".join(lines[node.lineno-1:node.end_lineno])


def transform(relative: Path, source: str):
    updates = []
    for name, filepath in REPLACEMENTS[relative].items():
        replacement = filepath.read_text(encoding="utf8").rstrip() + "\n"
        tree = ast.parse(replacement)
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef) or tree.body[0].name != name:
            raise ValueError("Invalid full function: " + name)
        start, end, old = span(source, name)
        if name == "reconstruct_registered_goal" and (
            "append_unique_verified_derivation" not in old
            or "expected one registered derivation" not in old
        ):
            raise ValueError("Canonical search contract changed")
        if name == "expand_cited_ehp_terminal_goal" and (
            "derived diagonal" not in old and "derived Hopf codomain" not in old
        ):
            raise ValueError("Missing R3U2 baseline in EHP provider")
        if old.rstrip() != replacement.rstrip():
            updates.append((start, end, replacement))
    lines = source.splitlines(keepends=True)
    for start, end, replacement in sorted(updates, reverse=True):
        lines[start-1:end] = [replacement]
    transformed = "".join(lines)
    if relative == CORE:
        tree = ast.parse(transformed)
        names = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "SourceBoundGoal"]
        if not names:
            goal_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GoalExpansion"]
            if len(goal_nodes) != 1:
                raise ValueError("GoalExpansion location changed")
            cl = (PACKAGE / "full_functions/SourceBoundGoal_FULL.py").read_text(encoding="utf8").rstrip() + "\n\n"
            code = transformed.splitlines(keepends=True)
            code[goal_nodes[0].end_lineno:goal_nodes[0].end_lineno] = ["\n" + cl]
            transformed = "".join(code)
    ast.parse(transformed)
    return transformed


def digest(source):
    return hashlib.sha256(source.encode("utf8")).hexdigest()


def install():
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    print("R3Y_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("Requires develop")
    staged = {}
    for relative in REPLACEMENTS:
        file = ROOT / relative
        if not file.is_file():
            raise FileNotFoundError(str(relative))
        old = file.read_text(encoding="utf-8-sig")
        new = transform(relative, old)
        staged[relative] = (old, new)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    meta = OUTPUT / "installed.json"
    if meta.is_file():
        records = json.loads(meta.read_text(encoding="utf8"))
        if all(str(rel) in records and digest(old) == records[str(rel)]["after"]
               for rel,(old,new) in staged.items()):
            print("R3Y_ALREADY_INSTALLED=True")
            return
        if not all(str(rel) in records and digest(old) == records[str(rel)]["before"]
                   for rel,(old,new) in staged.items()):
            raise RuntimeError("Tracked sources differ from previous installation")
    records = {}
    for relative,(old,new) in staged.items():
        name = str(relative).replace("/", "__").replace("\\", "__")
        (OUTPUT / (name + ".before")).write_text(old, encoding="utf8")
        (OUTPUT / (name + ".FULL.py")).write_text(new, encoding="utf8")
        records[str(relative)] = {"before":digest(old),"after":digest(new),"changed":old != new}
    for relative,(old,new) in staged.items():
        if new != old:
            (ROOT / relative).write_text(new, encoding="utf8")
            print("R3Y_PATCHED=" + str(relative))
    meta.write_text(json.dumps(records, indent=2), encoding="utf8")
    print("R3Y_PATCH_COMPLETE=True")
    print("R3Y_FULL_FILES=" + str(OUTPUT))


def restore():
    meta = OUTPUT / "installed.json"
    if not meta.is_file():
        raise RuntimeError("No installation state")
    records = json.loads(meta.read_text(encoding="utf8"))
    for relative,data in records.items():
        if not data["changed"]:
            continue
        dest = ROOT / relative
        if digest(dest.read_text(encoding="utf8")) != data["after"]:
            raise RuntimeError("Refusing to overwrite subsequent changes: " + relative)
        name = relative.replace("/", "__").replace("\\", "__")
        dest.write_text((OUTPUT / (name + ".before")).read_text(encoding="utf8"),encoding="utf8")
        print("R3Y_RESTORED=" + relative)
    meta.unlink()


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install","restore"):
        raise SystemExit("Usage: install.py install|restore")
    globals()[sys.argv[1]]()
