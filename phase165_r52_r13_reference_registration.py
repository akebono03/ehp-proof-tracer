"""R52-R13: explicitly register an adopted, typed composite literature claim.

The caller, not a legacy ProofStep, supplies the typed content and citation.
This is source adoption, not independent verification of the original edition.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def register_adopted_composite_reference(
    *, assertion_id: str, locator: str, source_id: str,
    content: object, reference_kind: ReferenceKind = ReferenceKind.PROPOSITION,
    clause_ranges: tuple[tuple[str, str, int], ...] = (),
) -> RegistryBridgeResult:
    """Register a caller-adopted typed composite, preserving its original citation.

    Source adoption is an explicit input; it cannot be inferred from a prior
    ProofStep, the presence of a TeX token, or a SOURCE_ARCHIVE record.
    """
    if not isinstance(assertion_id, str) or not assertion_id:
        raise ValueError("assertion_id is required")
    if not isinstance(locator, str) or not locator:
        raise ValueError("locator is required")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("source_id is required")
    if not isinstance(reference_kind, ReferenceKind):
        raise TypeError("reference_kind must be ReferenceKind")
    if not is_dataclass(content) or isinstance(content, type):
        raise TypeError("typed composite dataclass instance required")
    parts = fields(content)
    if len(parts) < 2 or any(getattr(content, part.name) is None for part in parts):
        raise ValueError("composite requires at least two nonempty typed parts")
    registry = UnifiedStatementRegistry()
    reference_id = "adopted:" + assertion_id
    registry.add_reference(LiteratureEntry(
        reference_id=reference_id, kind=reference_kind,
        locator=locator, source_id=source_id,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=assertion_id, reference_id=reference_id,
        kind=AssertionKind.STATEMENT, content=content,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("typed_composite_fields", tuple(part.name for part in parts))
        + (("clause_ranges", clause_ranges),) if clause_ranges else
        ("typed_composite_fields", tuple(part.name for part in parts)),
    ))
    step = ProofStep(
        conclusion=content, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Adopted literature " + locator,
            literature_reference=LiteratureReference(
                label="Toda " + locator, locator=locator,
            ),
        ),
    )
    return RegistryBridgeResult(
        registry, (), (ProofStepLink(assertion_id=assertion_id, step=step),),
    )


def registered_prop51_items():
    """List all five proposition positions; position four remains an unproved GOAL."""
    from phase165_prop51_claim_order import ordered_prop51_items
    bridge = build_adopted_prop51_reference()
    content = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional").content
    return ordered_prop51_items(content)


def build_adopted_prop51_reference() -> RegistryBridgeResult:
    """Adopt the four already-typed clauses of Toda Proposition 5.1.

    Phase 55 provides typed values, *not* citation permission or a proof leaf.
    The adoption records the user-accepted Toda translated source; this does
    not claim original edition / independent mathematical verification.
    """
    from expression import (
        GeneratorSymbol, HomotopyElement, MapApplication, Multiple,
        ScalarSum, ScalarSymbol,
    )
    from homotopy_groups import (
        FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
    )
    from map_facts import EHP_H_MAP
    from proof import Relation, RelationType
    from toda_rules import (
        TodaDeltaImageUpToSignStatement,
        TodaProp51FiniteDimensionalStatement,
    )

    n = ScalarSymbol(name="n")
    eta2 = HomotopyElement(
        name="η₂", dimension=2, source=3, target=2,
        generator=GeneratorSymbol(family="η", index=2),
    )
    iota3 = HomotopyElement(
        name="ι_3", dimension=3,
        generator=GeneratorSymbol(family="ι", index=3),
    )
    iota5 = HomotopyElement(
        name="ι_5", dimension=5,
        generator=GeneratorSymbol(family="ι", index=5),
    )
    etan = HomotopyElement(
        name="η_n", dimension=n, source=ScalarSum(left=n, right=1),
        target=n, generator=GeneratorSymbol(family="η", index=n),
    )
    pi32 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi55 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    content = TodaProp51FiniteDimensionalStatement(
        pi3_2_group_relation=Relation(
            lhs=pi32, rhs=FreeCyclicGroup(generator=eta2),
            relation_type=RelationType.EQUALITY,
        ),
        eta2_hopf_relation=Relation(
            lhs=MapApplication(map=EHP_H_MAP, expression=eta2),
            rhs=iota3, relation_type=RelationType.EQUALITY,
        ),
        delta_iota5_relation=TodaDeltaImageUpToSignStatement(
            map=TodaDeltaMap(source_group=pi55, target_group=pi32),
            element=iota5,
            positive_value=Multiple(coefficient=2, expression=eta2),
        ),
        higher_eta_group_relation=Relation(
            lhs=TodaPrimaryGroup(
                group_dimension=ScalarSum(left=n, right=1), sphere_dimension=n,
            ),
            rhs=FiniteCyclicGroup(order=2, generator=etan),
            relation_type=RelationType.EQUALITY,
        ),
    )
    if {f.name for f in fields(content)} != {
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    }:
        raise ValueError("Proposition 5.1 clauses changed")
    bridge = register_adopted_composite_reference(
        assertion_id="toda:adopted:prop5.1:finite_dimensional",
        locator="Proposition 5.1",
        source_id="Toda translated TeX:Proposition 5.1 (user-adopted; original edition unverified)",
        content=content,
        clause_ranges=(("higher_eta_group_relation", "n", 4),),
    )
    # This literature assertion has no GIVEN proof link: no self-proof.
    from phase165_prop51_claim_order import pi4_3_goal
    bridge.registry.add_assertion(AssertionEntry(
        assertion_id="toda:adopted:prop5.1:pi4_3",
        reference_id="adopted:toda:adopted:prop5.1:finite_dimensional",
        kind=AssertionKind.STATEMENT,
        content=pi4_3_goal(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=4,
        scope=("user_adopted_claim_without_given_proof",),
    ))
    # Phase 166 R3-I: expose the five individual clauses in proof-use order.
    # The composite remains for existing callers; the canonical source claims
    # are these component assertions. ProofStepLinks are generated by the
    # uniform statement-order gate, never by this registration method.
    for position, component_key, clause in (
        (1, "eta2_hopf_relation", content.eta2_hopf_relation),
        (2, "pi3_2_group_relation", content.pi3_2_group_relation),
        (3, "delta_iota5_relation", content.delta_iota5_relation),
        (5, "higher_eta_group_relation", content.higher_eta_group_relation),
    ):
        bridge.registry.add_assertion(AssertionEntry(
            assertion_id="toda:adopted:prop5.1:" + component_key,
            reference_id="adopted:toda:adopted:prop5.1:finite_dimensional",
            kind=AssertionKind.STATEMENT,
            content=clause,
            origin=AssertionOrigin.FIXED_STATEMENT,
            component_position=position,
        ))
    return bridge
