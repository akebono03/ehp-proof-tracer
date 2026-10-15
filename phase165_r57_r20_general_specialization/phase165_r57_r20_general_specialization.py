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
        if not _bind(pattern.source, concrete.source, bindings):
            return False
        if not _bind(pattern.target, concrete.target, bindings):
            return False
        if not _bind(pattern.generator, concrete.generator, bindings):
            return False
        name = _substitute_name(pattern.name, bindings)
        return name == concrete.name
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


def specialize_typed_statement(source: object, goal: object) -> tuple[tuple[str, int], ...] | None:
    """Find explicit scalar bindings with exact instantiated-goal equality."""
    if not _contains_symbol(source):
        return None
    bindings: dict[str, int] = {}
    if not _bind(source, goal, bindings):
        return None
    if _instantiate(source, bindings) != goal:
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
        return _instantiate(premises[0].conclusion, dict(binding))

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
