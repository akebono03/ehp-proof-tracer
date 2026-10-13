from homotopy_groups import (
    TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement,
    FreeCyclicGroup,
)
from proof import ProofStep, ProofRule, Relation, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r14_diagonal_and_prop42 import (
    diagonal_suspension_subgoals, expand_diagonal_suspension,
    diagonal_suspension_isomorphism_rule, review_prop42_scope, audit_r14,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


def _goal(n=1):
    return TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(n,n),TodaPrimaryGroup(n+1,n+1))
    )


def _given(x):
    return ProofStep(x, (), ProofRule.GIVEN)


def test_diagonal_expansion_supplies_three_independent_subgoals():
    result = expand_diagonal_suspension(_goal())
    assert len(result) == 1
    assert len(result[0].subgoals) == 3


def test_diagonal_inference_on_fixture_steps():
    expansion = expand_diagonal_suspension(_goal())[0]
    matches = find_inference_matches_for_rule(
        expansion.rule, tuple(_given(x) for x in expansion.subgoals)
    )
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == _goal()


def test_wrong_target_generator_cannot_prove_isomorphism():
    exp = expand_diagonal_suspension(_goal())[0]
    a, b, image = exp.subgoals
    altered = Relation(b.lhs, FreeCyclicGroup(a.rhs.generator))
    assert find_inference_matches_for_rule(
        exp.rule, (_given(a), _given(altered), _given(image))
    ) == ()


def test_non_diagonal_suspension_is_rejected():
    invalid = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(2,1),TodaPrimaryGroup(3,2))
    )
    assert expand_diagonal_suspension(invalid) == ()


def test_prop42_candidates_never_automatically_certified():
    bridge, _ = build_phase165_r5_manifest_bridge()
    rows = review_prop42_scope(bridge)
    assert len(rows) == 2
    assert all(not row["proof_eligible"] for row in rows)
    assert all(not row["mathematical_clause_selected"] for row in rows)


def test_read_only_audit_not_proof():
    bridge, _ = build_phase165_r5_manifest_bridge()
    before = (len(bridge.registry._assertions), len(bridge.proof_links))
    report = audit_r14(bridge)
    assert (len(bridge.registry._assertions),len(bridge.proof_links)) == before
    assert report["diagonal_expansions"] == 1
    assert report["toda_proof_steps_created"] == 0
