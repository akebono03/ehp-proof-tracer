"""R14-R4: remaining Toda (5.1) schema types; no theorem certification."""
from __future__ import annotations
from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from proof import Relation, RelationType
from phase165_r14_r3_source_scope import CLAUSES

@dataclass(frozen=True)
class StableStem:
    index: int
    prime: int | None = None

    def __post_init__(self):
        if type(self.index) is not int:
            raise TypeError("stable stem index must be an integer")
        if self.prime is not None and self.prime != 2:
            raise ValueError("only the cited 2-primary component is encoded")

@dataclass(frozen=True)
class StableIdentity:
    """Symbolic E-infinity identity; not an evaluated suspension map."""
    stable_generator: str
    suspension_source: str
    source_dimension: int

    def __post_init__(self):
        if type(self.source_dimension) is not int or self.source_dimension < 1:
            raise ValueError("source dimension must be at least one")

@dataclass(frozen=True)
class Toda51TypedClaim:
    key: str
    assertion: object
    conditions: tuple[str, ...]
    source_locator: str = "(5.1)"
    proof_eligible: bool = False

    def __post_init__(self):
        if self.key not in {c.key for c in CLAUSES}:
            raise ValueError("unknown Toda (5.1) clause")
        if self.source_locator != "(5.1)" or self.proof_eligible is not False:
            raise ValueError("unverified Toda claim cannot be promoted")

def instantiate_remaining_toda51_clause(key: str, *, i: int | None = None,
                                         n: int | None = None,
                                         k: int | None = None) -> Toda51TypedClaim:
    """Return an instantiation, preserving all stated hypotheses."""
    remaining = {
        "pi_i_n_zero", "negative_stem_zero",
        "stable_zero_stem_cyclic", "stable_identity",
    }
    if key not in remaining:
        raise ValueError("unknown remaining Toda (5.1) clause")
    if key == "pi_i_n_zero":
        if type(i) is not int or type(n) is not int or n < 1 or i < 0 or i >= n:
            raise ValueError("requires integers 0 <= i < n, n >= 1")
        assertion = Relation(
            lhs=TodaPrimaryGroup(group_dimension=i, sphere_dimension=n),
            rhs=0, relation_type=RelationType.EQUALITY,
        )
        return Toda51TypedClaim(key, assertion, ("0 <= i < n", "n >= 1"))
    if key == "negative_stem_zero":
        if type(k) is not int or k >= 0:
            raise ValueError("requires negative integer k")
        assertion = (
            Relation(lhs=StableStem(k), rhs=0, relation_type=RelationType.EQUALITY),
            Relation(lhs=StableStem(k, 2), rhs=0, relation_type=RelationType.EQUALITY),
        )
        return Toda51TypedClaim(key, assertion, ("k < 0",))
    if key == "stable_zero_stem_cyclic":
        if i is not None or n is not None or k is not None:
            raise ValueError("zero-stem claim has no index parameters")
        # Generator symbol is deliberately symbolic: no invented typed stable map.
        return Toda51TypedClaim(
            key, ("G_0", "<iota>", "isomorphic_Z"), (),
        )
    if type(n) is not int or n < 1:
        raise ValueError("requires n >= 1")
    return Toda51TypedClaim(
        key, StableIdentity("iota", f"iota_{n}", n), ("n >= 1",),
    )

def audit_remaining_toda51(bridge) -> dict:
    from phase165_r14_r3_source_scope import collect_toda51_scope
    source = collect_toda51_scope(bridge)
    examples = (
        instantiate_remaining_toda51_clause("pi_i_n_zero", i=2, n=3),
        instantiate_remaining_toda51_clause("negative_stem_zero", k=-1),
        instantiate_remaining_toda51_clause("stable_zero_stem_cyclic"),
        instantiate_remaining_toda51_clause("stable_identity", n=3),
    )
    if len({item.key for item in examples}) != 4:
        raise ValueError("not all remaining clauses represented")
    return {
        "phase": "165 R14-R4",
        "reference_id": source["reference_id"],
        "source_clause_count": source["source_clause_count"],
        "previous_schema_count": source["typed_schema_count"],
        "new_schema_count": len(examples),
        "total_schema_count": source["typed_schema_count"] + len(examples),
        "claims": [{"key": e.key, "conditions": list(e.conditions),
                    "assertion_repr": repr(e.assertion)} for e in examples],
        "adjacent_source_status": source["adjacent_source_status"],
        "mathematically_certified": False,
        "new_proof_eligible": 0, "proof_steps_created": 0,
        "global_ehp_expansion_connected": False,
        "status": "FOUR_SCHEMAS_TYPED_PROVENANCE_NOT_CERTIFIED",
        "full_pytest_run": False,
    }
