"""Guard the R16->R17 remote lineage and non-circular theorem boundary."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r17_typed_map_open_goal.audit import (
    PRE_R16_HEAD, REVIEWED_HEAD, R16_PREFIX, SHARED_MATH,
    reviewed_lineage, validate_r16_report,
)


def committed_paths() -> tuple[str, ...]:
    return (SHARED_MATH, R16_PREFIX + "audit.py")


def test_released_r16_source_and_unchanged_math_handoff_are_accepted() -> None:
    assert reviewed_lineage(PRE_R16_HEAD, REVIEWED_HEAD,
                            committed_paths(), (SHARED_MATH,), False) == "LOCAL_R16_PATCH_UNCOMMITTED"
    assert reviewed_lineage(REVIEWED_HEAD, REVIEWED_HEAD,
                            committed_paths(), (), False) == "R16_MERGED_CLEAN"
    assert reviewed_lineage(PRE_R16_HEAD, REVIEWED_HEAD,
                            committed_paths(), (SHARED_MATH, "web_group_proof_common.py"), True) == "LOCAL_R16_PATCH_UNCOMMITTED"
    assert reviewed_lineage(REVIEWED_HEAD, REVIEWED_HEAD,
                            committed_paths(), ("web_group_proof_common.py",), True) == "R16_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,tracked,patched", (
    (PRE_R16_HEAD, PRE_R16_HEAD, committed_paths(), (SHARED_MATH,), False),
    ("f" * 40, REVIEWED_HEAD, committed_paths(), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, ("proof.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, committed_paths(), ("proof.py",), False),
    (PRE_R16_HEAD, REVIEWED_HEAD, committed_paths(), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, committed_paths(), ("web_group_proof_common.py",), False),
))
def test_unreviewed_checkout_or_tracked_change_fails_closed(local, remote, paths, tracked, patched) -> None:
    with pytest.raises(RuntimeError):
        reviewed_lineage(local, remote, paths, tracked, patched)


def valid_r16() -> dict:
    return {
        "phase": "174-R3-R7-R16",
        "gate": "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN",
        "new_group_given": 0,
        "new_mathematical_inference_rules": 0,
        "full_pytest_run": False,
        "root_proof_completed_claimed": False,
    }


def test_valid_real_r16_report_contract() -> None:
    assert validate_r16_report(valid_r16())["root_was_not_completed"] is True


@pytest.mark.parametrize("field,value", (
    ("phase", "174-R3-R7-R15"),
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_mathematical_inference_rules", 1),
    ("full_pytest_run", True),
    ("root_proof_completed_claimed", True),
))
def test_incorrect_prior_source_or_fabricated_completion_rejected(field, value) -> None:
    item = valid_r16()
    item[field] = value
    with pytest.raises(RuntimeError):
        validate_r16_report(item)
