"""Install one guarded solver function insertion and one standalone adapter."""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
SOLVER = REPO / "phase165_r3_recursive_search.py"
ADAPTER = REPO / "phase169_r3n_prior_result_alias.py"
NEW_ADAPTER = PACKAGE / "new_files" / "phase169_r3n_prior_result_alias.py"
MARKER = "from phase169_r3n_prior_result_alias import resolve_prior_result_alias_step"
ANCHOR = "            # phase165_reference_stop_r3: direct eligible source before prior internal proof"
INSERT = """            # R3N: a positioned DB result needs no completed earlier proof.
            # Exact screened GIVEN sources were returned above. Only differing
            # registered generator presentations reach this guarded fallback.
            if lookup_mode == "typed_reference_publication" and not options:
                from phase169_r3n_prior_result_alias import resolve_prior_result_alias_step
                alias_step = resolve_prior_result_alias_step(
                    target, bridge, citing_assertion_id,
                )
                if alias_step is not None:
                    for prior_step in alias_step.premises:
                        report("proved", prior_step.conclusion, prior_step)
                    solved.append((target, alias_step))
                    report("proved", target, alias_step)
                    return alias_step
"""


def extract_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    functions = [item for item in tree.body
                 if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and item.name == name]
    if len(functions) != 1:
        raise RuntimeError("Expected exactly one solver function")
    lines = source.splitlines(keepends=True)
    function = functions[0]
    return "".join(lines[function.lineno - 1:function.end_lineno])


def prepare_solver(source: str) -> str:
    if MARKER in source:
        return source
    if source.count(ANCHOR) != 1:
        raise RuntimeError("R3N solver insertion anchor changed; nothing patched")
    result = source.replace(ANCHOR, INSERT + ANCHOR, 1)
    ast.parse(result)
    if MARKER not in extract_function(result, "reconstruct_registered_goal"):
        raise RuntimeError("R3N insertion did not land inside target function")
    return result


def main() -> None:
    if not SOLVER.is_file() or not NEW_ADAPTER.is_file():
        raise RuntimeError("Run from an extracted package under repository root")
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=REPO, text=True).strip()
    print("R3N_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("develop branch is required")
    source = SOLVER.read_text(encoding="utf-8-sig")
    target = prepare_solver(source)
    adapter_source = NEW_ADAPTER.read_text(encoding="utf-8")
    ast.parse(adapter_source)
    if ADAPTER.exists() and ADAPTER.read_text(encoding="utf-8") != adapter_source:
        raise RuntimeError("existing R3N adapter differs; refuse overwrite")
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "reconstruct_registered_goal_FULL.py").write_text(
        extract_function(target, "reconstruct_registered_goal") + "\n", encoding="utf-8",
    )
    (output / "phase169_r3n_prior_result_alias_FULL.py").write_text(adapter_source, encoding="utf-8")
    if target != source:
        (output / "phase165_r3_recursive_search.py.before").write_text(source, encoding="utf-8")
    if not ADAPTER.exists():
        ADAPTER.write_text(adapter_source, encoding="utf-8")
        print("R3N_CREATED=" + ADAPTER.name)
    if target != source:
        SOLVER.write_text(target, encoding="utf-8")
        print("R3N_PATCHED=" + SOLVER.name)
    else:
        print("R3N_ALREADY_INSTALLED=True")
    print("R3N_FULL_CODE=" + str(output))
    print("R3N_PATCH_COMPLETE=True")


if __name__ == "__main__":
    main()
