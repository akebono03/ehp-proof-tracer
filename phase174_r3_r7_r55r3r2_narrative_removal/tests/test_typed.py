"""Render typed conclusions generically; no selected Group-query target."""
from __future__ import annotations

import pytest


@pytest.mark.parametrize('n', [4, 6, 8])
def test_even_n_prop27_typed_statement_latex(n: int) -> None:
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization

    sentence = typed_sentence(typed_specialization(n), None)
    assert sentence is not None
    assert rf'\iota_{{{2 * n + 1}}}' in sentence
    assert rf'\iota_{{{2 * n - 1}}}' in sentence
    assert r'\pm2' in sentence
    assert r'\mathrm{upper}' not in sentence
    assert r'\mathrm{lower}' not in sentence


@pytest.mark.parametrize('n', [6, 8])
def test_kernel_multiple_statement_is_formatted_from_its_own_type(n: int) -> None:
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        upper_delta_surjectivity_inputs,
    )
    from phase168_r3_27_typed_statement_projection import typed_sentence

    mapping = TodaDeltaMap(TodaPrimaryGroup(2*n+1, 2*n+1),
                           TodaPrimaryGroup(2*n-1, n))
    required = upper_delta_surjectivity_inputs(MapSurjective(mapping))
    assert required is not None
    kernel = required[2]
    display = typed_sentence(kernel, None)
    assert display is not None
    assert r'\ker(' in display
    assert r'\mathbb{Z}' in display
    assert r'\mathrm{upper}' not in display
    assert r'\mathrm{lower}' not in display


def test_general_zero_relation_is_not_target_specific() -> None:
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    source = CitedFamilyAnnihilator(
        left_family_id=4, right_family_id=2,
        minimum_left_index=6, right_index_offset=3,
        citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
    )
    for n in (6, 8):
        relation = canonical_annihilator_instance(source, n)
        assert relation is not None
        sentence = typed_sentence(relation, None)
        assert sentence is not None
        assert r'\nu' in sentence and r'\eta' in sentence
        assert '0' in sentence
