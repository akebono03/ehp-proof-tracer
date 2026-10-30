"""Focused, fail-closed checks of scoped rule-only public-path experiment."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r9_r2_scoped_search_bridge.audit import _git
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import InferenceRule, ProofRule, ProofStep


def _fixture():
    cited = ProofStep("earlier-cited", (), ProofRule.GIVEN)
    rule = InferenceRule(name="typed inference")
    root = ProofStep("derived", (cited,), ProofRule.INFERENCE, inference_rule=rule)
    return cited, root


def test_catalog_extracts_only_subgoals_not_prior_proofsteps():
    cited, root = _fixture()
    assert walk_proof_ancestry(root) == (cited, root)
    catalog = inference_expansion_catalog(root)
    assert len(catalog) == 1
    assert catalog[0][0] == "derived"
    assert catalog[0][1].subgoals == ("earlier-cited",)
    assert all(not isinstance(item, ProofStep) for item in catalog[0][1].subgoals)


def test_scoped_provider_prioritizes_exact_rule_and_delegates_other_goals():
    _, root = _fixture()
    fallback = lambda goal: (GoalExpansion(InferenceRule(name="fallback"), (goal,)),)
    provider = scoped_expansion_provider(root, fallback)
    assert provider("derived") == (GoalExpansion(root.inference_rule, ("earlier-cited",)),)
    assert provider("other") == fallback("other")


def test_rejects_fake_given_and_noninference_premise():
    cited, root = _fixture()
    with pytest.raises(ValueError, match="GIVEN"):
        walk_proof_ancestry(replace(cited, premises=(root,)))
    with pytest.raises(ValueError, match="inferred"):
        walk_proof_ancestry(replace(root, inference_rule=None))
    with pytest.raises(ValueError, match="unverified"):
        walk_proof_ancestry(ProofStep("foreign", (), ProofRule.RELATION))


def test_duplicate_conclusion_with_two_incompatible_rules_fails_closed():
    cited, root = _fixture()
    other = ProofStep("derived", (cited,), ProofRule.INFERENCE,
                      inference_rule=InferenceRule(name="different"))
    final = ProofStep("final", (root, other), ProofRule.INFERENCE,
                      inference_rule=InferenceRule(name="combine"))
    with pytest.raises(ValueError, match="ambiguous"):
        inference_expansion_catalog(final)


def test_cyclic_proof_is_rejected():
    cited, root = _fixture()
    object.__setattr__(root, "premises", (root,))
    with pytest.raises(ValueError, match="cyclic"):
        walk_proof_ancestry(root)


def test_invalid_fallback_provider_fails_closed():
    _, root = _fixture()
    with pytest.raises(TypeError):
        scoped_expansion_provider(root, object())
    provider = scoped_expansion_provider(root, lambda goal: ["invalid"])
    with pytest.raises(TypeError):
        provider("other")


def test_readonly_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")
