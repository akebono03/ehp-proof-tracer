"""Focused evidence extraction guards; do not assume pi3^2 is complete."""
from dataclasses import dataclass

from phase165_r12_r18_evidence_reuse import extract_completed_root, find_screened_generator_witness
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class FakeResult:
    status: ProofSearchStatus
    conclusion: object
    proven_steps: tuple[ProofStep, ...]
    open_goals: tuple[object, ...] = ()


def test_complete_inference_root_reused():
    goal = "some group result"
    step = ProofStep(goal, (), ProofRule.INFERENCE)
    found = extract_completed_root(FakeResult(ProofSearchStatus.COMPLETE, goal, (step,)), goal)
    assert found.status == "PROVEN_ROOT"
    assert found.proof is step


def test_partial_or_given_result_never_promoted():
    goal = "some group result"
    inference = ProofStep(goal, (), ProofRule.INFERENCE)
    given = ProofStep(goal, (), ProofRule.GIVEN)
    assert extract_completed_root(FakeResult(ProofSearchStatus.PARTIAL, None, (inference,)), goal).proof is None
    assert extract_completed_root(FakeResult(ProofSearchStatus.COMPLETE, goal, (given,)), goal).proof is None


def test_missing_generator_witness_stays_unresolved():
    class Bridge:
        proof_links = ()
    result = find_screened_generator_witness(Bridge(), "generator image")
    assert result.status == "UNRESOLVED"
