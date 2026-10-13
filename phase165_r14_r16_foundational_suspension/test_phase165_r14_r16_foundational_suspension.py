import pytest

from phase165_r14_r16_foundational_suspension import (
    FOUNDATIONAL_SUSPENSION_IDENTITY,
    instantiate_foundational_identity_suspension,
    bind_foundational_diagonal_obligations,
    audit_r16,
)


def test_foundational_claim_is_general_and_well_typed():
    for n in (1, 2, 3, 7):
        c = instantiate_foundational_identity_suspension(n)
        assert c.statement.map.source_group.sphere_dimension == n
        assert c.statement.map.target_group.sphere_dimension == n + 1
        assert c.statement.source_generator.generator.index == n
        assert c.statement.target_generator.generator.index == n + 1
        assert c.reference == FOUNDATIONAL_SUSPENSION_IDENTITY


@pytest.mark.parametrize("invalid", (0, -1, True, 1.5, "2"))
def test_invalid_dimensions_fail_closed(invalid):
    with pytest.raises(ValueError):
        instantiate_foundational_identity_suspension(invalid)


def test_foundational_fact_is_not_falsely_attributed_to_toda():
    c = instantiate_foundational_identity_suspension(1)
    assert c.literature_assertion_id is None
    assert not c.independently_reviewed
    assert not c.proof_eligible


def test_diagonal_dependencies_preserved():
    goals = bind_foundational_diagonal_obligations(1)
    assert len(goals) == 3
    assert goals[2] == instantiate_foundational_identity_suspension(1).statement


def test_proposition42_is_not_certified_by_foundational_identity():
    report = audit_r16()
    assert report["prop42_candidate_count"] == 2
    assert not report["prop42_clause_selected"]
    assert report["new_proof_steps"] == 0
    assert not report["foundational_claim_proof_eligible"]
