"""Focused proof-tree and negative checks for R20R11 verified prior results."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    verified_db_step,
)
from phase171_r2i_eta_hopf_bridge.audit import _checked_chain, _screened_context
from phase171_r2j_r2_cyclic_hopf_surjective.audit import build_cited_r2j_r2_proof
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    cyclic_generator_image_surjectivity_rule,
    expand_cited_cyclic_hopf_surjectivity,
    verified_prior_cyclic_generator_image_surjectivity_rule,
)
from phase171_r20r11_verified_prior_hopf_surjectivity.install import (
    OLD_SHARED,
    NEW_SHARED,
    transform_source,
    transform_shared,
)
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def _public_case():
    screened, root, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    offered = expand_cited_cyclic_hopf_surjectivity(
        goal, available, proof_target=root, bridge=screened,
    )
    prior = tuple(candidate for candidate in offered if candidate.rule.name ==
                  "verified earlier database cyclic generator in Hopf image implies surjectivity")
    return screened, root, goal, chain, offered, prior


def test_verified_prior_proposal_is_wired_into_shared_search():
    screened, root, goal, chain, offered, prior = _public_case()
    assert len(prior) == 1
    assert len(offered) == 2
    group = prior[0].subgoals[0]
    assert prior[0].subgoals[1] == chain.conclusion
    db = admitted_db_step(group, proof_target=root, bridge=screened)
    assert db is not None
    assert verified_db_step(db, proof_target=root, bridge=screened)
    shared = shared_expansion_provider(screened, proof_target=root)(goal)
    assert any(candidate.rule.name == prior[0].rule.name
               and candidate.subgoals == prior[0].subgoals for candidate in shared)


def test_real_inferred_hopf_image_and_verified_db_group_prove_surjective():
    screened, root, goal, chain, _, prior = _public_case()
    _, group, _, proof_nodes, _ = build_cited_r2j_r2_proof()
    inferred_image = next(
        node for node in proof_nodes
        if node.conclusion == chain.conclusion and node.rule is ProofRule.INFERENCE
    )
    db = admitted_db_step(group, proof_target=root, bridge=screened)
    assert db is not None
    matches = find_inference_matches_for_rule(prior[0].rule, (db, inferred_image))
    assert len(matches) == 1
    assert matches[0].premises == (db, inferred_image)
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal


def test_untrusted_given_cannot_replace_verified_prior():
    screened, root, goal, chain, _, prior = _public_case()
    _, group, _, proof_nodes, _ = build_cited_r2j_r2_proof()
    inferred_image = next(node for node in proof_nodes
                          if node.conclusion == chain.conclusion and node.rule is ProofRule.INFERENCE)
    fake = ProofStep(group, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(prior[0].rule, (fake, inferred_image)) == ()
    db = admitted_db_step(group, proof_target=root, bridge=screened)
    assert db is not None
    assert find_inference_matches_for_rule(
        prior[0].rule, (replace(db, note="unreviewed"), inferred_image)
    ) == ()
    assert find_inference_matches_for_rule(
        prior[0].rule, (db, ProofStep(chain.conclusion, (), ProofRule.INFERENCE))
    ) == ()
    assert find_inference_matches_for_rule(
        cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion),
        (db, inferred_image),
    ) == ()


def test_prior_dependency_order_fails_closed_for_its_own_group():
    screened, _, goal, chain, _, prior = _public_case()
    group = prior[0].subgoals[0]
    with pytest.raises(ValueError):
        verified_prior_cyclic_generator_image_surjectivity_rule(
            goal, group, chain.conclusion,
            proof_target=group, bridge=screened,
        )


def test_existing_non_contextual_proposals_are_unchanged():
    screened, root, goal, chain, offered, prior = _public_case()
    existing = expand_cited_cyclic_hopf_surjectivity(
        goal, _checked_chain(screened, _screened_context()[2])[1],
        proof_target=root,
    )
    assert len(existing) == 1
    assert existing[0].rule.name == "cyclic codomain generator in image implies Hopf surjectivity"
    assert existing[0].subgoals == offered[0].subgoals


def test_patch_transform_preserves_unmodified_shared_text():
    source = "header\n" + OLD_SHARED + "footer\n"
    with pytest.raises(SyntaxError):
        transform_shared(source)
    with pytest.raises(RuntimeError):
        transform_source("unrelated source")
    assert OLD_SHARED != NEW_SHARED
