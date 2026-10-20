from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
)
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from proof import Relation
from toda_rules import Toda45IsomorphismStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from unified_statement_registry import AssertionOrigin
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context

def _fixture():
    source = TodaPrimaryGroup(4, 3)
    target = TodaPrimaryGroup(5, 4)
    eta3 = HomotopyElement(
        name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    base = Relation(source, FiniteCyclicGroup(2, eta3))
    goal = Relation(target, FiniteCyclicGroup(2, IteratedSuspension(eta3, 1)))
    iso = Toda45IsomorphismStatement(
        TodaIteratedSuspensionMap(exponent=1, source_group=source, target_group=target)
    )
    return base, iso, goal

def test_r3u_general_toda45_proposes_concrete_iso_as_subgoal():
    base, iso, goal = _fixture()
    bridge = build_shared_typed_bridge()
    target_id = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=target_id,
        explicit_publication_target=True,
    )
    statements = tuple(
        link.step.conclusion for link in screened.proof_links if link.step is not None
    )
    assert base in statements
    assert any(
        isinstance(statement, Toda45IsomorphismStatement)
        and specialize_typed_statement(statement, iso) is not None
        for statement in statements
    )
    options = expand_registered_toda45_finite_cyclic_goal(goal, statements)
    assert any(option.subgoals == (base, iso) for option in options)

def test_r3u_no_general_toda45_does_not_offer_transport():
    base, _, goal = _fixture()
    assert expand_registered_toda45_finite_cyclic_goal(goal, (base,)) == ()

def test_r3u_named_eta4_is_not_silently_identified():
    base, iso, goal = _fixture()
    eta4 = HomotopyElement(
        name="η_4", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4),
    )
    named = Relation(goal.lhs, FiniteCyclicGroup(2, eta4))
    assert expand_registered_toda45_finite_cyclic_goal(named, (base, iso)) == ()
