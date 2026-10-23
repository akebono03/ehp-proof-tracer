"""R57-R20: generic typed scalar specialization with cited source provenance.

The mathematical source is the adopted Toda (5.1) TeX. This module can only
instantiate already-screened symbolic statements: it never treats matching a
goal as evidence and never turns an uncited source into a proof leaf.
"""
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


def _contains_symbol(value: object) -> bool:
    if isinstance(value, ScalarSymbol):
        return True
    if isinstance(value, tuple):
        return any(_contains_symbol(item) for item in value)
    if is_dataclass(value) and not isinstance(value, type):
        return any(_contains_symbol(getattr(value, field.name)) for field in fields(value))
    return False


def _scalar_value(value: object, bindings: dict[str, int]) -> int | None:
    if type(value) is int:
        return value
    if isinstance(value, ScalarSymbol):
        return bindings.get(value.name)
    if isinstance(value, ScalarSum):
        left, right = _scalar_value(value.left, bindings), _scalar_value(value.right, bindings)
        return left + right if left is not None and right is not None else None
    if isinstance(value, ScalarProduct):
        left, right = _scalar_value(value.left, bindings), _scalar_value(value.right, bindings)
        return left * right if left is not None and right is not None else None
    return None


def _bind(pattern: object, concrete: object, bindings: dict[str, int]) -> bool:
    if isinstance(pattern, ScalarSymbol):
        if type(concrete) is not int or concrete < 1:
            return False
        old = bindings.setdefault(pattern.name, concrete)
        return old == concrete
    if isinstance(pattern, (ScalarSum, ScalarProduct)) and type(concrete) is int:
        resolved = _scalar_value(pattern, bindings)
        if resolved is not None:
            return resolved == concrete
        if isinstance(pattern, ScalarSum):
            if isinstance(pattern.left, ScalarSymbol) and type(pattern.right) is int:
                return _bind(pattern.left, concrete - pattern.right, bindings)
            if isinstance(pattern.right, ScalarSymbol) and type(pattern.left) is int:
                return _bind(pattern.right, concrete - pattern.left, bindings)
        return False
    if isinstance(pattern, HomotopyElement) and isinstance(concrete, HomotopyElement):
        if not isinstance(pattern.name, str):
            return False
        if not _bind(pattern.dimension, concrete.dimension, bindings):
            return False
        if pattern.source is not None and not _bind(pattern.source, concrete.source, bindings):
            return False
        if pattern.target is not None and not _bind(pattern.target, concrete.target, bindings):
            return False
        if not _bind(pattern.generator, concrete.generator, bindings):
            return False
        name = _substitute_name(pattern.name, bindings)
        if name == concrete.name:
            return True
        # The registered iota_n schema has no source/target metadata, while
        # older concrete statements use subscript characters in their names.
        if (pattern.name == "ι_n" and pattern.source is None and pattern.target is None
                and concrete.generator is not None
                and concrete.generator.family == "ι"
                and type(concrete.generator.index) is int):
            subscript = str(concrete.generator.index).translate(
                str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            return concrete.name in ("ι" + subscript, "ι_" + str(concrete.generator.index))
        return False
    if type(pattern) is not type(concrete):
        return False
    if isinstance(pattern, tuple):
        return len(pattern) == len(concrete) and all(
            _bind(p, c, bindings) for p, c in zip(pattern, concrete)
        )
    if is_dataclass(pattern) and not isinstance(pattern, type):
        return all(_bind(getattr(pattern, field.name), getattr(concrete, field.name), bindings)
                   for field in fields(pattern))
    return pattern == concrete


def _substitute_name(name: str, bindings: dict[str, int]) -> str:
    # Source notation uses a literal underscore: ι_n -> ι_5.
    for symbol, value in sorted(bindings.items(), key=lambda item: -len(item[0])):
        name = name.replace("_" + symbol, "_" + str(value))
    return name


def _instantiate(value: object, bindings: dict[str, int]) -> object:
    if isinstance(value, (ScalarSymbol, ScalarSum, ScalarProduct)):
        actual = _scalar_value(value, bindings)
        if actual is None:
            raise ValueError("unbound scalar in source template")
        return actual
    if isinstance(value, tuple):
        return tuple(_instantiate(x, bindings) for x in value)
    if isinstance(value, HomotopyElement):
        return replace(value, name=_substitute_name(value.name, bindings),
                       dimension=_instantiate(value.dimension, bindings),
                       source=_instantiate(value.source, bindings),
                       target=_instantiate(value.target, bindings),
                       generator=_instantiate(value.generator, bindings))
    if is_dataclass(value) and not isinstance(value, type):
        return replace(value, **{field.name: _instantiate(getattr(value, field.name), bindings)
                                 for field in fields(value)})
    return value


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
        from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
        from proof import Relation, RelationType
        from expression import ScalarSymbol
        n = ScalarSymbol("n")
        is_diagonal = (
            isinstance(source, Relation)
            and source.relation_type is RelationType.EQUALITY
            and source.lhs == TodaPrimaryGroup(n, n)
            and isinstance(source.rhs, FreeCyclicGroup)
            and isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and isinstance(goal.rhs, FreeCyclicGroup)
            and bindings.get("n") == goal.lhs.sphere_dimension == goal.lhs.group_dimension
            and _bind(source, goal, dict(bindings))
        )
        if not is_diagonal:
            return None
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    if (isinstance(source, TodaPrimaryGroupZeroStatement)
            and source.group.sphere_dimension == 1
            and isinstance(source.group.group_dimension, ScalarSymbol)
            and bindings.get(source.group.group_dimension.name, 0) <= 1):
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


def _specialization_rule(source: object, goal: object) -> InferenceRule:
    def guard(premises, bindings):
        return (len(premises) == 1
                and type(premises[0].conclusion) is type(source)
                and premises[0].conclusion == source
                and specialize_typed_statement(source, goal) is not None)

    def conclusion(premises):
        binding = specialize_typed_statement(premises[0].conclusion, goal)
        if binding is None:
            raise ValueError("unmatched symbolic source")
        # The guard has already checked this exact goal against the registered
        # source, including the iota generator's legacy metadata representation.
        return goal

    return InferenceRule(
        name="generic cited typed scalar specialization",
        premise_patterns=(PremisePattern(statement_type=type(source)),),
        match_guard=guard, conclusion_builder=conclusion,
    )


def expand_cited_general_specialization(
    goal: object, available: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expand only from screened typed source leaves, never from source archives."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    seen: list[object] = []
    output: list[GoalExpansion] = []
    for source in available:
        if source in seen:
            continue
        if specialize_typed_statement(source, goal) is not None:
            seen.append(source)
            output.append(GoalExpansion(_specialization_rule(source, goal), (source,)))
    return tuple(output)


def build_adopted_toda51_diagonal_reference(tex_path: Path) -> RegistryBridgeResult:
    """Register the cited symbolic diagonal clause of the adopted (5.1) TeX.

    Only the exact existing source sentence authorizes this schema. It is a
    fixed literature assertion (and hence may be a GIVEN leaf), not a derived
    group result, and it carries the original Toda (5.1) citation.
    """
    tex = Path(tex_path).read_text(encoding="utf8")
    expected = r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z"
    if expected not in tex:
        raise ValueError("adopted Toda (5.1) diagonal clause missing or changed")
    n = ScalarSymbol("n")
    statement = Relation(
        lhs=TodaPrimaryGroup(group_dimension=n, sphere_dimension=n),
        rhs=FreeCyclicGroup(HomotopyElement(
            name="ι_n", dimension=n,
            generator=GeneratorSymbol(family="ι", index=n),
        )),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    reference_id = "adopted:toda51:diagonal"
    assertion_id = "adopted:assertion:toda51:diagonal"
    registry.add_reference(LiteratureEntry(
        reference_id=reference_id, kind=ReferenceKind.EQUATION,
        locator="(5.1)", source_id="Toda translated TeX:(5.1) (adopted; original edition unverified)",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=assertion_id, reference_id=reference_id,
        kind=AssertionKind.STATEMENT, content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("symbolic_diagonal", "n_positive"),
    ))
    cited_step = ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.1) diagonal cyclic source",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    return RegistryBridgeResult(
        registry, (), (ProofStepLink(assertion_id=assertion_id, step=cited_step),)
    )
