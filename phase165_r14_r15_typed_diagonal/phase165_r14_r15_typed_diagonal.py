"""R14-R15: connect Toda (5.1) typed clauses to diagonal suspension obligations.

Source claims are not independently verified and never become proof leaves here.
"""
from __future__ import annotations
from dataclasses import dataclass
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from proof import Relation
from phase165_r14_r2_toda51 import TODA_51_SCHEMAS, instantiate_toda51_clause
from phase165_r14_r14_diagonal_and_prop42 import (
    diagonal_suspension_subgoals, review_prop42_scope,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


@dataclass(frozen=True)
class TypedPremiseBinding:
    goal: object
    source_locator: str | None
    kind: str
    verified: bool = False
    proof_eligible: bool = False


def match_diagonal_toda51_claims(suspension: TodaSuspensionMap) -> tuple[TypedPremiseBinding, ...]:
    """Specialize the existing (5.1) schema and compare structural goal types."""
    goals = diagonal_suspension_subgoals(suspension)
    if goals is None:
        return ()
    schema = next(x for x in TODA_51_SCHEMAS if x.name == 'diagonal_infinite_cyclic')
    rows = []
    for index, expected in ((suspension.source_group.sphere_dimension, goals[0]),
                            (suspension.target_group.sphere_dimension, goals[1])):
        typed = instantiate_toda51_clause(schema, index)
        if not isinstance(typed, Relation) or typed.lhs != expected.lhs:
            raise ValueError('Toda (5.1) diagonal group does not match target')
        if typed.rhs.generator.generator != expected.rhs.generator.generator:
            raise ValueError('Toda (5.1) diagonal generator does not match target')
        if typed.rhs.generator.source != expected.rhs.generator.source or typed.rhs.generator.target != expected.rhs.generator.target:
            raise ValueError('Toda (5.1) generator dimensions differ')
        rows.append(TypedPremiseBinding(expected, '(5.1)', 'TODA51_DIAGONAL_TYPED_SOURCE_ONLY'))
    rows.append(TypedPremiseBinding(goals[2], None, 'GENERATOR_SUSPENSION_NEEDS_SOURCE'))
    return tuple(rows)


def audit_r15(bridge=None) -> dict:
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    goal = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    )
    rows = match_diagonal_toda51_claims(goal.map)
    prop42 = review_prop42_scope(bridge)
    return {
        'phase': '165 R14-R15',
        'diagonal_goal': repr(goal),
        'typed_premise_count': len(rows),
        'toda51_bound': sum(r.source_locator == '(5.1)' for r in rows),
        'generator_suspension_source_confirmed': False,
        'premises': [{'goal': repr(r.goal), 'locator': r.source_locator,
                      'kind': r.kind, 'verified': r.verified,
                      'proof_eligible': r.proof_eligible} for r in rows],
        'prop42_source_candidate_count': len(prop42),
        'prop42_selected': False,
        'prop42_application_verified': False,
        'eligible_new_leaves': 0,
        'proof_steps_created': 0,
        'status': 'DIAGONAL_TODA51_SCHEMAS_BOUND_UNVERIFIED',
        'full_pytest_run': False,
    }
