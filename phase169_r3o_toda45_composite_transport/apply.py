"""R3O guarded installer. Only a new typed-rule module and one solver function."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE = ROOT / "phase165_r52_r9_shared_math.py"
NEW_MODULE = ROOT / "phase169_r3o_stable_composite_rule.py"
STAGED = PACKAGE / "new_files" / "phase169_r3o_stable_composite_rule.py"
OUTPUT = PACKAGE / "output"

ANCHOR = "        options.extend(expand_finite_cyclic_relation(goal))"
INSERT = (
    "        from phase169_r3o_stable_composite_rule import (\n"
    "            expand_cited_toda45_composite_transport,\n"
    "        )\n"
    "        options.extend(expand_cited_toda45_composite_transport(\n"
    "            goal, tuple(available),\n"
    "        ))"
)


def _function_text(source: str, function: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == function]
    if len(matches) != 1:
        raise RuntimeError("Function boundary not unique: " + function)
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            text=True, capture_output=True, check=True).stdout.strip()
    print("R3O_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("R3O expects develop branch")
    if not SOURCE.is_file() or not STAGED.is_file():
        raise RuntimeError("R3O missing source or staging module")
    src = SOURCE.read_text(encoding="utf-8-sig")
    new_module = STAGED.read_text(encoding="utf-8")
    ast.parse(src)
    ast.parse(new_module)
    if src.count(ANCHOR) != 1:
        raise RuntimeError("R3O guarded function anchor missing or ambiguous")
    if src.count("def shared_expansion_provider(") != 1:
        raise RuntimeError("R3O shared expansion provider has changed")
    previously_installed = "expand_cited_toda45_composite_transport(" in src
    if previously_installed:
        if INSERT not in src:
            raise RuntimeError("R3O existing installation differs")
        patched = src
    else:
        patched = src.replace(ANCHOR, ANCHOR + "\n" + INSERT, 1)
    ast.parse(patched)
    if NEW_MODULE.exists() and NEW_MODULE.read_text(encoding="utf-8") != new_module:
        raise RuntimeError("R3O module exists with unexpected contents")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Save full replaceable functions and whole new module, including imports.
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        _function_text(patched, "shared_expansion_provider") + "\n", encoding="utf-8")
    (OUTPUT / "phase169_r3o_stable_composite_rule_FULL.py").write_text(
        new_module, encoding="utf-8")
    if patched != src:
        backup = OUTPUT / "phase165_r52_r9_shared_math.py.before"
        if not backup.exists():
            shutil.copy2(SOURCE, backup)
        SOURCE.write_text(patched, encoding="utf-8")
        print("R3O_PATCHED=phase165_r52_r9_shared_math.py")
    else:
        print("R3O_ALREADY_PATCHED=True")
    if not NEW_MODULE.exists():
        NEW_MODULE.write_text(new_module, encoding="utf-8")
        print("R3O_CREATED=phase169_r3o_stable_composite_rule.py")
    else:
        print("R3O_MODULE_ALREADY_INSTALLED=True")
    print("R3O_FULL_CODE=" + str(OUTPUT))
    print("R3O_PATCH_COMPLETE=True")


if __name__ == "__main__":
    main()
