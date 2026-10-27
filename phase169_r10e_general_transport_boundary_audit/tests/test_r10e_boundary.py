"""R10E0 limited shape and range checks, without manufacturing ProofSteps."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from phase169_r10e_general_transport_boundary_audit.audit import group_shape
from phase169_r7_general_stable_transport.rule import (
    _consecutive_generator_image_goals,
)
from proof import Relation, RelationType


def _element(family: str, n: int, stem: int) -> HomotopyElement:
    return HomotopyElement(
        name=family + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")),
        dimension=n, source=n + stem, target=n,
        generator=GeneratorSymbol(family=family, index=n),
    )


def _group(n: int, k: int, structure: object) -> Relation:
    return Relation(
        TodaPrimaryGroup(n + k, n), structure, RelationType.EQUALITY,
    )


def test_r10e0_classifies_zero_goal_without_cyclic_transport():
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 8))
    assert group_shape(zero) == "zero_group"


def test_r10e0_classifies_single_finite_cyclic_group():
    goal = _group(15, 7, FiniteCyclicGroup(16, _element("σ", 15, 7)))
    assert group_shape(goal) == "finite_cyclic"


def test_r10e0_classifies_direct_sum_independently_from_components():
    goal = _group(15, 8, DirectSumGroup((
        FiniteCyclicGroup(2, _element("ε", 15, 8)),
        FiniteCyclicGroup(2, _element("μ", 15, 8)),
    )))
    assert group_shape(goal) == "direct_sum"


def test_r10e0_classifies_free_cyclic_group_without_guessing_order():
    goal = _group(4, 3, FreeCyclicGroup(_element("ν", 4, 3)))
    assert group_shape(goal) == "free_cyclic"


def test_r10e0_stable_start_rejects_lower_source_even_if_types_match():
    source = _group(8, 7, FiniteCyclicGroup(16, _element("σ", 8, 7)))
    goal = _group(9, 7, FiniteCyclicGroup(16, _element("σ", 9, 7)))
    assert _consecutive_generator_image_goals(source, goal) is None


def test_r10e0_stable_sigma_can_form_goals_without_claiming_proof():
    source = _group(9, 7, FiniteCyclicGroup(16, _element("σ", 9, 7)))
    goal = _group(10, 7, FiniteCyclicGroup(16, _element("σ", 10, 7)))
    images = _consecutive_generator_image_goals(source, goal)
    assert images is not None and len(images) == 1
    assert all(type(x).__name__ == "GeneratorImage" for x in images)
    assert all(type(x).__name__ != "ProofStep" for x in images)
