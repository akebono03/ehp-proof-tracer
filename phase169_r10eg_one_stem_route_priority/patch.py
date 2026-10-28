"""Guarded reversible, narrowly scoped R10EG production patch.

Only one function in the existing transport adapter is modified. No inference
rules, typed proof steps, reference data or databases are changed.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase169_r10e1_general_group_transport" / "transport.py"
FUNCTION = "expand_prior_general_group_transport"
OLD = (
    "    k = group.group_dimension - n\n"
    "    if k < 0 or n <= k + 2 or _components(goal) is None:\n"
    "        return ()\n"
    "    citing_id = (\n"
)
NEW = (
    "    k = group.group_dimension - n\n"
    "    if k < 0 or n <= k + 2 or _components(goal) is None:\n"
    "        return ()\n"
    "    # R10EG: established eta-specific 1-stem derivations must not compete\n"
    "    # with the newer arbitrary-fold general transport at the same root.\n"
    "    # This is a proposal-selection restriction, not a mathematical fact.\n"
    "    if (k == 1 and isinstance(goal, Relation)\n"
    "            and isinstance(goal.rhs, FiniteCyclicGroup)\n"
    "            and goal.rhs.order == 2):\n"
    "        from phase165_r12_r28_presentation_connection import _matching_eta_name\n"
    "        from toda_rules import toda_eta_family_definition_statement\n"
    "        eta = toda_eta_family_definition_statement(n).element\n"
    "        if _matching_eta_name(goal.rhs.generator, eta):\n"
    "            return ()\n"
    "    citing_id = (\n"
)


def extract_function(source: str) -> str:
    """Export a complete replacement function, including its local imports."""
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == FUNCTION]
    if len(nodes) != 1:
        raise RuntimeError("R10EG expected exactly one transport function")
    lines = source.splitlines(keepends=True)
    node = nodes[0]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def transform(raw: bytes) -> tuple[bytes, str]:
    """Preserve CRLF/LF and reject unknown or already patched source."""
    text = raw.decode("utf-8")
    if "\r\n" in text and text.count("\n") != text.count("\r\n"):
        raise RuntimeError("R10EG mixed newlines refused")
    crlf = "\r\n" in text
    normalized = text.replace("\r\n", "\n")
    if normalized.count(OLD) != 1 or NEW in normalized:
        raise RuntimeError("R10EG unreviewed or already patched transport source")
    patched = normalized.replace(OLD, NEW, 1)
    ast.parse(patched)
    full = extract_function(patched)
    if patched.count("def " + FUNCTION + "(") != 1:
        raise RuntimeError("R10EG function count changed unexpectedly")
    output = patched.replace("\n", "\r\n") if crlf else patched
    return output.encode("utf-8"), full


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("Usage: python -m phase169_r10eg_one_stem_route_priority.patch OUTPUT_DIRECTORY")
    output = Path(args[0]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    raw = TARGET.read_bytes()
    patched, function = transform(raw)
    reviewed = (Path(__file__).resolve().parent / (FUNCTION + "_FULL.py")).read_text(encoding="utf-8")
    if function.strip() != reviewed.strip():
        raise RuntimeError("R10EG generated function differs from reviewed full replacement")
    (output / "transport.py.before").write_bytes(raw)
    (output / "transport.py.FULL").write_bytes(patched)
    (output / (FUNCTION + "_FULL.py")).write_text(function + "\n", encoding="utf-8")
    TARGET.write_bytes(patched)
    print("R10EG_PATCHED=" + str(TARGET))
    print("R10EG_FULL_FUNCTION=" + str(output / (FUNCTION + "_FULL.py")))
    print("R10EG_FULL_FILE=" + str(output / "transport.py.FULL"))
    print("R10EG_NEWLINE=" + ("CRLF" if b"\r\n" in raw else "LF"))
    print("R10EG_INFERENCE_RULES_CHANGED=False")


if __name__ == "__main__":
    main()
