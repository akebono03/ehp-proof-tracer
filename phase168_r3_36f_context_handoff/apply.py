"""Minimal guarded patch: pass actual screened search bridge to narrative model."""
from __future__ import annotations

import ast
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGETS = (
    "phase165_r52_r9_shared_math.py",
    "phase165_r55_nk_only_goal.py",
    "web_group_proof.py",
)


def replace_once(source: str, old: str, new: str, name: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{name}: expected exactly one anchor, got {count}")
    return source.replace(old, new, 1)


def rewrite(path: str, source: str) -> str:
    if path == TARGETS[0]:
        source = replace_once(
            source, "proof_order_catalog=None, recursive_proof_order_catalog=None):",
            "proof_order_catalog=None, recursive_proof_order_catalog=None, context_sink=None):",
            path,
        )
        source = replace_once(
            source, "                target_order=order,\n",
            "                target_order=order,\n                context_sink=context_sink,\n",
            path,
        )
        source = replace_once(
            source,
            "    if expansion_provider is None:\n        expansion_provider = shared_expansion_provider(\n            proof_context, proof_target=goal,",
            "    if context_sink is not None:\n"
            "        context_sink(proof_context)\n"
            "    if expansion_provider is None:\n"
            "        expansion_provider = shared_expansion_provider(\n"
            "            proof_context, proof_target=goal,",
            path,
        )
    elif path == TARGETS[1]:
        source = replace_once(
            source,
            "def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None):",
            "def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None, context_sink=None):",
            path,
        )
        source = replace_once(
            source,
            "        provider = shared_expansion_provider(\n            screened, proof_target=candidate,\n",
            "        if context_sink is not None:\n"
            "            context_sink(screened)\n"
            "        provider = shared_expansion_provider(\n"
            "            screened, proof_target=candidate,\n",
            path,
        )
        source = replace_once(
            source,
            "        proof_order_catalog=proof_order_catalog,\n    )\n    if citing_id is not None:",
            "        proof_order_catalog=proof_order_catalog,\n"
            "        context_sink=context_sink,\n"
            "    )\n    if citing_id is not None:",
            path,
        )
    elif path == TARGETS[2]:
        source = replace_once(
            source,
            "  bridge = build_shared_typed_bridge()\n"
            "  result = search_group_from_registered_goal(n=n, k=k, goal=goal, bridge=bridge)\n"
            "  model = build_linked_proof_narrative_model(result, bridge)\n",
            "  bridge = build_shared_typed_bridge()\n"
            "  search_contexts = []\n"
            "  result = search_group_from_registered_goal(\n"
            "    n=n, k=k, goal=goal, bridge=bridge,\n"
            "    context_sink=search_contexts.append,\n"
            "  )\n"
            "  model_bridge = search_contexts[-1] if search_contexts else bridge\n"
            "  model = build_linked_proof_narrative_model(result, model_bridge)\n",
            path,
        )
    return source


def function_text(source: str, function: str) -> str:
    tree = ast.parse(source)
    node = next(
        item for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == function
    )
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def main() -> None:
    changes = []
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    functions = {
        TARGETS[0]: "search_shared_group_goal",
        TARGETS[1]: "search_group_from_registered_goal",
        TARGETS[2]: "build_standard_web_group_proof_view",
    }
    prepared = {}
    for name in TARGETS:
        target = ROOT / name
        raw = target.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        source = raw.decode("utf-8").replace("\r\n", "\n")
        updated = rewrite(name, source)
        ast.parse(updated)
        prepared[name] = (target, source, updated, newline)
    for name, (target, old, new, newline) in prepared.items():
        if old == new:
            raise RuntimeError("Expected new change: " + name)
        backup = output / (name + ".before.py")
        backup.write_text(old, encoding="utf-8")
        full = output / (name.replace(".py", "") + "_FULL_FUNCTION.py")
        full.write_text(function_text(new, functions[name]) + "\n", encoding="utf-8")
        diff = "".join(difflib.unified_diff(
            old.splitlines(keepends=True), new.splitlines(keepends=True),
            fromfile=name + ":before", tofile=name + ":after",
        ))
        (output / (name + ".diff")).write_text(diff, encoding="utf-8")
        target.write_bytes(new.replace("\n", newline).encode("utf-8"))
        changes.append(name)
    print("PATCHED:", ", ".join(changes))
    print("FULL_FUNCTIONS:", output)


if __name__ == "__main__":
    main()
