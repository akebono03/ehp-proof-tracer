"""Positive and negative notation guard tests, plus actual DB correspondence."""
from __future__ import annotations

from dataclasses import replace

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r7_typed_nu_prime_notation import installer
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation


def observed_pair():
    signed = canonical_toda58()
    earlier = exact_prior_database_result(4, 3)
    assert isinstance(earlier.rhs, DirectSumGroup)
    part, = (x for x in earlier.rhs.summands if isinstance(x, FiniteCyclicGroup))
    return signed.positive_value.right.expression, part.generator


def test_actual_prior_and_source_are_same_strict_nu_prime_notation():
    left, right = observed_pair()
    assert left != right
    assert same_typed_generator_notation(left, right)
    assert same_typed_generator_notation(right, left)


def test_incompatible_dimensions_and_prime_or_family_rejected():
    left, right = observed_pair()
    assert not same_typed_generator_notation(left, replace(right, exponent=2))
    wrong_dim = replace(right.expression, source=right.expression.source + 1)
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_dim))
    wrong_family = replace(right.expression, generator=GeneratorSymbol("\\eta'"))
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_family))
    wrong_name = replace(right.expression, name="ν")
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_name))


def test_other_elements_are_not_identified_by_similar_suspension():
    left, right = observed_pair()
    other = HomotopyElement("ν", 3, 6, 3, GeneratorSymbol("ν"))
    assert not same_typed_generator_notation(Suspension(other), IteratedSuspension(other, 1))
    assert same_typed_generator_notation(right, right)
    assert not same_typed_generator_notation(left, IteratedSuspension(right.expression, 0))


def test_installer_is_idempotent_and_rejects_partial_patch():
    path = installer.TARGET
    # Validate against the actual checked-in R13R2 implementation.
    source = open(path, encoding="utf-8-sig").read()
    updated, needed = installer.render(source)
    if needed:
        assert installer.NEW_IMPORT in updated and installer.NEW_BODY in updated
        assert installer.render(updated) == (updated, False)
    else:
        assert installer.NEW_IMPORT in source and installer.NEW_BODY in source
    import pytest
    with pytest.raises(RuntimeError, match="PARTIAL"):
        installer.render(installer.NEW_IMPORT + installer.OLD_BODY)
