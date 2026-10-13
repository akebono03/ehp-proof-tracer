"""Guarded R52-R9 installer. Apply a replaceable function at a time."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
TARGETS = (
    "phase165_r52_r9_shared_math.py",
    "phase165_r52_r7_registered_common_proof.py",
    "phase165_r52_r5_auto_search.py",
    "test_phase165_r52_r9_shared_math.py",
)


def _function_body(text: str, name: str):
    tree = ast.parse(text)
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f"expected one function: {name}")
    node = nodes[0]
    lines = text.splitlines(keepends=True)
    return ("".join(lines[node.lineno - 1:node.end_lineno]),
            node.lineno - 1, node.end_lineno)


def _replace_one_function(current: str, new: str, name: str) -> str:
    old_func, start, end = _function_body(current, name)
    new_func, _, _ = _function_body(new, name)
    lines = current.splitlines(keepends=True)
    lines[start:end] = [new_func]
    output = "".join(lines)
    ast.parse(output)
    return output


def main():
    for name in ("web_app.py", "phase165_r14_r34_backward_search.py",
                 "phase165_r14_r38_direct_registry.py", "phase165_r52_r2_search_adapter.py",
                 "phase165_r14_r39_toda51.tex", "phase165_r52_r7_registered_common_proof.py",
                 "phase165_r52_r5_auto_search.py"):
        if not (ROOT / name).exists():
            raise FileNotFoundError("Required project file missing: " + name)
    planned = {}
    for name in TARGETS:
        incoming = (BUNDLE / name).read_text(encoding="utf-8")
        ast.parse(incoming)
        current_file = ROOT / name
        if name in ("phase165_r52_r7_registered_common_proof.py", "phase165_r52_r5_auto_search.py"):
            current = current_file.read_text(encoding="utf-8-sig")
            function_name = ("build_registered_common_replay" if "r7" in name
                             else "search_group_structure_automatically")
            if name.endswith("r7_registered_common_proof.py"):
                if ("providers = registered_proof_providers()" not in current
                        and "search_shared_group_goal" not in current):
                    raise RuntimeError("Unknown R7 version; refusing to install")
            else:
                if "search_registered_partial_proof" not in current:
                    raise RuntimeError("Unknown R5 version; refusing to install")
            planned[current_file] = _replace_one_function(current, incoming, function_name)
        else:
            planned[current_file] = incoming
    target = ROOT / "phase165_r14_r34_backward_search.py"
    current = target.read_text(encoding="utf-8-sig")
    if "if goal == pi32_goal():" not in current and "ETA_2_HOPF_INVARIANT_FACT" not in current:
        raise RuntimeError("Unknown R34 version; refusing to remove special branch")
    replacement = (BUNDLE / "phase165_r34_expansions_FULL.py.txt").read_text(encoding="utf-8")
    planned[target] = _replace_one_function(current, replacement, "phase165_r34_expansions")
    # All transformations have been syntax-checked before ANY project file is changed.
    for dst, src in planned.items():
        if dst.exists() and dst.read_text(encoding="utf-8-sig") == src:
            print("Unchanged:", dst.name)
            continue
        if dst.exists():
            backup = ROOT / (dst.name + ".phase165_r52_r9_backup")
            if not backup.exists():
                shutil.copy2(dst, backup)
        dst.write_text(src, encoding="utf-8")
        print("Installed:", dst.name)
    print("Shared typed search installed; full pytest NOT run.")


if __name__ == "__main__":
    main()
