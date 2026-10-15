"""Targeted R57-R7 tests (no legacy proof replay)."""
from dataclasses import replace
from pathlib import Path
import ast
import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _typed_case():
    source = TodaPrimaryGroup(4, 3)
    target = TodaPrimaryGroup(5, 4)
    eta3 = HomotopyElement(name="η₃", dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family="η", index=3))
    base = Relation(source, FiniteCyclicGroup(2, eta3), RelationType.EQUALITY)
    suspension = TodaIteratedSuspensionMap(exponent=1, source_group=source, target_group=target)
    iso = Toda45IsomorphismStatement(map=suspension)
    goal = Relation(target, FiniteCyclicGroup(2, IteratedSuspension(expression=eta3, exponent=1)), RelationType.EQUALITY)
    return base, iso, goal


def _bridge(statements):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id="r", kind=ReferenceKind.PROPOSITION,
                                           locator="Test source", source_id="typed-fixture"))
    links = []
    for i, statement in enumerate(statements):
        identifier = "test:" + str(i)
        registry.add_assertion(AssertionEntry(assertion_id=identifier, reference_id="r",
                 kind=AssertionKind.STATEMENT, content=statement, origin=AssertionOrigin.FIXED_STATEMENT))
        links.append(ProofStepLink(assertion_id=identifier, step=ProofStep(
                    conclusion=statement, premises=(), rule=ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def test_typed_source_and_iso_produce_existing_toda45_expansion():
    base, iso, goal = _typed_case()
    options = expand_registered_toda45_finite_cyclic_goal(goal, (base, iso))
    assert len(options) == 1
    assert options[0].subgoals == (base, iso)
    assert "Toda 4.5" in options[0].rule.name


def test_no_isomorphism_or_base_never_creates_source_evidence():
    base, iso, goal = _typed_case()
    assert expand_registered_toda45_finite_cyclic_goal(goal, (base,)) == ()
    assert expand_registered_toda45_finite_cyclic_goal(goal, (iso,)) == ()
    assert expand_registered_toda45_finite_cyclic_goal(goal, ()) == ()


def test_named_eta_is_not_assumed_equal_to_suspension():
    base, iso, goal = _typed_case()
    eta4 = HomotopyElement(name="η₄", dimension=4, source=5, target=4,
                           generator=GeneratorSymbol(family="η", index=4))
    named = replace(goal, rhs=FiniteCyclicGroup(2, eta4))
    assert expand_registered_toda45_finite_cyclic_goal(named, (base, iso)) == ()


def test_shared_provider_exposes_typed_transport_only_with_source():
    base, iso, goal = _typed_case()
    assert any(option.subgoals == (base, iso) for option in shared_expansion_provider(_bridge((base, iso)))(goal))
    assert not any(option.subgoals == (base, iso) for option in shared_expansion_provider(_bridge((base,)))(goal))


def test_targeted_unregistered_toda45_not_given_by_connection():
    source = Path(__file__).resolve().parents[1] / "phase165_r52_r9_shared_math.py"
    body = ast.parse(source.read_text(encoding="utf-8"))
    function = next(x for x in body.body if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider")
    assert any(isinstance(node, ast.Name) and node.id == "expand_registered_toda45_finite_cyclic_goal"
               for node in ast.walk(function))
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "ProofStep"
                   for node in ast.walk(function))
