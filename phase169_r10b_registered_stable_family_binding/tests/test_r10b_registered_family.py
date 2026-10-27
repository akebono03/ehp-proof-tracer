"""R10B: DB family identity is a typed candidate guard, not a proof axiom."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
    registered_family_of,
    registered_stable_family_pair,
)
from phase169_r7_general_stable_transport.rule import (
    _consecutive_generator_image_goals,
    _intermediate_typed_generator,
)
from proof import Relation, RelationType


_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def member(family, n: int) -> HomotopyElement:
    return HomotopyElement(
        name=family.display + str(n).translate(_SUB),
        dimension=n,
        source=n + family.stem,
        target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def test_r10b_all_registered_kinds_zero_identified_without_zero():
    families = read_registered_stable_families()
    assert len(families) == 39
    assert len({item.family_id for item in families}) == 39
    assert not any(item.family_id == 0 for item in families)
    assert {2, 4, 9}.issubset({item.family_id for item in families})
    for family in families:
        initial = member(family, family.minimum_n)
        assert registered_family_of(initial) == family
        assert registered_family_of(member(family, family.minimum_n + 3)) == family
        assert registered_family_of(member(family, family.minimum_n - 1)) is None


@pytest.mark.parametrize("family_id", [2, 4, 9, 10, 23, 103])
@pytest.mark.parametrize("r", [1, 2, 4])
def test_r10b_registered_family_arbitrary_steps(family_id, r):
    families = read_registered_stable_families()
    family = next(row for row in families if row.family_id == family_id)
    source = member(family, max(family.minimum_n, family.stem + 2))
    target = member(family, source.dimension + r)
    assert registered_stable_family_pair(source, target) == family
    for step in range(1, r):
        assert _intermediate_typed_generator(source, target, step, r) == member(
            family, source.dimension + step
        )


def test_r10b_rejects_spoofed_family_stem_and_minimum():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    source = member(nu, 5)
    target = member(nu, 7)
    assert registered_stable_family_pair(source, target) == nu
    wrong_stem = replace(target, source=target.source + 1)
    wrong_symbol = replace(target, generator=replace(target.generator, family="η"))
    wrong_decoration = replace(target, generator=replace(target.generator, decoration="′"))
    wrong_name = replace(target, name="ν₉")
    unknown = replace(target, generator=replace(target.generator, family="UNKNOWN"))
    for invalid in (wrong_stem, wrong_symbol, wrong_decoration, wrong_name, unknown):
        assert registered_stable_family_pair(source, invalid) is None
        assert _intermediate_typed_generator(source, invalid, 1, 2) is None
    assert registered_family_of(member(nu, 3)) is None


def test_r10b_single_suspension_also_requires_registered_identity():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    original = member(nu, 5)
    last = member(nu, 6)
    assert _intermediate_typed_generator(original, last, 0, 1) == original
    assert _intermediate_typed_generator(original, last, 1, 1) == last
    bad = replace(last, source=last.source + 1)
    assert _intermediate_typed_generator(original, bad, 0, 1) is None
    from proof import Relation, RelationType
    source_group = Relation(TodaPrimaryGroup(8, 5), FiniteCyclicGroup(8, original),
                            RelationType.EQUALITY)
    target_group = Relation(TodaPrimaryGroup(9, 6), FiniteCyclicGroup(8, bad),
                            RelationType.EQUALITY)
    assert _consecutive_generator_image_goals(source_group, target_group) is None


def test_r10b_unequal_registry_id_does_not_count_as_same_family():
    families = read_registered_stable_families()
    eta = next(row for row in families if row.family_id == 2)
    nu = next(row for row in families if row.family_id == 4)
    assert registered_stable_family_pair(member(eta, 4), member(nu, 6)) is None


def test_r10b_mixed_composition_preserves_typed_names():
    families = read_registered_stable_families()
    eta = next(row for row in families if row.family_id == 2)
    start = Composition(member(eta, 4), member(eta, 5))
    finish = Composition(member(eta, 7), member(eta, 8))
    middle = _intermediate_typed_generator(start, finish, 2, 3)
    assert middle == Composition(member(eta, 6), member(eta, 7))


def test_r10b_registered_names_never_generate_proof_steps():
    families = read_registered_stable_families()
    nu = next(row for row in families if row.family_id == 4)
    original = member(nu, 5)
    last = member(nu, 7)
    source = Relation(TodaPrimaryGroup(8, 5), FiniteCyclicGroup(8, original),
                      RelationType.EQUALITY)
    target = Relation(TodaPrimaryGroup(10, 7), FiniteCyclicGroup(8, last),
                      RelationType.EQUALITY)
    images = _consecutive_generator_image_goals(source, target)
    assert images is not None and len(images) == 2
    assert images[0].source_generator == original
    assert images[-1].target_generator == last
    assert all(type(image).__name__ == "GeneratorImage" for image in images)
    assert all(type(image).__name__ != "ProofStep" for image in images)
    too_early = Relation(TodaPrimaryGroup(7, 4), FiniteCyclicGroup(8, member(nu, 4)),
                         RelationType.EQUALITY)
    assert _consecutive_generator_image_goals(too_early, target) is None


def test_r10b_patch_only_complete_function_and_preserves_other_source():
    from phase169_r10b_registered_stable_family_binding.patch import (
        BACKUP, replacement_content, _function_range,
    )
    before = BACKUP.read_bytes()
    after, function = replacement_content(before)
    previous = before.decode("utf-8").replace("\r\n", "\n")
    changed = after.decode("utf-8").replace("\r\n", "\n")
    start, end = _function_range(previous)
    assert "registered_stable_family_pair" in function
    assert previous[:start] == changed[:start]
    assert previous[end:].strip() == changed[start + len(function):].strip()
    with pytest.raises(RuntimeError):
        replacement_content(after)
