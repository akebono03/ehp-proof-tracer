"""R12-R14 targeted integration with registered, citation-screened sources."""
from __future__ import annotations

import pytest
from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r14_kernel_closure import (
    KernelClosureResult, prove_kernel_in_screened_context, summarize_proof_ancestry,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r3_recursive_search import reconstruct_registered_goal
from proof import ProofRule, Relation, RelationType
from phase163_r4_registry_bridge import RegistryBridgeResult


def kernel_goal():
    eta = HomotopyElement("η₂", dimension=2, source=3, target=2,
                          generator=GeneratorSymbol("η", 2))
    return SuspensionKernelFreeCyclicStatement(
        TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3)),
        FreeCyclicGroup(Multiple(coefficient=2, expression=eta)),
    )


def test_r14_kernel_goal_has_no_target_group_result_as_premise():
    goal = kernel_goal()
    assert goal.map.target_group == TodaPrimaryGroup(4, 3)
    assert goal.kernel_group.generator.coefficient == 2
    assert not isinstance(goal, Relation)


def test_r14_no_cited_given_never_certifies_kernel():
    bridge = build_shared_typed_bridge()
    empty = RegistryBridgeResult(bridge.registry, bridge.records, ())
    target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    citing = next(iter(bridge.registry._assertions))
    result = prove_kernel_in_screened_context(kernel_goal(), empty,
                    citing_assertion_id=citing, proof_target=target)
    assert result.status != "CERTIFIED"
    assert result.proof is None


def test_r14_invalid_goal_type_rejected():
    bridge = build_shared_typed_bridge()
    target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    with pytest.raises(TypeError):
        prove_kernel_in_screened_context(target, bridge,
                citing_assertion_id=next(iter(bridge.registry._assertions)),
                proof_target=target)


def test_r14_actual_recursive_kernel_proof_closes_with_reference_ancestry():
    bridge = build_shared_typed_bridge()
    citing = next(iter(bridge.registry._assertions))
    target = Relation(TodaPrimaryGroup(4, 3), object(), relation_type=RelationType.EQUALITY)
    result = prove_kernel_in_screened_context(kernel_goal(), bridge,
                     citing_assertion_id=citing, proof_target=target)
    assert result.status == "CERTIFIED", f"Kernel proof open: {result.status}: {result.blocker}"
    assert result.proof is not None
    assert result.proof.rule is ProofRule.INFERENCE
    ancestry = summarize_proof_ancestry(result.proof)
    assert ancestry["inference"] >= 3
    assert ancestry["given"] >= 2
    assert ancestry["has_general_prop42_ancestor"]
