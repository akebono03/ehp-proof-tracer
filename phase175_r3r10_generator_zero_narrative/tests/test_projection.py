"""R3R10 shared projection tests: only verified typed content is verbalized."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, ProofStep


def _registered_zero_image() -> GeneratorImage:
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        prior.rhs.generator,
        Zero(),
    )


def test_registered_composite_generator_zero_is_visible() -> None:
    image = _registered_zero_image()
    step = ProofStep(image, (), ProofRule.INFERENCE)
    rendered = typed_sentence(image, step)
    assert rendered is not None
    assert rendered.startswith(r"$E(\eta_{2}")
    assert r"\nu'" in rendered
    assert r"\circ " in rendered
    assert rendered.endswith("=0$.")


def test_non_expression_zero_generator_does_not_get_invented_text() -> None:
    image = _registered_zero_image()
    malformed = GeneratorImage(image.map, "NOT_A_TYPED_EXPRESSION", Zero())
    step = ProofStep(malformed, (), ProofRule.INFERENCE)
    assert typed_sentence(malformed, step) is None


def test_nonzero_unsupported_generator_is_not_reinterpreted_as_zero() -> None:
    image = _registered_zero_image()
    changed = GeneratorImage(image.map, image.source_generator, "not-zero")
    step = ProofStep(changed, (), ProofRule.INFERENCE)
    assert typed_sentence(changed, step) is None
