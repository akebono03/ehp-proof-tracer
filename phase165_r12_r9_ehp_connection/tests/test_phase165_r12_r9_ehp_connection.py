import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r9_ehp_connection import (
    ExactnessWindowWitness,
    classify_ehp_exactness_windows,
    collect_screened_exactness_windows,
)
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _bridge(rule=ProofRule.GIVEN, origin=AssertionOrigin.FIXED_STATEMENT):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("ref", ReferenceKind.PROPOSITION, "Proposition 4.2"))
    value = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(5, 5),
        middle_term=TodaPrimaryGroup(3, 2),
        target_term=TodaPrimaryGroup(4, 3),
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    ))
    registry.add_assertion(AssertionEntry(
        "fact", "ref", AssertionKind.STATEMENT, value, origin=origin,
    ))
    return RegistryBridgeResult(
        registry, (), (ProofStepLink("fact", step=ProofStep(value, (), rule)),),
    )


def test_r9_reads_fixed_typed_exactness():
    found = collect_screened_exactness_windows(_bridge())
    assert len(found) == 1
    assert found[0].assertion_id == "fact"
    assert len(classify_ehp_exactness_windows(found)["delta_e"]) == 1


def test_r9_never_promotes_inference_or_internal_claim():
    assert collect_screened_exactness_windows(_bridge(rule=ProofRule.INFERENCE)) == ()
    assert collect_screened_exactness_windows(
        _bridge(origin=AssertionOrigin.PROOF_INTERNAL)
    ) == ()


def test_r9_classifies_other_exactness_pairs_without_inference():
    rows = (
        ExactnessWindowWitness("a", EHP_E_MAP, EHP_H_MAP, 1, 2, 3),
        ExactnessWindowWitness("b", EHP_H_MAP, EHP_DELTA_MAP, 2, 3, 4),
    )
    groups = classify_ehp_exactness_windows(rows)
    assert len(groups["e_h"]) == 1
    assert len(groups["h_delta"]) == 1
    assert groups["delta_e"] == ()


def test_r9_rejects_wrong_source_type():
    with pytest.raises(TypeError):
        collect_screened_exactness_windows(object())
    with pytest.raises(TypeError):
        classify_ehp_exactness_windows((object(),))
