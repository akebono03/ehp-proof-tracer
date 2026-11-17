"""Real-repository integration, intentionally no prior-proof replay.

Runs only in the real repository, never in the mock-only authoring runner.
"""
from __future__ import annotations

import pytest

from expression import Multiple, Zero
from homotopy_groups import DirectSumGroup
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, verified_db_step,
)
from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
from phase175_r4r5r3_public_order_zero.provider import build_public_order_zero_provider
from proof import (
    ProofRule, Relation, RelationType, apply_inference_match,
    find_inference_matches_for_rule,
)


def test_real_ordered_db_prior_generator_and_both_summands_public_proposals() -> None:
    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    direct = exact_prior_database_result(4, 4)
    assert isinstance(root, Relation)
    assert isinstance(eta, Relation)
    assert isinstance(direct, Relation)
    assert isinstance(direct.rhs, DirectSumGroup)
    sources = [eta] + [direct for _ in direct.rhs.summands]
    generators = [(eta.rhs.order, eta.rhs.generator)] + [
        (part.order, part.generator) for part in direct.rhs.summands
    ]
    for source, (m, generator) in zip(sources, generators):
        prior = admitted_db_step(source, proof_target=root)
        assert prior is not None and verified_db_step(prior, proof_target=root)
        goal = Relation(Multiple(m, generator), Zero(), RelationType.EQUALITY)
        proposals = build_public_order_zero_provider(
            bridge=object(), proof_target=root,
        )(goal)
        assert len(proposals) == 1
        assert proposals[0].rule.name == RULE_NAME
        assert proposals[0].subgoals == (source,)
        match = find_inference_matches_for_rule(proposals[0].rule, (prior,))
        assert len(match) == 1
        inferred = apply_inference_match(match[0])
        assert inferred.rule is ProofRule.INFERENCE
        assert inferred.conclusion == goal
        assert inferred.premises == (prior,)


def test_real_shared_expansion_provider_has_installed_general_rule() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase175_r4r5r3_public_order_zero.installer import INSERTION
    import inspect

    assert "build_public_order_zero_provider" in inspect.getsource(shared_expansion_provider)
    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    assert root is not None and eta is not None
    goal = Relation(Multiple(2, eta.rhs.generator), Zero())
    bridge = build_shared_typed_bridge()
    providers = shared_expansion_provider(bridge, proof_target=root)
    options = providers(goal)
    relevant = [o for o in options if o.rule.name == RULE_NAME]
    assert len(relevant) >= 1
    assert all(o.subgoals == (eta,) for o in relevant)
