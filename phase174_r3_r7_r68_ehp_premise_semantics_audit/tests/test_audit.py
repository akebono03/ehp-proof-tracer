"""R68 focused negative controls for typed, verified proof-step premise checks."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r68_ehp_premise_semantics_audit.audit import (
    PINS, check_direct_premises, git_blob_sha, source_guard, unique_inference_index,
)


def _role(name: str) -> SimpleNamespace:
    return SimpleNamespace(name=name)


def _fixture() -> SimpleNamespace:
    given = SimpleNamespace(conclusion="previous source", rule=_role("GIVEN"),
                            premises=(), inference_rule=None)
    exact = SimpleNamespace(conclusion="typed exactness", rule=_role("INFERENCE"),
                            premises=(given,), inference_rule=SimpleNamespace(name="certify window"))
    zero = SimpleNamespace(conclusion="zero image", rule=_role("INFERENCE"),
                           premises=(given,), inference_rule=SimpleNamespace(name="prove zero image"))
    goal = SimpleNamespace(conclusion="injective", rule=_role("INFERENCE"),
                           premises=(zero, exact), inference_rule=SimpleNamespace(name="EHP injective"))
    return SimpleNamespace(steps=(given, exact, zero, goal))


def test_unique_checked_inference() -> None:
    model = _fixture()
    assert unique_inference_index(model, frozenset(range(4)), "injective", "EHP injective") == 3
    assert check_direct_premises(model, frozenset(range(4)), 3,
                                 ("zero image", "typed exactness"),
                                 ("INFERENCE", "INFERENCE")) == (2, 1)


def test_direct_premise_reversal_rejected() -> None:
    with pytest.raises(RuntimeError, match="R68_PREMISE_GOAL_OR_ROLE_MISMATCH"):
        check_direct_premises(_fixture(), frozenset(range(4)), 3,
                              ("typed exactness", "zero image"),
                              ("INFERENCE", "INFERENCE"))


def test_direct_given_cannot_replace_inferred_premise() -> None:
    with pytest.raises(RuntimeError, match="R68_PREMISE_GOAL_OR_ROLE_MISMATCH"):
        check_direct_premises(_fixture(), frozenset(range(4)), 3,
                              ("zero image", "typed exactness"),
                              ("GIVEN", "INFERENCE"))


def test_incomplete_premise_scope_rejected() -> None:
    with pytest.raises(RuntimeError, match="R68_MISSING_OR_AMBIGUOUS_PREMISE"):
        check_direct_premises(_fixture(), frozenset({0, 1, 3}), 3,
                              ("zero image", "typed exactness"),
                              ("INFERENCE", "INFERENCE"))


def test_unknown_rule_or_duplicate_inference_rejected() -> None:
    model = _fixture()
    with pytest.raises(RuntimeError, match="R68_INFERENCE_NOT_UNIQUE"):
        unique_inference_index(model, frozenset(range(4)), "injective", "different")
    model.steps = model.steps + (model.steps[3],)
    with pytest.raises(RuntimeError, match="R68_INFERENCE_NOT_UNIQUE"):
        unique_inference_index(model, frozenset(range(5)), "injective", "EHP injective")


def test_inference_root_not_given() -> None:
    with pytest.raises(RuntimeError, match="R68_TARGET_NOT_INFERENCE"):
        check_direct_premises(_fixture(), frozenset(range(4)), 0, (), ())


@pytest.mark.parametrize("bad_index", [-1, 4, None, "3"])
def test_invalid_index_rejected(bad_index: object) -> None:
    with pytest.raises(ValueError, match="R68_INVALID_VERIFIED_STEP_INDEX"):
        check_direct_premises(_fixture(), frozenset(range(4)), bad_index, (), ())


def test_wrong_count_rejected() -> None:
    with pytest.raises(RuntimeError, match="R68_PREMISE_COUNT_CHANGED"):
        check_direct_premises(_fixture(), frozenset(range(4)), 3,
                              ("zero image",), ("INFERENCE",))


def test_invalid_required_roles_rejected() -> None:
    with pytest.raises(ValueError, match="R68_INVALID_REQUIRED_PREMISE_CONTRACT"):
        check_direct_premises(_fixture(), frozenset(range(4)), 3,
                              ("zero image",), ())


def test_source_guard_accepts_reviewed_repo() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 11
    assert source_guard(root) == tuple(PINS)


def test_source_guard_rejects_changed_blob(tmp_path: Path) -> None:
    path = tmp_path / next(iter(PINS))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R68_SOURCE_GUARD_FAILED"):
        source_guard(tmp_path)


def test_git_blob_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
