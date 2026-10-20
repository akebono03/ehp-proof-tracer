# R3-G modified source units

## phase165_r52_r27_r5_literature.py

```python
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from expression import ScalarProduct, ScalarSum, ScalarSymbol
from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup
from toda_rules import Toda45IsomorphismStatement
from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationRecord, MigrationStatus
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)
def _toda45_universal_statement() -> Toda45IsomorphismStatement:
    """The whole (4.5) map schema; numerical domain is validated on use."""
    n, k, m = ScalarSymbol("n"), ScalarSymbol("k"), ScalarSymbol("m")
    return Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=ScalarSum(left=m, right=ScalarProduct(left=-1, right=n)),
        source_group=TodaPrimaryGroup(
            group_dimension=ScalarSum(left=n, right=k), sphere_dimension=n,
        ),
        target_group=TodaPrimaryGroup(
            group_dimension=ScalarSum(left=m, right=k), sphere_dimension=m,
        ),
    ))

def _register_toda45(registry, links, records, source_bridge) -> None:
    source_id = "toda:tex:ch4:0006"
    candidates = [
        a for a in source_bridge.registry._assertions.values()
        if a.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(a.content, dict)
        and a.content.get("source_statement_id") == source_id
    ]
    if len(candidates) != 1:
        raise ValueError("unique source archive entry required: (4.5)")
    archive = candidates[0].content
    source_text = archive.get("source_text")
    if (not isinstance(source_text, str)
            or archive.get("source_sha256") != sha256(source_text.encode("utf-8")).hexdigest()
            or "E" not in source_text):
        raise ValueError("source content does not match reviewed scope: (4.5)")
    ref_id = f"typed_literature:{source_id}"
    assertion_id = f"typed_literature:assertion:{source_id}"
    statement = _toda45_universal_statement()
    registry.add_reference(LiteratureEntry(
        ref_id, ReferenceKind.EQUATION, "(4.5)", source_id=source_id,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id, ref_id, AssertionKind.STATEMENT, statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("n>=k+2", "m>=n", "k>=0"),
    ))
    links.append(ProofStepLink(
        assertion_id, step=ProofStep(
            conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        ),
    ))
    records.append(MigrationRecord(
        "phase166_r3g", "(4.5)", assertion_id,
        MigrationStatus.STRUCTURED,
        "typed universal suspension map with explicit numerical domain",
    ))

def build_typed_literature_bridge(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Produce two fixed, source-bound general claims; never promote other archive rows."""
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for locator, source_id, digest, tokens, claim, kind in _SOURCES:
        candidates = [
            a for a in source_bridge.registry._assertions.values()
            if a.origin is AssertionOrigin.SOURCE_ARCHIVE
            and isinstance(a.content, dict)
            and a.content.get("source_statement_id") == source_id
        ]
        if len(candidates) != 1:
            raise ValueError(f"unique source archive entry required: {locator}")
        archive = candidates[0].content
        text = archive.get("source_text")
        if (not isinstance(text, str) or archive.get("source_sha256") != digest
                or any(token not in text for token in tokens)):
            raise ValueError(f"source content does not match reviewed scope: {locator}")
        ref_id = f"typed_literature:{source_id}"
        assertion_id = f"typed_literature:assertion:{source_id}"
        registry.add_reference(LiteratureEntry(ref_id, kind, locator, source_id=source_id))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        )))
        records.append(MigrationRecord(
            "phase165_r52_r27_r5", locator, assertion_id,
            MigrationStatus.STRUCTURED, "typed universal literature claim; specialization not certified",
        ))
    _register_toda45(registry, links, records, source_bridge)
    return RegistryBridgeResult(registry, tuple(records), tuple(links))

```

## phase165_r57_r20_general_specialization.py

```python
from __future__ import annotations
from dataclasses import fields, is_dataclass, replace
from pathlib import Path
from expression import GeneratorSymbol, HomotopyElement, ScalarProduct, ScalarSum, ScalarSymbol
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)
def _bind_symbolic_constraints(pattern: object, concrete: object, bindings: dict[str, int]) -> bool:
    """Solve typed scalar equalities in dependency order, not field order."""
    constraints = []

    def flatten(p, c):
        if type(p) is not type(c) and not isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)):
            return False
        if isinstance(p, tuple):
            if len(p) != len(c):
                return False
            return all(flatten(x, y) for x, y in zip(p, c))
        if is_dataclass(p) and not isinstance(p, type) and not isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)):
            return all(flatten(getattr(p, field.name), getattr(c, field.name)) for field in fields(p))
        constraints.append((p, c))
        return True

    if not flatten(pattern, concrete):
        return False
    pending = list(constraints)
    for _ in range(len(pending) + 1):
        if not pending:
            return True
        next_pending = []
        advanced = False
        for p, c in pending:
            if isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)) and type(c) is int:
                expr = _linear_scalar_expression(p)
                if expr is None:
                    return False
                coefficients, constant = expr
                remaining = {v: a for v, a in coefficients.items() if v not in bindings and a}
                known = constant + sum(a * bindings[v] for v, a in coefficients.items() if v in bindings)
                if not remaining:
                    if known != c:
                        return False
                    advanced = True
                elif len(remaining) == 1:
                    name, a = next(iter(remaining.items()))
                    if (c - known) % a:
                        return False
                    bindings[name] = (c - known) // a
                    advanced = True
                else:
                    next_pending.append((p, c))
            elif _bind(p, c, bindings):
                advanced = True
            else:
                return False
        if not advanced:
            return False
        pending = next_pending
    return not pending

def _linear_scalar_expression(value: object):
    """Represent an affine scalar expression as (coefficients, constant)."""
    if type(value) is int:
        return ({}, value)
    if isinstance(value, ScalarSymbol):
        return ({value.name: 1}, 0)
    if isinstance(value, ScalarSum):
        left, right = _linear_scalar_expression(value.left), _linear_scalar_expression(value.right)
        if left is None or right is None:
            return None
        coeff = dict(left[0])
        for name, amount in right[0].items():
            coeff[name] = coeff.get(name, 0) + amount
        return (coeff, left[1] + right[1])
    if isinstance(value, ScalarProduct):
        if type(value.left) is int:
            factor, inner = value.left, _linear_scalar_expression(value.right)
        elif type(value.right) is int:
            factor, inner = value.right, _linear_scalar_expression(value.left)
        else:
            return None
        if inner is None:
            return None
        return ({name: factor * amount for name, amount in inner[0].items()}, factor * inner[1])
    return None

def specialize_typed_statement(source: object, goal: object) -> tuple[tuple[str, int], ...] | None:
    """Bind general numeric schemas, checking (4.5) stable-range conditions."""
    if not _contains_symbol(source):
        return None
    bindings: dict[str, int] = {}
    from toda_rules import Toda45IsomorphismStatement
    matching = (_bind_symbolic_constraints(source, goal, bindings)
                if isinstance(source, Toda45IsomorphismStatement)
                else _bind(source, goal, bindings))
    if not matching:
        return None
    try:
        instantiated = _instantiate(source, bindings)
    except (ValueError, TypeError):
        return None
    if instantiated != goal:
        return None
    from phase165_prop51_range_guard import allows_typed_specialization
    if not allows_typed_specialization(source, bindings):
        return None
    from toda_rules import Toda45IsomorphismStatement
    if isinstance(source, Toda45IsomorphismStatement):
        n, k, m = (bindings.get(name) for name in ("n", "k", "m"))
        if (any(type(x) is not int for x in (n, k, m))
                or k < 0 or n < k + 2 or m < n):
            return None
    return tuple(sorted(bindings.items()))

```

## phase165_r52_r27_r5_typed_references\test_r5_typed_references.py

```python
def test_r5_two_general_literature_claims_linked_as_exact_references():
    production = discover_goal_search_inputs().bridge
    bridge = build_typed_literature_bridge(production)
    assert len(bridge.proof_links) == 3
    assert {type(a.content) for a in bridge.registry._assertions.values()} == {
        TodaProp44UniversalStatement, Toda52UniversalStatement,
        Toda45IsomorphismStatement,
    }
    for assertion in bridge.registry._assertions.values():
        assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
        steps = _typed_reference_steps(bridge, assertion.content)
        assert len(steps) == 1
        assert steps[0].rule is ProofRule.GIVEN
        assert steps[0].conclusion == assertion.content

def test_r5_shared_bridge_contains_two_typed_literature_claims():
    bridge = build_shared_typed_bridge()
    for statement in (TodaProp44UniversalStatement(), Toda52UniversalStatement()):
        assert len(_typed_reference_steps(bridge, statement)) == 1

def test_r5_no_unchecked_source_promotion():
    production = discover_goal_search_inputs().bridge
    old = build_typed_literature_bridge(production)
    assert len(old.proof_links) == 3
    assert Toda52UniversalStatement().minimum_i == 3
    assert TodaProp44UniversalStatement().includes_suspension_injectivity
    assert all(link.step.rule is ProofRule.GIVEN for link in old.proof_links)

def test_r5_missing_source_rejected():
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    empty = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError, match="unique source archive"):
        build_typed_literature_bridge(empty)

```
