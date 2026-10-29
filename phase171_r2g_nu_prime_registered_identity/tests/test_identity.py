"""Focused R2G tests for registered, typed nu-prime identity."""
from __future__ import annotations

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase168_r2_8_3_generator_identity.identity import (
    _factor_identity,
    _master_records,
    same_registered_group_presentation,
)


def db_nu_prime() -> HomotopyElement:
    return HomotopyElement(
        "ν'", 3, 6, 3, GeneratorSymbol(r"\nu'"),
    )


def r2e_nu_prime(*, decoration: str = "′") -> HomotopyElement:
    return HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration=decoration),
    )


def test_master_row_three_matches_reviewed_metadata() -> None:
    record = _master_records()[3]
    assert (record["n"], record["k"], record["kinds"]) == ("3", "3", "1")
    assert (record["display"], record["latex"]) == ("ν'", r"\nu'")


def test_unindexed_r2e_nu_prime_is_same_registered_id_as_db() -> None:
    db = db_nu_prime()
    r2e = r2e_nu_prime()
    assert db != r2e
    assert _factor_identity(db, _master_records()) == (3, 3, 6, 3)
    assert _factor_identity(r2e, _master_records()) == (3, 3, 6, 3)
    assert same_registered_group_presentation(FiniteCyclicGroup(4, db), FiniteCyclicGroup(4, r2e))


def test_ascii_prime_and_suspension_are_registered_equivalences() -> None:
    db = db_nu_prime()
    r2e = r2e_nu_prime(decoration="'")
    assert same_registered_group_presentation(FiniteCyclicGroup(4, db), FiniteCyclicGroup(4, r2e))
    assert same_registered_group_presentation(
        FiniteCyclicGroup(4, IteratedSuspension(db, 1)),
        FiniteCyclicGroup(4, Suspension(r2e)),
    )


@pytest.mark.parametrize("invalid", [
    HomotopyElement("ν′", 4, 7, 4, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 7, 3, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 6, 4, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", index=5, decoration="′")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("η", decoration="′")),
])
def test_unindexed_alias_rejects_wrong_type(invalid: HomotopyElement) -> None:
    assert not same_registered_group_presentation(
        FiniteCyclicGroup(4, db_nu_prime()), FiniteCyclicGroup(4, invalid),
    )


def test_wrong_order_and_group_kind_do_not_match() -> None:
    assert not same_registered_group_presentation(
        FiniteCyclicGroup(4, db_nu_prime()),
        FiniteCyclicGroup(8, r2e_nu_prime()),
    )
    assert not same_registered_group_presentation(
        FreeCyclicGroup(db_nu_prime()),
        FiniteCyclicGroup(4, r2e_nu_prime()),
    )


def test_new_alias_rejects_changed_master_record() -> None:
    base = _master_records()
    for key, value in (("latex", r"\nu"), ("display", "ν"),
                       ("kinds", "0"), ("k", "4"), ("n", "4")):
        records = {i: record.copy() for i, record in base.items()}
        records[3][key] = value
        assert _factor_identity(r2e_nu_prime(), records) is None


def test_real_r2e_relation_matches_db_goal_without_becoming_proof() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase171_r2e_toda53_double_reference import ASSERTION_ID
    from expression import Multiple

    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=3)
    assert len(targets) == 1
    target = targets[0]
    source = bridge.registry.assertion("shared:12:" + ASSERTION_ID).content
    assert isinstance(source.lhs, Multiple) and source.lhs.coefficient == 2
    assert target.rhs.generator != source.lhs.expression
    assert same_registered_group_presentation(
        target.rhs, FiniteCyclicGroup(4, source.lhs.expression),
    )
    assert not any(link.step is not None and link.step.conclusion == target
                   for link in bridge.proof_links)
