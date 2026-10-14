from dataclasses import replace

import pytest

from phase165_r52_r17_internal_dependency import (
    CompletedInternalProof,
    depends_on,
    find_reusable_internal_proof,
)
from proof import ProofRule, ProofStep


def _proof():
    leaf = ProofStep(conclusion="base", premises=(), rule=ProofRule.GIVEN)
    middle = ProofStep(conclusion="pi3_2", premises=(leaf,), rule=ProofRule.INFERENCE)
    last = ProofStep(conclusion="pi4_3", premises=(middle,), rule=ProofRule.INFERENCE)
    return middle, last


def test_completed_pi43_reusable_for_distinct_later_goal():
    middle, last = _proof()
    assert find_reusable_internal_proof("pi4_3", "pi5_4", (CompletedInternalProof(last),)) is last
    assert find_reusable_internal_proof("pi4_3", "pi5_3", (CompletedInternalProof(last),)) is last


def test_proof_cannot_cite_its_own_conclusion():
    middle, last = _proof()
    assert find_reusable_internal_proof("pi4_3", "pi4_3", (CompletedInternalProof(last),)) is None


def test_reverse_dependency_is_not_accepted():
    middle, last = _proof()
    assert depends_on(last, "pi3_2")
    assert find_reusable_internal_proof("pi4_3", "pi3_2", (CompletedInternalProof(last),)) is None


def test_given_or_invalid_ancestry_not_completed_internal_proof():
    with pytest.raises(ValueError):
        CompletedInternalProof(ProofStep(conclusion="x", premises=(), rule=ProofRule.GIVEN))
    child = ProofStep(conclusion="x", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="x", premises=(child,), rule=ProofRule.INFERENCE)
    with pytest.raises(ValueError, match="self-dependent"):
        CompletedInternalProof(root)


def test_internal_proof_is_a_distinct_non_given_step():
    middle, last = _proof()
    assert find_reusable_internal_proof("pi3_2", "pi4_3", (CompletedInternalProof(middle),)) is middle
    assert middle.rule is ProofRule.INFERENCE


def test_multiple_proven_results_are_ambiguous():
    middle, last = _proof()
    another = replace(last)
    with pytest.raises(ValueError, match="ambiguous"):
        find_reusable_internal_proof("pi4_3", "other", (CompletedInternalProof(last), CompletedInternalProof(another)))
