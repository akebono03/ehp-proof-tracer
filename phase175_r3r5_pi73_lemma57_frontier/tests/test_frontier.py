"""Verify the shape of the EHP-zero-image query in the real checkout."""
from __future__ import annotations

import pytest

pytest.importorskip("phase165_r52_r9_shared_math")

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaHopfInvariantMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import hopf_injectivity_from_zero_image_inputs
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import expand_zero_image_from_cyclic_generator


def test_pi73_hopf_injectivity_requires_precisely_pi62_suspension() -> None:
    hopf = TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5))
    inputs = hopf_injectivity_from_zero_image_inputs(MapInjective(hopf))
    assert inputs is not None
    zero_image, exactness = inputs
    assert zero_image == ImageZeroStatement(TodaSuspensionMap(
        TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3),
    ))
    assert exactness.window.middle_term == TodaPrimaryGroup(7, 3)


def test_generic_zero_image_uses_unproved_pi62_presentation_and_image() -> None:
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    goals = expand_zero_image_from_cyclic_generator(ImageZeroStatement(e), prior)
    assert len(goals) == 1
    assert goals[0].subgoals == (
        prior, GeneratorImage(e, prior.rhs.generator, Zero()),
    )
    assert all(not hasattr(item, "premises") for item in goals[0].subgoals)
