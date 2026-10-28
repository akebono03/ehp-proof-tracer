"""Focused real-library tests of the common stable representative convention."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import (
    Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple, Sum,
)
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10eq_r1_universal_stable_definition.definition import (
    expand_defined_stable_element_image,
    is_defined_stable_image,
    is_defined_stable_suspension,
    typed_element_span,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule


_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def member(family, n):
    return HomotopyElement(
        family.display + str(n).translate(_SUB), n,
        n + family.stem, n,
        GeneratorSymbol(family.symbol_family, n),
    )


def image(source, target):
    q, n = typed_element_span(source)
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(q, n), TodaPrimaryGroup(q + 1, n + 1)),
        source, target,
    )


def inferred(goal):
    option, = expand_defined_stable_element_image(goal)
    assert option.subgoals == ()
    matches = find_inference_matches_for_rule(option.rule, ())
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE and step.premises == ()
    assert step.conclusion == goal
    return step


def test_r10eq_all_39_registered_indexed_representatives():
    rows = read_registered_stable_families()
    assert len(rows) == 39
    for row in rows:
        n = max(row.minimum_n, row.stem + 2, 2)
        a, b = member(row, n), member(row, n + 1)
        assert is_defined_stable_suspension(a, b)
        inferred(image(a, b))


def test_r10eq_arbitrary_formal_stable_element_without_csv():
    x = HomotopyElement("x", 16, 30, 16)
    e1 = IteratedSuspension(x, 1)
    e2 = IteratedSuspension(x, 2)
    assert typed_element_span(x) == (30, 16)
    inferred(image(x, e1))
    inferred(image(e1, e2))


def test_r10eq_registered_14_stem_composition_sum_multiple():
    rows = {row.family_id: row for row in read_registered_stable_families()}
    a = member(rows[9], 16)
    b = member(rows[9], 23)
    ap = member(rows[9], 17)
    bp = member(rows[9], 24)
    first = Composition(a, b)
    second = Composition(ap, bp)
    assert typed_element_span(first) == (30, 16)
    assert is_defined_stable_suspension(first, second)
    inferred(image(first, second))
    k = member(rows[23], 16)
    kp = member(rows[23], 17)
    inferred(image(Sum(first, k), Sum(second, kp)))
    inferred(image(Multiple(3, k), Multiple(3, kp)))


def test_r10eq_reject_unrelated_or_wrong_stem():
    rows = {row.family_id: row for row in read_registered_stable_families()}
    k = member(rows[23], 16)
    kp = member(rows[23], 17)
    wrong = replace(kp, generator=replace(kp.generator, family="unknown"))
    for candidate in (wrong, replace(kp, name="not_kappa"),
                      replace(kp, source=kp.source + 1),
                      replace(kp, generator=replace(kp.generator, decoration="′"))):
        assert not is_defined_stable_image(image(k, candidate))
        assert expand_defined_stable_element_image(image(k, candidate)) == ()
    assert not is_defined_stable_suspension(k, member(rows[9], 17))


def test_r10eq_reject_outside_stable_range_and_malformed_maps():
    rows = {row.family_id: row for row in read_registered_stable_families()}
    k, kp = member(rows[23], 15), member(rows[23], 16)
    assert not is_defined_stable_suspension(k, kp)
    assert expand_defined_stable_element_image(image(k, kp)) == ()
    valid = image(member(rows[23], 16), member(rows[23], 17))
    bad_map = replace(valid, map=TodaSuspensionMap(
        TodaPrimaryGroup(30, 16), TodaPrimaryGroup(32, 18),
    ))
    assert not is_defined_stable_image(bad_map)
    assert expand_defined_stable_element_image(bad_map) == ()


def test_r10eq_reject_forged_expressions_and_bool_coefficients():
    x = HomotopyElement("x", 16, 30, 16)
    assert not is_defined_stable_suspension(x, IteratedSuspension(x, -1))
    assert not is_defined_stable_suspension(x, IteratedSuspension(x, True))
    assert typed_element_span(Multiple(True, x)) is None
    bad = HomotopyElement("broken", 17, 30, 16)
    assert typed_element_span(bad) is None
    assert typed_element_span(Sum(x, bad)) is None
    assert typed_element_span(Composition(x, x)) is None


def test_r10eq_rule_replay_guard_rejects_forged_premise():
    rows = {row.family_id: row for row in read_registered_stable_families()}
    a, b = member(rows[23], 16), member(rows[23], 17)
    goal = image(a, b)
    option, = expand_defined_stable_element_image(goal)
    forged = (inferred(goal),)
    assert find_inference_matches_for_rule(option.rule, forged) == (
        find_inference_matches_for_rule(option.rule, ())[0],
    )


def test_r10eq_guarded_function_replacement():
    from phase169_r10eq_r1_universal_stable_definition.patch import (
        OLD, NEW, full_function_span, replacement_content,
    )
    source = (
        "import os\n\ndef shared_expansion_provider(a):\n"
        + OLD
        + "    return a\n\ndef following_function():\n    return 1\n"
    )
    updated, complete = replacement_content(source.encode("utf-8"))
    assert NEW in complete and OLD not in complete
    assert b"def following_function():" in updated
    assert b"import os" in updated
    assert "def shared_expansion_provider" in complete
    with pytest.raises(RuntimeError):
        replacement_content(updated)
    assert full_function_span(source)[0] == source.index("def shared_expansion_provider")
