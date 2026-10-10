from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r12_literature_registration import (
    existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)
from phase163_r4_r12_stable_bases import (
    BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2,
    _check_pi4_3, existing_stable_minimal_registration,
    register_stable_minimal_dimensions,
)
from unified_statement_registry import AssertionOrigin
from toda_upstream_bootstrap import _build_phase50_result


def _previous():
    return register_prop51_prop53_literature_statements(
        build_registry_bridge(), existing_prop51_prop53_candidates()
    )


def test_minimal_stems_are_distinct_typed_entries():
    result = existing_stable_minimal_registration()
    first = result.snapshot.registry.assertion(BASE_ID_1)
    second = result.snapshot.registry.assertion(BASE_ID_2)
    assert first.content.lhs == TodaPrimaryGroup(group_dimension=4, sphere_dimension=3)
    assert second.content.lhs == TodaPrimaryGroup(group_dimension=6, sphere_dimension=4)
    assert first.origin is AssertionOrigin.PROOF_INTERNAL
    assert second.origin is AssertionOrigin.FIXED_STATEMENT
    assert result.base_1_id != result.base_2_id


def test_correct_boundaries_do_not_specialize_n4_from_n_ge_5():
    result = existing_stable_minimal_registration()
    assert result.snapshot.registry.assertion(GENERAL_ID_1).scope == "n >= 3"
    assert result.snapshot.registry.assertion(GENERAL_ID_2).scope == "n >= 5"
    assert result.relation_1 == "WITHIN_GENERAL_SCOPE_N_EQUALS_3"
    assert result.relation_2 == "INDEPENDENT_MINIMUM_N_EQUALS_4_OUTSIDE_GENERAL_N_GE_5"


def test_pi4_3_generator_is_preserved():
    statement = existing_stable_minimal_registration().snapshot.registry.assertion(BASE_ID_1).content
    assert statement.rhs.order == 2
    assert statement.rhs.generator.generator == GeneratorSymbol(family="η", index=3)
    assert statement.rhs.generator.source == 4
    assert statement.rhs.generator.target == 3


def test_rejects_incorrect_pi4_3_generator():
    statement = _build_phase50_result()["final_group_step"].conclusion
    wrong = replace(statement, rhs=FiniteCyclicGroup(
        order=2,
        generator=HomotopyElement(name="η₅", dimension=5, source=6, target=5,
                                 generator=GeneratorSymbol(family="η", index=5)),
    ))
    with pytest.raises(ValueError):
        _check_pi4_3(wrong)


def test_rejects_incorrect_pi4_3_order():
    statement = _build_phase50_result()["final_group_step"].conclusion
    with pytest.raises(ValueError):
        _check_pi4_3(replace(statement, rhs=FiniteCyclicGroup(
            order=4, generator=statement.rhs.generator
        )))


def test_preserves_existing_eight_and_proof_links():
    previous = _previous()
    statement = _build_phase50_result()["final_group_step"].conclusion
    result = register_stable_minimal_dimensions(previous, statement)
    assert result.snapshot.proof_links == previous.snapshot.proof_links
    assert result.snapshot.records[:-1] == previous.snapshot.records
    for evidence in previous.evidence:
        assert (result.snapshot.registry.assertion(evidence.assertion_id)
                == previous.snapshot.registry.assertion(evidence.assertion_id))
    assert result.snapshot.records[-1].status is MigrationStatus.STRUCTURED


def test_no_unverified_proofstep_link_is_added():
    result = existing_stable_minimal_registration()
    assert all(link.assertion_id != BASE_ID_1 for link in result.snapshot.proof_links)
    assert result.source_status == "SOURCE_UNVERIFIED"
    assert result.proof_status == "PROOF_ANCESTRY_NOT_CHECKED"


def test_rejects_untyped_previous_result():
    with pytest.raises(TypeError):
        register_stable_minimal_dimensions(object(), object())
