from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r13_inventory import (
    InventoryClassification,
    _generator_assessment,
    inventory_registry_snapshot,
)
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup
from proof import Relation, RelationType


def test_inventory_original_boundary_is_metadata_only():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    assert report.count(InventoryClassification.METADATA_ONLY) > 0
    assert any(item.component_key == "pi6_4_group_relation" and
               item.classification is InventoryClassification.METADATA_ONLY for item in report.items)


def test_inventory_does_not_assume_scope_was_typed_checked():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    item = next(i for i in report.items if i.assertion_id ==
                "boundary:Proposition 5.3:higher_eta_squared_group_relation")
    assert item.scope_text == "n >= 5"
    assert item.scope_assessment == "TEXT_SCOPE_ONLY_NOT_CHECKED"


def test_inventory_records_no_phantom_source_verification():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    assert report.count(InventoryClassification.TYPED_SOURCE_UNVERIFIED) == 0


def test_inventory_refuses_unknown_evidence_id():
    with pytest.raises(ValueError, match="absent assertion"):
        inventory_registry_snapshot(build_registry_bridge(), frozenset({"unknown"}), frozenset())


def test_inventory_refuses_scope_without_typed_evidence():
    with pytest.raises(ValueError, match="typed scope ids"):
        inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset({"x"}))


def test_generator_assessment_for_cyclic_and_direct_sum():
    def relation(rhs):
        return Relation(lhs="group", rhs=rhs, relation_type=RelationType.EQUALITY)
    assert _generator_assessment(relation(FiniteCyclicGroup(order=2, generator="eta"))) == "PRESENT"
    assert _generator_assessment(relation(FreeCyclicGroup(generator="nu"))) == "PRESENT"
    assert _generator_assessment(relation(DirectSumGroup(summands=(
        FreeCyclicGroup(generator="nu"), FiniteCyclicGroup(order=4, generator="E_nu")
    )))) == "PRESENT"


def test_metadata_inventory_does_not_mutate_bridge():
    baseline = build_registry_bridge()
    before = tuple((r.assertion_id, r.status) for r in baseline.records)
    inventory_registry_snapshot(baseline, frozenset(), frozenset())
    assert before == tuple((r.assertion_id, r.status) for r in baseline.records)
