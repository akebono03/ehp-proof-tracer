"""Source-bound equality-symmetry and public-provider regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.audit import (
    _git,
    inspect_public_eta_symmetry,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.install import (
    R11_HOOK,
    _complete_function,
    install,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    cited_chain_forward_equalities,
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    screened, target, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    return screened, target, chain, available


def test_first_reverse_requires_actual_forward_proof_obligation():
    _, _, chain, available = _case()
    goal = reverse_equality(chain.alpha_composition)
    assert goal is not None
    proposal, = expand_reverse_cited_eta_hopf_equalities(goal, available)
    assert proposal.rule.name == "equality symmetry"
    assert proposal.subgoals == (chain.alpha_composition,)
    assert not any(isinstance(item, ProofStep) for item in proposal.subgoals)


def test_all_forward_orientations_are_screened_and_reversible():
    _, _, chain, available = _case()
    forwards = cited_chain_forward_equalities(available)
    assert chain.alpha_composition in forwards
    assert chain.conclusion in forwards
    assert len(forwards) >= 5
    for forward in forwards:
        reverse = reverse_equality(forward)
        assert reverse is not None
        proposals = expand_reverse_cited_eta_hopf_equalities(reverse, available)
        assert len(proposals) == 1
        assert proposals[0].subgoals == (forward,)


def test_source_free_and_incomplete_source_sets_cannot_propose_reversal():
    _, _, chain, available = _case()
    reverse = reverse_equality(chain.alpha_composition)
    assert expand_reverse_cited_eta_hopf_equalities(reverse, ()) == ()
    without_definition = tuple(item for item in available
                               if item != TodaEtaFamilyGeneralDefinition())
    assert expand_reverse_cited_eta_hopf_equalities(reverse, without_definition) == ()


def test_wrong_relation_and_wrong_generator_do_not_match():
    _, _, chain, available = _case()
    reverse = reverse_equality(chain.alpha_composition)
    assert reverse is not None
    invalid = replace(reverse, relation_type=RelationType.INEQUALITY)
    assert expand_reverse_cited_eta_hopf_equalities(invalid, available) == ()
    alien = HomotopyElement("alien", 3, source=6, target=3,
                            generator=GeneratorSymbol("alien"))
    mismatched = replace(reverse, lhs=alien)
    assert expand_reverse_cited_eta_hopf_equalities(mismatched, available) == ()
    assert expand_reverse_cited_eta_hopf_equalities(object(), available) == ()


def test_reverse_equality_refuses_nonsymmetric_statement_or_trivial_cycle():
    _, _, chain, available = _case()
    forward = chain.alpha_composition
    assert reverse_equality(object()) is None
    assert reverse_equality(replace(forward, relation_type=RelationType.ZERO)) is None
    assert reverse_equality(Relation("x", "x", RelationType.EQUALITY)) is None
    with pytest.raises(TypeError):
        expand_reverse_cited_eta_hopf_equalities(forward, [available])


def test_symmetry_matches_only_a_proved_forward_step_from_real_r2i():
    _, _, chain, available = _case()
    root, actual, ancestry = build_cited_r2i_proof()
    assert root.rule is ProofRule.INFERENCE
    assert actual == chain
    original, = tuple(node for node in ancestry
                      if node.conclusion == chain.alpha_composition
                      and node.rule is ProofRule.INFERENCE)
    goal = reverse_equality(chain.alpha_composition)
    route, = expand_reverse_cited_eta_hopf_equalities(goal, available)
    matches = find_inference_matches_for_rule(route.rule, (original,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (original,)


def test_shared_provider_exposes_exact_inverse_route():
    screened, target, chain, available = _case()
    inverse = reverse_equality(chain.alpha_composition)
    proposals = shared_expansion_provider(screened, proof_target=target)(inverse)
    matches = tuple(item for item in proposals
                    if item.rule.name == "equality symmetry"
                    and item.subgoals == (chain.alpha_composition,))
    assert len(matches) == 1
    assert len(expand_reverse_cited_eta_hopf_equalities(inverse, available)) == 1


def test_guarded_installer_is_idempotent_in_dry_run():
    from pathlib import Path
    assert install(dry_run=True) is False
    import phase165_r52_r9_shared_math as module
    function = _complete_function(Path(module.__file__).read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    assert function.count(R11_HOOK) == 1


def test_read_only_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_public_audit_is_fail_closed_and_does_not_replay_old_tree():
    report = inspect_public_eta_symmetry()
    assert report["first_reverse_inference_matched"] is True
    assert report["shared_first_reverse_connected"] is True
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False
    assert report["public_search_status"] in ("complete", "partial", "search_failed")
