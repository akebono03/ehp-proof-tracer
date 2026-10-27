"""R10D2: shared inference and source checks, not family-specific rules."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    _image_members,
    build_cited_stable_family_definitions,
    canonical_member,
    cited_family_reference_sentence,
    expand_cited_stable_family,
    verified_source_positions,
)
from proof import (
    ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule,
)


def _source(family_id: int) -> CitedStableFamilyDefinition:
    family, = (item for item in read_registered_stable_families()
               if item.family_id == family_id)
    return CitedStableFamilyDefinition(family.family_id, family.minimum_n, family.stem)


def _image(family_id: int, n: int) -> GeneratorImage:
    source = _source(family_id)
    earlier = canonical_member(source, n)
    later = canonical_member(source, n + 1)
    assert earlier is not None and later is not None
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + source.stem, n),
            TodaPrimaryGroup(n + source.stem + 1, n + 1),
        ),
        earlier.element, later.element,
    )


def test_r10d2_source_positions_verified_without_new_mathematical_rules():
    assert dict(verified_source_positions()) == {4: 8550, 9: 10450}
    bridge = build_cited_stable_family_definitions()
    assert len(bridge.registry._assertions) == 2
    assert len(bridge.proof_links) == 2
    for link in bridge.proof_links:
        assert link.step is not None
        assert link.step.rule is ProofRule.GIVEN
        assert not link.step.premises
        assert isinstance(link.step.conclusion, CitedStableFamilyDefinition)


@pytest.mark.parametrize("family_id,first_dimension", [(4, 4), (9, 8)])
def test_r10d2_citation_to_concrete_definition_to_image_is_real_inference(
    family_id, first_dimension,
):
    source = _source(family_id)
    bridge = build_cited_stable_family_definitions()
    cited, = (link.step for link in bridge.proof_links
              if link.step is not None and link.step.conclusion == source)
    definitions = []
    for n in (first_dimension, first_dimension + 1):
        candidate = canonical_member(source, n)
        assert isinstance(candidate, StableFamilyMemberDefinition)
        options = expand_cited_stable_family(candidate, (source,))
        assert len(options) == 1
        assert options[0].subgoals == (source,)
        matches = find_inference_matches_for_rule(options[0].rule, (cited,))
        assert len(matches) == 1
        derived = apply_inference_match(matches[0])
        assert derived.rule is ProofRule.INFERENCE
        assert derived.premises == (cited,)
        definitions.append(derived)
    image = _image(family_id, first_dimension)
    options = expand_cited_stable_family(image, (source,))
    assert len(options) == 1
    assert options[0].subgoals == tuple(step.conclusion for step in definitions)
    matches = find_inference_matches_for_rule(options[0].rule, tuple(definitions))
    assert len(matches) == 1
    derived_image = apply_inference_match(matches[0])
    assert derived_image.conclusion == image
    assert derived_image.rule is ProofRule.INFERENCE
    assert len(derived_image.premises) == 2


@pytest.mark.parametrize("family_id,n", [(4, 5), (4, 8), (9, 9), (9, 12)])
def test_r10d2_one_general_image_engine_across_stems_and_indices(family_id, n):
    source = _source(family_id)
    goal = _image(family_id, n)
    assert _image_members(goal) is not None
    assert len(expand_cited_stable_family(goal, (source,))) == 1
    assert len(expand_cited_stable_family(goal, ())) == 0


def test_r10d2_wrong_dimension_source_and_unrelated_family_fail_closed():
    nu = _source(4)
    sigma = _source(9)
    nu_image = _image(4, 5)
    assert expand_cited_stable_family(nu_image, (sigma,)) == ()
    wrong_map = replace(nu_image, map=replace(
        nu_image.map,
        target_group=TodaPrimaryGroup(11, 7),
    ))
    assert _image_members(wrong_map) is None
    assert expand_cited_stable_family(wrong_map, (nu,)) == ()
    assert canonical_member(nu, 3) is None
    assert canonical_member(sigma, 7) is None


def test_r10d2_a_db_family_without_citation_is_not_auto_provable():
    mu_family, = (item for item in read_registered_stable_families()
                  if item.family_id == 103)
    fake_source = CitedStableFamilyDefinition(mu_family.family_id,
                                               mu_family.minimum_n,
                                               mu_family.stem)
    assert canonical_member(fake_source, mu_family.minimum_n) is None
    assert expand_cited_stable_family(fake_source, (fake_source,)) == ()


def test_r10d2_an_unverified_instance_and_given_image_do_not_satisfy_rule():
    source = _source(4)
    image = _image(4, 5)
    options = expand_cited_stable_family(image, (source,))
    assert len(options) == 1
    first, second = options[0].subgoals
    unproved = (ProofStep(first, (), ProofRule.GIVEN),
                ProofStep(second, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(options[0].rule, unproved) == ()
    wrong = (ProofStep(first, (), ProofRule.INFERENCE),
             ProofStep(replace(second, index=8), (), ProofRule.INFERENCE))
    assert find_inference_matches_for_rule(options[0].rule, wrong) == ()


def test_r10d2_common_reference_not_series_specific_renderer():
    assert (cited_family_reference_sentence(_source(4))
            == r"$n\ge 4$ に対し, $\nu_n=E^{n-4}\nu_{4}$ と定義する.")
    assert (cited_family_reference_sentence(_source(9))
            == r"$n\ge 8$ に対し, $\sigma_n=E^{n-8}\sigma_{8}$ と定義する.")
    assert cited_family_reference_sentence(object()) is None
