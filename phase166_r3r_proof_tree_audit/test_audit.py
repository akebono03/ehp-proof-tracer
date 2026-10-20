from dataclasses import dataclass

from proof import InferenceRule, ProofRule, ProofStep, Relation
from phase165_r14_r6_generic_iso import GeneratorImage
from audit import ancestors, audit_relation_steps


@dataclass(frozen=True)
class StubAssertion:
    reference_id: str


@dataclass(frozen=True)
class StubReference:
    locator: str


@dataclass(frozen=True)
class StubLink:
    step: ProofStep
    assertion_id: str


class StubRegistry:
    def assertion(self, assertion_id: str) -> StubAssertion:
        return StubAssertion("prop51")

    def reference(self, reference_id: str) -> StubReference:
        return StubReference("Proposition 5.1")


@dataclass(frozen=True)
class StubBridge:
    proof_links: tuple[StubLink, ...]
    registry: StubRegistry


def test_r3r_accepts_actual_inference_ancestry():
    given = ProofStep(GeneratorImage("H", "eta2", "iota3"), (), ProofRule.GIVEN)
    derived = ProofStep(Relation("H(eta2)", "iota3"), (given,), ProofRule.INFERENCE,
                        inference_rule=InferenceRule("generator image to relation"))
    bridge = StubBridge((StubLink(given, "prop51_image"),), StubRegistry())
    result = audit_relation_steps((derived,), bridge)
    assert result["derived_image_relation_chain_verified"] is True
    assert result["relations_with_image_ancestor"] == 1


def test_r3r_rejects_independent_given_relation():
    given = ProofStep(GeneratorImage("H", "eta2", "iota3"), (), ProofRule.GIVEN)
    unrelated = ProofStep(Relation("H(eta2)", "iota3"), (), ProofRule.GIVEN)
    bridge = StubBridge((StubLink(given, "prop51_image"),), StubRegistry())
    result = audit_relation_steps((unrelated,), bridge)
    assert result["derived_image_relation_chain_verified"] is False
    assert result["relation_evidence"][0]["independent_given_relation"] is True


def test_r3r_rejects_missing_registered_ancestor():
    given = ProofStep(GeneratorImage("H", "eta2", "iota3"), (), ProofRule.GIVEN)
    derived = ProofStep(Relation("H(eta2)", "iota3"), (given,), ProofRule.INFERENCE)
    bridge = StubBridge((), StubRegistry())
    result = audit_relation_steps((derived,), bridge)
    assert result["derived_image_relation_chain_verified"] is False


def test_r3r_detects_nested_ancestry():
    given = ProofStep("source", (), ProofRule.GIVEN)
    intermediate = ProofStep("intermediate", (given,), ProofRule.INFERENCE)
    result = ancestors(intermediate)
    assert result == (given, intermediate)
