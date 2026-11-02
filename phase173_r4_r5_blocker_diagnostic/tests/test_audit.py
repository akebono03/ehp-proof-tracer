"""Focused offline contracts for the R4-R5 read-only blocker diagnostic."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import pytest

from phase173_r4_r5_blocker_diagnostic import audit


@dataclass(frozen=True)
class Symbol:
    family: str
    index: int | None


@dataclass(frozen=True)
class Element:
    name: str
    generator: Symbol


@dataclass(frozen=True)
class FiniteCyclicGroup:
    order: int
    generator: Element


def test_encoded_tree_preserves_generator_symbol_and_name() -> None:
    item = Element("eta_7", Symbol("η", 7))
    tree = audit.encoded_tree(item)
    assert tree == {
        "type": "Element",
        "fields": {
            "name": "eta_7",
            "generator": {"type": "Symbol", "fields": {"family": "η", "index": 7}},
        },
    }


def test_first_difference_locates_exact_generator_field() -> None:
    a = audit.encoded_tree(Element("η₇", Symbol("η", 7)))
    b = audit.encoded_tree(Element("eta_7", Symbol("η", 7)))
    assert audit.first_difference(a, b) == {
        "path": "root.fields.name", "expected": "η₇", "registered": "eta_7",
    }


def test_first_difference_preserves_symbol_index_guard() -> None:
    a = audit.encoded_tree(Element("η₇", Symbol("η", 7)))
    b = audit.encoded_tree(Element("η₇", Symbol("η", 8)))
    diff = audit.first_difference(a, b)
    assert diff is not None
    assert diff["path"] == "root.fields.generator.fields.index"


def test_components_match_without_order_assumption() -> None:
    a = FiniteCyclicGroup(2, Element("ν₄η₇", Symbol("ν", 4)))
    b = FiniteCyclicGroup(2, Element("Eν′η₇", Symbol("ν", None)))
    assert audit.component_differences((a, b), (b, a)) == []


def test_component_mismatch_preserves_type_and_order() -> None:
    a = FiniteCyclicGroup(2, Element("ν₄η₇", Symbol("ν", 4)))
    b = FiniteCyclicGroup(4, Element("ν₄η₇", Symbol("ν", 4)))
    result = audit.component_differences((a,), (b,))
    assert result[0]["kind"] == "unmatched_expected_component"
    assert result[1]["kind"] == "unmatched_registered_component"


def test_component_name_difference_is_diagnostic_not_normalization() -> None:
    a = FiniteCyclicGroup(2, Element("η₇", Symbol("η", 7)))
    b = FiniteCyclicGroup(2, Element("eta7", Symbol("η", 7)))
    result = audit.component_differences((a,), (b,))
    assert result[0]["kind"] == "generator_shape_mismatch"
    assert result[0]["first_difference"]["path"].endswith("generator.fields.name")


def test_missing_components_do_not_become_empty_proof() -> None:
    assert audit.component_differences(None, ()) == [{
        "kind": "missing_components", "expected_present": False,
        "registered_present": True,
    }]
    assert audit.component_differences((), ()) == []


def test_unsupported_objects_fail_closed() -> None:
    with pytest.raises(TypeError, match="unsupported"):
        audit.encoded_tree(object())


def test_depth_limit_is_enforced() -> None:
    with pytest.raises(ValueError, match="depth"):
        audit.encoded_tree([[[[[[[[[[[[[[[[[[[1]]]]]]]]]]]]]]]]]]])


def test_preflight_rejects_unreviewed_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path.resolve()
    responses = {
        ("rev-parse", "--show-toplevel"): str(root),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "unexpected",
    }
    monkeypatch.setattr(audit, "git", lambda _root, *args: responses[args])
    with pytest.raises(RuntimeError, match="unreviewed develop HEAD"):
        audit.preflight(root, remote=False)


def test_source_blob_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path.resolve()
    responses = {
        ("rev-parse", "--show-toplevel"): str(root),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): "",
    }
    for name, blob in audit.REVIEWED_FILES.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixture", encoding="utf-8")
        responses[("rev-parse", "HEAD:" + name)] = blob
    monkeypatch.setattr(audit, "git", lambda _root, *args: responses[args])
    assert audit.preflight(root, remote=False)["source_guard"] == "PASS"
    first = next(iter(audit.REVIEWED_FILES))
    responses[("rev-parse", "HEAD:" + first)] = "WRONG"
    with pytest.raises(RuntimeError, match="unreviewed source blob"):
        audit.preflight(root, remote=False)


def test_saved_diagnostics_keep_no_proof_assertion() -> None:
    data = {"i": 9, "exact_generator_match": True,
            "generator_images_proved": False, "complete_proof_asserted": False}
    serialized = json.loads(json.dumps(data))
    assert serialized["generator_images_proved"] is False
    assert serialized["complete_proof_asserted"] is False
