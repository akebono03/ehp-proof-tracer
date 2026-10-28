"""Offline guards for canonical eta 1-stem proposal selection patch."""
from __future__ import annotations

import ast

import pytest

from phase169_r10eg_one_stem_route_priority.patch import (
    FUNCTION, NEW, OLD, extract_function, transform,
)


def _sample(newline: str) -> bytes:
    text = (
        "def other():\n"
        "    return 1\n\n"
        "def expand_prior_general_group_transport():\n"
        + OLD +
        "        None\n"
        "    )\n"
        "    return ()\n"
    )
    return text.replace("\n", newline).encode("utf-8")


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_r10eg_full_function_and_line_endings(newline):
    original = _sample(newline)
    patched, full = transform(original)
    assert NEW in patched.decode("utf-8").replace("\r\n", "\n")
    assert full.startswith("def expand_prior_general_group_transport():")
    assert "return ()" in full
    assert "_matching_eta_name" in full
    assert (b"\r\n" in patched) == (newline == "\r\n")
    ast.parse(patched.decode("utf-8"))


def test_r10eg_rejects_second_patch():
    patched, _ = transform(_sample("\n"))
    with pytest.raises(RuntimeError, match="already patched"):
        transform(patched)


def test_r10eg_rejects_missing_or_ambiguous_anchor():
    with pytest.raises(RuntimeError):
        transform(b"def unrelated():\n    return None\n")
    with pytest.raises(RuntimeError):
        transform(_sample("\n") + _sample("\n"))


def test_r10eg_rejects_mixed_newlines():
    with pytest.raises(RuntimeError, match="mixed newlines"):
        transform(_sample("\r\n") + b"\n")


def test_r10eg_has_only_typed_eta_guard():
    assert "k == 1" in NEW
    assert "goal.rhs.order == 2" in NEW
    assert "_matching_eta_name" in NEW
    assert "return ()" in NEW
    assert "ProofRule" not in NEW
    assert FUNCTION == "expand_prior_general_group_transport"
    assert extract_function(_sample("\n").decode("utf-8")).startswith("def expand_prior_general_group_transport")
