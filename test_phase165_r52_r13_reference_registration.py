"""R52-R13 targeted tests; full pytest belongs at the end of Phase 165."""
from dataclasses import dataclass

import pytest

from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import (
    build_adopted_prop51_reference,
    register_adopted_composite_reference,
)
from phase165_r3_recursive_search import _typed_reference_steps
from proof import ProofRule


@dataclass(frozen=True)
class CompositeFact:
    first: int
    second: str


def test_r13_generic_composite_registration_and_proof_lookup():
    base = register_adopted_composite_reference(
        assertion_id="sample", locator="Lemma X", source_id="approved source",
        content=CompositeFact(3, "proof"),
    )
    bridge = expand_cited_given_components(base)
    assert len(bridge.proof_links) == 3
    assert len(_typed_reference_steps(bridge, 3)) == 1
    assert len(_typed_reference_steps(bridge, "proof")) == 1
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)


def test_r13_rejects_untyped_and_missing_source():
    with pytest.raises(ValueError):
        register_adopted_composite_reference(
            assertion_id="x", locator="Lemma X", source_id="",
            content=CompositeFact(1, "a"),
        )
    with pytest.raises(TypeError):
        register_adopted_composite_reference(
            assertion_id="x", locator="Lemma X", source_id="approved",
            content="plain untyped source",
        )


def test_r13_prop51_four_components_have_direct_typed_given_links():
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    assert len(bridge.proof_links) == 5
    parent = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional")
    for name in (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ):
        clause = getattr(parent.content, name)
        found = _typed_reference_steps(bridge, clause)
        assert len(found) == 1
        assert found[0].rule is ProofRule.GIVEN
        assert found[0].inference_rule.literature_reference.locator == "Proposition 5.1"


def test_r13_shared_bridge_discovers_prop51_any_target():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    bridge = build_shared_typed_bridge(sources=(build_adopted_prop51_reference(),))
    assert len(bridge.proof_links) == 5
    clauses = build_adopted_prop51_reference().registry._assertions
    original = next(iter(clauses.values())).content
    assert len(_typed_reference_steps(bridge, original.pi3_2_group_relation)) == 1
    assert len(_typed_reference_steps(bridge, original.delta_iota5_relation)) == 1
