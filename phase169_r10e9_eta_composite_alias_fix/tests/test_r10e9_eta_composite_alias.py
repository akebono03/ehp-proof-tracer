"""R10E9: typed eta name alias, independent citation and composition proofs."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r12_r20_eta_definition import (
    TodaEtaFamilyGeneralDefinition,
    build_cited_eta_family_definition,
    expand_cited_eta_definition,
)
from phase165_r12_r21_eta_generator_chain import (
    _eta_pair,
    expand_cited_eta_generator,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    canonical_member,
    expand_cited_stable_family,
)
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    composite_generator_image_rule,
    expand_composite_generator_image,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import toda_eta_family_definition_statement

ROOT = Path(__file__).resolve().parents[2]
_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _eta(n: int) -> HomotopyElement:
    # Read the actual registered family instead of inventing a generator type.
    family, = (row for row in read_registered_stable_families()
               if row.family_id == 2)
    return HomotopyElement(
        name=family.name_at(n), dimension=n, source=n + family.stem,
        target=n, generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _epsilon(n: int) -> HomotopyElement:
    family, = (row for row in read_registered_stable_families()
               if row.family_id == 10)
    return HomotopyElement(
        name=family.name_at(n), dimension=n, source=n + family.stem,
        target=n, generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _image(n: int, stem: int, earlier, later) -> GeneratorImage:
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + stem, n),
            TodaPrimaryGroup(n + stem + 1, n + 1),
        ), earlier, later,
    )


def test_r10e9_unicode_eta_image_proposed_with_cited_premises():
    for n in (11, 12, 14, 15):
        goal = _image(n, 1, _eta(n), _eta(n + 1))
        suspension = GeneratorSuspension(goal.map, goal.source_generator, goal.target_generator)
        assert _eta_pair(suspension) is not None
        options = expand_cited_eta_generator(goal)
        assert len(options) == 1
        assert options[0].subgoals == (suspension,)
        assert expand_cited_eta_generator(suspension)


def test_r10e9_typed_alias_guards_refuse_forgery():
    goal = _image(11, 1, _eta(11), _eta(12))
    invalid_targets = (
        replace(goal.target_generator, name="eta_12"),
        replace(goal.target_generator, generator=GeneratorSymbol(family="ν", index=12)),
        replace(goal.target_generator, source=14),
        replace(goal.target_generator, target=13),
        replace(goal.target_generator, dimension=13),
    )
    for bad in invalid_targets:
        forged = replace(goal, target_generator=bad)
        suspension = GeneratorSuspension(forged.map, forged.source_generator, forged.target_generator)
        assert _eta_pair(suspension) is None
        assert expand_cited_eta_generator(forged) == ()
    forged_map = replace(goal, map=TodaSuspensionMap(
        TodaPrimaryGroup(13, 11), TodaPrimaryGroup(14, 12),
    ))
    assert expand_cited_eta_generator(forged_map) == ()


def test_r10e9_eta_image_replays_from_real_cited_general_definition():
    bridge = build_cited_eta_family_definition(ROOT / "sources" / "toda" / "Toda_05_2.tex")
    leaf, = (link.step for link in bridge.proof_links)
    assert leaf is not None and leaf.rule is ProofRule.GIVEN
    assert leaf.conclusion == TodaEtaFamilyGeneralDefinition()
    definitions = []
    for n in (11, 12):
        statement = toda_eta_family_definition_statement(n)
        option, = expand_cited_eta_definition(statement, (leaf.conclusion,))
        matches = find_inference_matches_for_rule(option.rule, (leaf,))
        assert len(matches) == 1
        step = apply_inference_match(matches[0])
        assert step.rule is ProofRule.INFERENCE and step.premises == (leaf,)
        definitions.append(step)
    goal = _image(11, 1, _eta(11), _eta(12))
    suspension_goal = GeneratorSuspension(goal.map, goal.source_generator, goal.target_generator)
    option, = expand_cited_eta_generator(suspension_goal)
    matches = find_inference_matches_for_rule(option.rule, tuple(definitions))
    assert len(matches) == 1
    suspension_step = apply_inference_match(matches[0])
    assert suspension_step.conclusion == suspension_goal
    assert suspension_step.rule is ProofRule.INFERENCE
    option, = expand_cited_eta_generator(goal)
    matches = find_inference_matches_for_rule(option.rule, (suspension_step,))
    assert len(matches) == 1
    image_step = apply_inference_match(matches[0])
    assert image_step.rule is ProofRule.INFERENCE
    assert image_step.conclusion == goal
    assert image_step.premises == (suspension_step,)


def test_r10e9_eta_epsilon_composite_uses_existing_two_factor_rule():
    source = CitedStableFamilyDefinition(10, 3, 8)
    for n in (11, 12, 14, 15):
        earlier = Composition(_eta(n), _epsilon(n + 1))
        later = Composition(_eta(n + 1), _epsilon(n + 2))
        goal = _image(n, 9, earlier, later)
        eta_image, epsilon_image = component_image_obligations(goal)
        assert eta_image == _image(n, 1, _eta(n), _eta(n + 1))
        assert epsilon_image == _image(n + 1, 8, _epsilon(n + 1), _epsilon(n + 2))
        assert len(expand_cited_eta_generator(eta_image)) == 1
        assert len(expand_cited_stable_family(epsilon_image, (source,))) == 1
        assert len(expand_composite_generator_image(goal)) == 1
        # Neither factor may be a free GIVEN; both independently require proof.
        rule = composite_generator_image_rule(goal)
        assert find_inference_matches_for_rule(rule, (
            ProofStep(eta_image, (), ProofRule.GIVEN),
            ProofStep(epsilon_image, (), ProofRule.INFERENCE),
        )) == ()


def test_r10e9_existing_canonical_eta_name_still_matches():
    first = toda_eta_family_definition_statement(11)
    second = toda_eta_family_definition_statement(12)
    goal = GeneratorSuspension(
        TodaSuspensionMap(TodaPrimaryGroup(12, 11), TodaPrimaryGroup(13, 12)),
        first.element, second.element,
    )
    assert _eta_pair(goal) == (first, second)


def test_r10e9_complete_guarded_replacement_requires_source_review():
    from phase169_r10e9_eta_composite_alias_fix.patch import (
        OLD_FUNCTION, NEW_FUNCTION, transform,
    )
    assert 'from phase165_r12_r28_presentation_connection import _matching_eta_name' in NEW_FUNCTION
    original = (ROOT / "phase165_r12_r21_eta_generator_chain.py").read_text(encoding="utf-8")
    assert NEW_FUNCTION in original
    assert OLD_FUNCTION not in original
    import pytest
    with pytest.raises(RuntimeError, match="eta function changed"):
        transform(original)
