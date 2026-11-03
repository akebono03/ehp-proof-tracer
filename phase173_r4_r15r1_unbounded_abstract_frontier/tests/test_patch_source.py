"""Standalone tests of the one-function patch boundary."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_IMPORT,
    UPDATED_IMPORT,
    transform,
)


def fixture_source(eol: str = "\n") -> bytes:
    text = (
        "from __future__ import annotations\n"
        + ORIGINAL_IMPORT + "\n"
        + "from phase173_r4_r4_typed_generator_audit.audit import _group_components, _map_components\n"
        + "def checked_general_inputs(goal: object):\n"
        + "    registered = exact_prior_database_result(4, k)\n"
        + "    first = admitted_db_step(first, proof_target=goal)\n"
        + "    second = admitted_db_step(second, proof_target=goal)\n"
        + "    mapped = _map_components(first, second)\n"
        + "    actual = _group_components(goal)\n"
        + "    if not components_match_alias(mapped, actual):\n"
        + "        return None\n"
        + "    return first, second\n\n\n"
        + "def general_toda56_rule(goal: object):\n"
        + "    return goal\n"
    )
    return text.replace("\n", eol).encode("utf-8")


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_transform_preserves_end_of_lines_and_unrelated_function(eol: str) -> None:
    source = fixture_source(eol)
    result = transform(source)
    assert UPDATED_IMPORT.encode() in result
    assert ORIGINAL_IMPORT.encode() not in result
    assert result.count(b"def checked_abstract_inputs(") == 1
    assert result.count(b"def checked_general_inputs(") == 1
    assert result.endswith(f"def general_toda56_rule(goal: object):{eol}    return goal{eol}".encode())
    assert (b"\r\n" in result) == (eol == "\r\n")
    ast.parse(result.decode())


def test_transform_refuses_missing_guard() -> None:
    source = fixture_source().replace(b"components_match_alias(mapped, actual)", b"True")
    with pytest.raises(RuntimeError, match="Reviewed generator guard"):
        transform(source)


def test_transform_refuses_duplicate_general_implementation() -> None:
    source = fixture_source().replace(b"def general_toda56_rule", b"def checked_abstract_inputs(x):\n    pass\n\ndef general_toda56_rule")
    with pytest.raises(RuntimeError, match="Previously generalized"):
        transform(source)


def test_transform_refuses_mixed_endings() -> None:
    source = fixture_source("\r\n") + b"# stray\n"
    with pytest.raises(RuntimeError, match="Mixed EOL"):
        transform(source)
