import pytest
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from phase165_r14_r14_diagonal_and_prop42 import diagonal_suspension_subgoals
from phase165_r14_r18_diagonal_integration import (
    DiagonalEvidenceMissing, derive_diagonal_iso_from_certified_groups, audit_r18,
)
from proof import ProofRule, ProofStep


def _fixture(n=1):
    suspension = TodaSuspensionMap(TodaPrimaryGroup(n, n), TodaPrimaryGroup(n+1,n+1))
    group_goals = diagonal_suspension_subgoals(suspension)[:2]
    return suspension, tuple(ProofStep(goal, (), ProofRule.GIVEN) for goal in group_goals)


def test_derivation_with_explicit_fixture_group_proof_steps():
    suspension, steps = _fixture()
    result = derive_diagonal_iso_from_certified_groups(suspension, *steps)
    assert result.conclusion == TodaSuspensionIsomorphismStatement(suspension)
    assert result.rule is ProofRule.INFERENCE
    assert len(result.premises) == 3
    assert result.premises[2].foundational_reference is not None


def test_general_diagonal_degree_is_supported():
    suspension, steps = _fixture(4)
    assert derive_diagonal_iso_from_certified_groups(suspension, *steps).conclusion.map == suspension


def test_missing_toda_leaves_are_rejected():
    suspension, steps = _fixture()
    with pytest.raises(DiagonalEvidenceMissing):
        derive_diagonal_iso_from_certified_groups(suspension, None, steps[1])
    with pytest.raises(DiagonalEvidenceMissing):
        derive_diagonal_iso_from_certified_groups(suspension, steps[0], None)


def test_wrong_group_step_is_rejected():
    suspension, steps = _fixture()
    other, wrong = _fixture(3)
    with pytest.raises(DiagonalEvidenceMissing):
        derive_diagonal_iso_from_certified_groups(suspension, wrong[0], steps[1])


def test_non_diagonal_map_is_rejected():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(3,2), TodaPrimaryGroup(4,3))
    with pytest.raises(DiagonalEvidenceMissing):
        derive_diagonal_iso_from_certified_groups(suspension, None, None)


def test_real_registry_has_no_automatic_promotion():
    report = audit_r18()
    assert report["fail_closed_on_missing_group_steps"]
    assert report["verified_toda_group_steps_supplied"] == 0
    assert not report["pi32_proved"]
    assert not report["prop42_semantics_certified"]
    assert report["new_toda_proof_steps"] == 0
