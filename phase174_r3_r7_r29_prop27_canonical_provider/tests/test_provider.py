"""R29 canonical backward provider and source-bound ancestry tests."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
    PROVIDER_ID, build_canonical_prop27_context,
    expand_cited_prop27_goal, search_canonical_prop27_instance,
)
from phase174_r3_r7_r29_prop27_canonical_provider.audit import allow_paths
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parents[2]


def test_context_uses_canonical_shared_bridge_and_registry():
    bridge, providers = build_canonical_prop27_context(ROOT)
    assert len(bridge.proof_links) == 1
    assert len(providers.entries()) == 1
    assert providers.entries()[0].provider_id == PROVIDER_ID
    assert providers.entries()[0].origin == "SHARED_CITED_CONTEXT"


def test_registered_general_goal_has_exact_universal_premise():
    proposals = expand_cited_prop27_goal(Prop27GeneralTheoremPremise())
    assert len(proposals) == 1
    assert proposals[0].subgoals == (Prop27UniversalLiteratureStatement(),)


def test_cited_specialization_proposal_is_general_not_given():
    proposals = expand_cited_prop27_goal(typed_specialization(6))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (Prop27GeneralTheoremPremise(),)


@pytest.mark.parametrize("n", [2, 4, 6, 8])
def test_canonical_backward_inference_keeps_provenance(n):
    step = search_canonical_prop27_instance(ROOT, n)
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == typed_specialization(n)
    assert len(step.premises) == 1
    general = step.premises[0]
    assert general.rule is ProofRule.INFERENCE
    assert general.premises[0].rule is ProofRule.GIVEN
    assert type(general.premises[0].conclusion) is Prop27UniversalLiteratureStatement
    assert step.inference_rule.literature_reference.locator == "Proposition 2.7"


def test_forged_signed_instance_has_no_candidate():
    forged = replace(typed_specialization(6), sign_undetermined=False)
    assert expand_cited_prop27_goal(forged) == ()


def test_no_unrelated_goal_candidate():
    assert expand_cited_prop27_goal("pi_12^7=0") == ()
    assert expand_cited_prop27_goal(Prop27GeneralTheoremPremise(only_even_n=False)) == ()


def test_odd_dimensions_are_not_admitted():
    with pytest.raises(ValueError):
        search_canonical_prop27_instance(ROOT, 5)


def test_source_guard_rejects_unreviewed_paths():
    assert allow_paths(("phase174_r3_r7_r28_prop27_typed_literature_registration/README.md",))
    assert allow_paths(("phase174_r3_r7_r29_prop27_canonical_provider/provider.py",))
    for path in ("proof.py", "phase165_r52_r9_shared_math.py", ".pytest_cache/v/cache/lastfailed"):
        with pytest.raises(RuntimeError):
            allow_paths((path,))
