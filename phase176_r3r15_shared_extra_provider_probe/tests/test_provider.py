"""Focused source guard and typed source-free right composition contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase176_r3r15_shared_extra_provider_probe.provider import build_screened_extra_provider
from proof import ProofRule, ProofStep


def _fixture_goal():
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        Composition(a, Composition(b, c)), Zero(),
    )


def test_screened_source_is_required():
    with pytest.raises(ValueError, match="ONE_SCREENED_SOURCE_REQUIRED"):
        build_screened_extra_provider(())


def test_spoofed_source_is_rejected():
    spoof = ProofStep("not citation", (), ProofRule.GIVEN)
    with pytest.raises(ValueError, match="SCREENED_SOURCE_STEP_INVALID"):
        build_screened_extra_provider((spoof,))


def test_inference_pretending_to_be_source_is_rejected():
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    step = ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.INFERENCE)
    with pytest.raises(ValueError, match="SCREENED_SOURCE_STEP_INVALID"):
        build_screened_extra_provider((step,))


def test_missing_citation_metadata_is_rejected():
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    step = ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.GIVEN)
    with pytest.raises(ValueError, match="LEMMA57_CITATION_REQUIRED"):
        build_screened_extra_provider((step,))


def test_goal_type_is_well_formed():
    goal = _fixture_goal()
    from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
    from phase176_r3r10_right_zero_transport_isolated.rule import right_zero_transport_inputs
    base = preceding_zero_image(goal)
    assert base is not None
    assert right_zero_transport_inputs(goal, base) == (base,)
    assert preceding_zero_image(replace(goal, target_generator=goal.source_generator)) is None
