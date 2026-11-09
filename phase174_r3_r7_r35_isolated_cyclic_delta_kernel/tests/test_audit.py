"""R35 integration observations, without modifying the shared provider."""
from __future__ import annotations

from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit import (
    inspect_isolated_frontier, verify_checkout,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    checked_prior_statements,
)
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    expand_cyclic_delta_kernel,
)
from phase165_r12_r2_quotient_rules import KernelMultipleStatement


def test_source_guard_keeps_reviewed_r34():
    assert verify_checkout()["source_guard"] == "PASS"


def test_real_r34_composition_is_not_replaced_with_synthetic_generator():
    codomain, image = checked_prior_statements()
    goal = KernelMultipleStatement(image.map, image.map.source_group, image.element, 2)
    proposals = expand_cyclic_delta_kernel(goal, (codomain, image))
    assert len(proposals) == 1
    assert proposals[0].subgoals[1:] == (codomain, image)


def test_real_shared_screen_preserves_unproved_frontier():
    result = inspect_isolated_frontier()
    assert result["screened_cited_codomain"] == 1
    assert result["screened_cited_signed_image"] == 1
    assert result["isolated_kernel_expansions"] == 1
    assert result["composite_generator_preserved"] is True
    assert result["kernel_proof_certified_by_audit"] is False
    assert result["shared_provider_connected_in_r35"] is False
    assert result["root_complete"] is False
