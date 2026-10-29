"""R2I: cited Definition, proof ancestry, typed rewriting, and negative cases."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase171_r2i_eta_hopf_bridge.audit import (
    _available,
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2i_eta_hopf_bridge.source import (
    _make_chain,
    cited_eta_suspension_equality_rule,
    eligible_eta_hopf_chains,
    expand_cited_eta_hopf_power,
)
from phase169_r10eb_typed_composition_power.display import (
    typed_stable_composition_power_latex,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def _case():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    return chain, available


def test_r2i_cited_proof_tree_without_group_completion():
    proof, chain, ancestry = build_cited_r2i_proof()
    assert proof.conclusion == chain.conclusion
    assert proof.rule is ProofRule.INFERENCE
    assert chain.conclusion.lhs == MapApplication(
        EHP_H_MAP, Composition(chain.alpha, chain.eta_next),
    )
    assert chain.conclusion.rhs == Composition(chain.beta, chain.eta_next)
    assert sum(step.rule is ProofRule.GIVEN for step in ancestry) == 3
    assert sum(step.rule is ProofRule.INFERENCE for step in ancestry) >= 10
    assert all(step.rule is ProofRule.INFERENCE for step in ancestry if step.premises)


def test_r2i_uses_only_screened_both_general_sources():
    chain, available = _case()
    assert eligible_eta_hopf_chains(()) == ()
    without_eta = tuple(x for x in available if not isinstance(x, TodaEtaFamilyGeneralDefinition))
    without_hopf_formula = tuple(x for x in available if not isinstance(x, TodaProp22RightFormula))
    assert expand_cited_eta_hopf_power(chain.conclusion, without_eta) == ()
    assert expand_cited_eta_hopf_power(chain.conclusion, without_hopf_formula) == ()
    assert len(expand_cited_eta_hopf_power(chain.conclusion, available)) == 1


def test_r2i_rejects_wrong_types_and_unrelated_primitive():
    chain, available = _case()
    wrong_beta = replace(chain.beta, source=100)
    wrong_hopf = Relation(
        MapApplication(EHP_H_MAP, chain.alpha),
        wrong_beta,
        RelationType.EQUALITY,
    )
    assert _make_chain(wrong_hopf) is None
    fake = replace(chain.conclusion, rhs=chain.beta)
    assert expand_cited_eta_hopf_power(fake, available) == ()
    assert expand_cited_eta_hopf_power(chain.conclusion, ()) == ()
    with pytest.raises(ValueError):
        cited_eta_suspension_equality_rule(
            Relation(Suspension(wrong_beta), chain.eta_next, RelationType.EQUALITY),
            chain.generator_suspension,
        )


def test_r2i_rejects_fake_given_generator_suspension():
    chain, available = _case()
    rule = cited_eta_suspension_equality_rule(
        chain.eta_forward, chain.generator_suspension,
    )
    forged_leaf = ProofStep(
        conclusion=chain.generator_suspension,
        premises=(),
        rule=ProofRule.GIVEN,
    )
    assert find_inference_matches_for_rule(rule, (forged_leaf,)) == ()
    proposals = expand_cited_eta_hopf_power(chain.eta_forward, available)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (chain.generator_suspension,)


def test_r2i_eta_squared_is_a_typed_composition_not_given():
    proof, chain, ancestry = build_cited_r2i_proof()
    assert isinstance(chain.conclusion.rhs, Composition)
    assert chain.conclusion.rhs.is_type_compatible()
    assert typed_stable_composition_power_latex(chain.conclusion.rhs) == r"\eta_{5}^{2}"
    assert all(step.conclusion != chain.conclusion for step in ancestry if step.rule is ProofRule.GIVEN)
