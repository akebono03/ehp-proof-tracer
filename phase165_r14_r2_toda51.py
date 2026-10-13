"""R14-R2: generic typed mathematical clauses for Toda (5.1).

This module does not certify the original text, create a ProofStep, or mark a
source assertion proof-eligible. It constructs exact, checkable goal shapes.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType


@dataclass(frozen=True)
class Toda51Clause:
    name: str
    bound_variable: str
    minimum: int
    strict: bool
    source_locator: str = "(5.1)"
    proof_eligible: bool = False

    def __post_init__(self) -> None:
        if self.name not in ("sphere_one_zero", "diagonal_infinite_cyclic"):
            raise ValueError("unknown (5.1) clause")
        if self.bound_variable != ("i" if self.name == "sphere_one_zero" else "n"):
            raise ValueError("bound variable mismatch")
        if type(self.minimum) is not int or self.minimum != 1:
            raise ValueError("unexpected variable lower bound")
        if self.strict != (self.name == "sphere_one_zero"):
            raise ValueError("strictness mismatch")
        if self.proof_eligible is not False:
            raise ValueError("unverified clause cannot be promoted")


TODA_51_SCHEMAS = (
    Toda51Clause("sphere_one_zero", "i", 1, True),
    Toda51Clause("diagonal_infinite_cyclic", "n", 1, False),
)


def instantiate_toda51_clause(clause: Toda51Clause, index: int) -> Relation:
    """Instantiate the statement only within its quantified range.

    The returned Relation is a typed *claim*, not a derivation or ProofStep.
    """
    if clause not in TODA_51_SCHEMAS:
        raise ValueError("unrecognized source clause")
    if type(index) is not int or index < clause.minimum or (clause.strict and index == clause.minimum):
        raise ValueError("index is outside Toda (5.1) range")
    if clause.name == "sphere_one_zero":
        return Relation(
            lhs=TodaPrimaryGroup(group_dimension=index, sphere_dimension=1),
            rhs=0,
            relation_type=RelationType.EQUALITY,
        )
    iota = HomotopyElement(
        name=f"ι_{index}",
        dimension=index,
        source=index,
        target=index,
        generator=GeneratorSymbol(family="ι", index=index),
    )
    return Relation(
        lhs=TodaPrimaryGroup(group_dimension=index, sphere_dimension=index),
        rhs=FreeCyclicGroup(generator=iota),
        relation_type=RelationType.EQUALITY,
    )


def report_toda51_source(bridge: object) -> dict:
    """Discover matching source locators without granting citation permission."""
    assertions = bridge.registry._assertions.values()
    matches = []
    for assertion in assertions:
        if not assertion.assertion_id.startswith("phase163:archive:"):
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.locator.strip() in ("(5.1)", "Equation (5.1)"):
            matches.append({
                "assertion_id": assertion.assertion_id,
                "reference_id": assertion.reference_id,
                "locator": reference.locator,
                "source_text": assertion.content["source_text"],
            })
    return {
        "source_locator": "(5.1)",
        "source_matches": matches,
        "mathematical_claim_schemas": 2,
        "source_semantics_certified": False,
        "newly_proof_eligible": 0,
        "proof_steps_created": 0,
        "status": "CLAUSES_TYPED_SOURCE_AND_PROOF_ELIGIBILITY_UNVERIFIED",
    }
