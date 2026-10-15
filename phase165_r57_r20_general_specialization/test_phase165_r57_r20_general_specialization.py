"""R57-R20: typed universal-source instantiation and proof-use-order checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSymbol
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r57_r20_general_specialization import (
    build_adopted_toda51_diagonal_reference,
    expand_cited_general_specialization,
    specialize_typed_statement,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from proof import ProofRule, Relation, RelationType, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from unified_statement_registry import AssertionOrigin


def _tex_path() -> Path:
    return Path(__file__).resolve().parent.parent / "phase165_r14_r39_toda51.tex"


def _diagonal_goal(n: int) -> Relation:
    return Relation(
        lhs=TodaPrimaryGroup(n, n),
        rhs=FreeCyclicGroup(HomotopyElement(
            name="ι_" + str(n), dimension=n,
            generator=GeneratorSymbol(family="ι", index=n),
        )),
        relation_type=RelationType.EQUALITY,
    )


def _source():
    bridge = build_adopted_toda51_diagonal_reference(_tex_path())
    link, = bridge.proof_links
    return bridge, link.step


def test_r20_cited_symbolic_diagonal_has_exact_toda_51_provenance():
    bridge, step = _source()
    assertion, = bridge.registry._assertions.values()
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(assertion.reference_id).locator == "(5.1)"
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == assertion.content
    assert isinstance(step.conclusion.lhs.sphere_dimension, ScalarSymbol)


def test_r20_single_general_template_works_for_arbitrary_positive_n():
    _, step = _source()
    for n in (1, 3, 5, 10, 100):
        goal = _diagonal_goal(n)
        assert specialize_typed_statement(step.conclusion, goal) == (("n", n),)
        expansion, = expand_cited_general_specialization(goal, (step.conclusion,))
        matches = find_inference_matches_for_rule(expansion.rule, (step,))
        assert len(matches) == 1
        derived = derive_inference_proof_step(matches[0])
        assert derived.rule is ProofRule.INFERENCE
        assert derived.conclusion == goal


def test_r20_missing_cited_source_never_yields_specialization():
    goal = _diagonal_goal(5)
    assert expand_cited_general_specialization(goal, ()) == ()
    assert specialize_typed_statement(goal, goal) is None


def test_r20_wrong_dimensions_and_generator_are_rejected():
    _, step = _source()
    bad_dimension = Relation(TodaPrimaryGroup(6, 5), _diagonal_goal(5).rhs)
    bad_generator = Relation(TodaPrimaryGroup(5, 5), FreeCyclicGroup(
        HomotopyElement("ι_5", dimension=5, generator=GeneratorSymbol("η", 5)),
    ))
    for goal in (bad_dimension, bad_generator, _diagonal_goal(0)):
        assert expand_cited_general_specialization(goal, (step.conclusion,)) == ()


def test_r20_missing_or_changed_original_clause_rejected(tmp_path: Path):
    source = tmp_path / "toda.tex"
    source.write_text(r"\pi^{n}_{n}=\mathbb Z", encoding="utf8")
    with pytest.raises(ValueError):
        build_adopted_toda51_diagonal_reference(source)


def test_r20_screened_shared_expansion_preserves_diagonal_order_boundary():
    bridge = build_shared_typed_bridge()
    diagonal = _diagonal_goal(5)
    proposals = shared_expansion_provider(bridge, proof_target=diagonal)(diagonal)
    matching = tuple(x for x in proposals
                     if getattr(x.rule, "name", "") == "generic cited typed scalar specialization")
    assert len(matching) == 1
    assert matching[0].subgoals[0].lhs.group_dimension == ScalarSymbol("n")
    assert retain_ordered_root_expansions(diagonal, diagonal, matching) == matching


def test_r20_higher_eta_root_still_blocked_by_order_gate():
    from phase165_r57_r8_eta_specialization import specialize_eta_group_relation
    from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
    from phase165_r57_r8_eta_specialization import _fixed_typed_relations
    bridge = build_adopted_prop51_reference()
    source, = _fixed_typed_relations(bridge)
    goal = specialize_eta_group_relation(source, 4)
    from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
    expansion, = expand_registered_eta_specialization(goal, (source,))
    assert retain_ordered_root_expansions(goal, goal, (expansion,)) == ()
