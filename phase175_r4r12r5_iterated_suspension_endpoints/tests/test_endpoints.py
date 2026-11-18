"""R4R12R5: real DB generator endpoints and rejection contract."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, HomotopyElement, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r3_two_summand_quotient.rule import _rank_two_endpoints
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from proof import ProofStep, Relation


def test_actual_db_iterated_suspension_is_composable() -> None:
    middle=exact_prior_database_result(4,4)
    assert isinstance(middle,Relation)
    parts=middle.rhs.summands
    assert isinstance(parts[1].generator, Composition)
    assert isinstance(parts[1].generator.left, IteratedSuspension)
    assert _rank_two_endpoints(parts[1].generator.left)==(7,4)
    assert _rank_two_endpoints(parts[1].generator)==(8,4)
    assert _rank_two_endpoints(parts[0].generator)==(8,4)


def test_actual_root_yields_conditional_unproved_candidates() -> None:
    root=exact_prior_database_result(5,4)
    assert isinstance(root,Relation)
    goal=CyclicStructureStatement(root.lhs,root.rhs.generator,2)
    proposals=expand_public_two_summand_quotient(goal,proof_target=root)
    assert len(proposals)==2
    assert all(len(p.subgoals)==6 for p in proposals)
    assert all(not any(isinstance(sub,ProofStep) for sub in p.subgoals) for p in proposals)


def test_bad_exponent_and_noncomposable_suspension_are_rejected() -> None:
    middle=exact_prior_database_result(4,4)
    left=middle.rhs.summands[1].generator.left
    assert _rank_two_endpoints(replace(left,exponent=-1)) is None
    assert _rank_two_endpoints(replace(left,exponent=True)) is None
    assert _rank_two_endpoints(replace(left,exponent='n')) is None
    assert _rank_two_endpoints(Composition(left,middle.rhs.summands[1].generator.left)) is None


def test_bad_inner_generator_endpoints_rejected() -> None:
    middle=exact_prior_database_result(4,4)
    left=middle.rhs.summands[1].generator.left
    inner=replace(left.expression,source=3,target=6)
    assert _rank_two_endpoints(replace(left,expression=inner)) is None
