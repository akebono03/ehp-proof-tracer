from __future__ import annotations

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import SurjectiveMapStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r16_bridges import (
    concrete_cyclic_kernel_as_multiple_rule,
    derive_from_certified_proof,
    suspension_surjectivity_as_generic_surjectivity_rule,
)
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r14_r6_generic_iso import MapSurjective
from proof import ProofRule, ProofStep


def test_generic_surjectivity_conversion_preserves_proof_ancestry():
    f = TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))
    source = ProofStep(MapSurjective(f), (), ProofRule.GIVEN)
    result = derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), source)
    assert result.conclusion == SurjectiveMapStatement(f)
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (source,)


def test_generic_kernel_conversion_preserves_generator_and_ancestry():
    f = TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))
    eta2 = HomotopyElement("η₂", dimension=2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    source = ProofStep(SuspensionKernelFreeCyclicStatement(
        f, FreeCyclicGroup(Multiple(coefficient=2, expression=eta2)),
    ), (), ProofRule.GIVEN)
    result = derive_from_certified_proof(concrete_cyclic_kernel_as_multiple_rule(), source)
    assert result.conclusion == KernelMultipleStatement(f, f.source_group, eta2, 2)
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (source,)


def test_unproved_goal_is_never_promoted_to_proof():
    with pytest.raises(TypeError):
        derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), MapSurjective(object()))
