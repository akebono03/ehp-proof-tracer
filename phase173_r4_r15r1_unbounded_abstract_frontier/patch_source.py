"""One-file, reviewed-source transformation for generic abstract prior frontiers.

The candidate is not a proof and never bypasses named-generator guards.
"""
from __future__ import annotations

import ast
from pathlib import Path

ORIGINAL_BLOB = "cd4b8feb29fbe95a4aedb355514a0267146935ee"
TARGET = "phase173_r4_r10_general_toda56_core/core.py"

UPDATED_IMPORT = "from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup"
ORIGINAL_IMPORT = "from homotopy_groups import TodaPrimaryGroup"

REPLACEMENT = '''def _abstract_group_signature(statement: object) -> tuple[tuple[str, int], ...] | None:
    """Read structural cyclic orders only; no generator equality is inferred."""
    components = _group_components(statement)
    if components is None:
        return None
    signature: list[tuple[str, int]] = []
    for component in components:
        if isinstance(component, FreeCyclicGroup):
            signature.append(("free", 0))
        elif (isinstance(component, FiniteCyclicGroup)
              and type(component.order) is int and component.order >= 2):
            signature.append(("finite", component.order))
        else:
            return None
    return tuple(sorted(signature))


def checked_abstract_inputs(goal: object) -> tuple[object, object] | None:
    """Identify general Toda 4.4 prior-group shapes for every registered k.

    This is a necessary abstract compatibility check, NOT a ProofStep,
    not a source citation and not evidence for named generator identities.
    The actual n=4 target and both adopted prior CSV rows must be verified.
    """
    coordinates = group_coordinates(goal)
    if coordinates is None:
        return None
    n, k = coordinates
    if n != 4 or type(k) is not int:
        return None
    dimension = n + k
    if dimension < 7:
        return None
    group = (
        goal.group if hasattr(goal, "group") else
        goal.lhs if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY
        else None
    )
    if group != TodaPrimaryGroup(dimension, 4):
        return None
    registered = exact_prior_database_result(4, k)
    if type(registered) is not type(goal) or registered != goal:
        return None
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    if first is None or second is None:
        return None
    if (admitted_db_step(first, proof_target=goal) is None
            or admitted_db_step(second, proof_target=goal) is None):
        return None
    target_signature = _abstract_group_signature(goal)
    first_signature = _abstract_group_signature(first)
    second_signature = _abstract_group_signature(second)
    if (target_signature is None or first_signature is None
            or second_signature is None):
        return None
    if tuple(sorted(first_signature + second_signature)) != target_signature:
        return None
    return first, second


def checked_general_inputs(goal: object) -> tuple[object, object] | None:
    """Require both abstract compatibility and certified generator presentation.

    The general structural gate is k-unbounded, but an unverified generator
    mapping never becomes a complete result. Existing public rules stay strict.
    """
    pair = checked_abstract_inputs(goal)
    if pair is None:
        return None
    first, second = pair
    mapped = _map_components(first, second)
    actual = _group_components(goal)
    if mapped is None or actual is None or not components_match_alias(mapped, actual):
        return None
    return first, second
'''


def transform(source: bytes) -> bytes:
    """Replace complete function and complete import atomically; retain EOL."""
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    if b"\r\n" in source and source.replace(b"\r\n", b"").find(b"\n") != -1:
        raise RuntimeError("Mixed EOL requires separate review")
    decoded = source.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(decoded)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    names = {node.name for node in functions}
    if "checked_abstract_inputs" in names:
        raise RuntimeError("Previously generalized core requires separate review")
    target = [node for node in functions if node.name == "checked_general_inputs"]
    subsequent = [node for node in functions if node.name == "general_toda56_rule"]
    if len(target) != 1 or len(subsequent) != 1:
        raise RuntimeError("Reviewed function anchors are missing")
    if subsequent[0].lineno <= target[0].end_lineno:
        raise RuntimeError("Reviewed function ordering changed")
    if decoded.count(ORIGINAL_IMPORT) != 1 or UPDATED_IMPORT in decoded:
        raise RuntimeError("Reviewed import anchor missing or duplicated")
    if decoded.count("def checked_general_inputs(") != 1:
        raise RuntimeError("Reviewed function name is ambiguous")
    source_lines = decoded.splitlines(keepends=True)
    before = "".join(source_lines[:target[0].lineno - 1])
    after = "".join(source_lines[subsequent[0].lineno - 1:])
    if any(line.strip() for line in source_lines[target[0].end_lineno:subsequent[0].lineno - 1]):
        raise RuntimeError("Unexpected code between reviewed functions")
    original = "".join(source_lines[target[0].lineno - 1:target[0].end_lineno])
    required = (
        "def checked_general_inputs(goal: object)",
        "exact_prior_database_result(4, k)",
        "admitted_db_step(first, proof_target=goal)",
        "admitted_db_step(second, proof_target=goal)",
        "_map_components(first, second)",
        "components_match_alias(mapped, actual)",
    )
    if not all(value in original for value in required):
        raise RuntimeError("Reviewed generator guard differs")
    updated = (before + REPLACEMENT + "\n" + after).replace(ORIGINAL_IMPORT, UPDATED_IMPORT)
    ast.parse(updated)
    output = updated.encode("utf-8")
    return output.replace(b"\n", newline) if newline == b"\r\n" else output


def find_module(root: Path) -> Path:
    return root / TARGET
