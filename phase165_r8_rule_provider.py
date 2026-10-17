"""Phase 165 R8: shared inverse pattern inference catalog.

Only invertible, fully bound InferenceRule patterns are used. No legacy
ProofSteps, unreviewed literature, or target-specific rules are manufactured.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import inspect
from typing import Iterable

from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    PatternVariable,
    PremisePattern,
    Relation,
    match_relation_pattern,
    match_statement_pattern,
    substitute_pattern_value,
)

# This is a module catalog, not a collection of group-specific proof premises.
DEFAULT_RULE_MODULES = (
    "ehp_rules", "stable_rules", "set_rules", "hopf_rules",
    "scalar_rules", "relation_rules", "map_property_rules",
    "homomorphism_rules", "indeterminacy_rules", "phase165_r12_r2_quotient_rules",
    "phase165_r12_r5_structure_bridge",
)


@dataclass(frozen=True)
class RuleCatalogReport:
    modules: tuple[str, ...]
    rule_names: tuple[str, ...]
    skipped_factories: tuple[str, ...]
    skipped_rules: tuple[str, ...]


def _unresolved_pattern(value: object) -> bool:
    from dataclasses import fields, is_dataclass
    if isinstance(value, PatternVariable):
        return True
    if is_dataclass(value):
        return any(_unresolved_pattern(getattr(value, f.name)) for f in fields(value))
    if isinstance(value, (tuple, list)):
        return any(_unresolved_pattern(v) for v in value)
    return False


def _pattern_variable_names(value: object) -> frozenset[str]:
    """Find every variable before substitution can replace an unknown with None."""
    from dataclasses import fields, is_dataclass
    if isinstance(value, PatternVariable):
        return frozenset((value.name,))
    if is_dataclass(value):
        return frozenset(
            name
            for field in fields(value)
            for name in _pattern_variable_names(getattr(value, field.name))
        )
    if isinstance(value, (tuple, list)):
        return frozenset(
            name for member in value for name in _pattern_variable_names(member)
        )
    return frozenset()


def _inverse(rule: InferenceRule, goal: object) -> GoalExpansion | None:
    pattern = rule.conclusion_pattern
    if pattern is None or not rule.premise_patterns:
        return None
    if isinstance(pattern, Relation) and isinstance(goal, Relation):
        bindings = match_relation_pattern(pattern, goal)
    elif type(pattern) is type(goal):
        try:
            bindings = match_statement_pattern(pattern, goal)
        except (TypeError, ValueError):
            return None
    else:
        return None
    if bindings is None:
        return None
    subgoals = []
    for premise in rule.premise_patterns:
        if not isinstance(premise, PremisePattern):
            return None
        template = premise.relation_pattern if premise.relation_pattern is not None else premise.statement_pattern
        if template is None:
            return None
        bound_names = frozenset(binding.variable.name for binding in bindings)
        if not _pattern_variable_names(template).issubset(bound_names):
            return None
        concrete = substitute_pattern_value(template, bindings)
        if _unresolved_pattern(concrete):
            return None
        subgoals.append(concrete)
    return GoalExpansion(rule=rule, subgoals=tuple(subgoals))


def discover_inference_rules(
    module_names: tuple[str, ...] = DEFAULT_RULE_MODULES,
) -> tuple[tuple[InferenceRule, ...], RuleCatalogReport]:
    """Obtain rule factories through the single R10 Rule Registry.

    This preserves the existing public API and discovery priority. It does
    not grant ProofStep/reference authority or synthesize missing inputs.
    """
    from phase165_r10_rule_registry import build_rule_registry
    registry = build_rule_registry(module_names)
    return registry.rules(), RuleCatalogReport(
        modules=registry.modules,
        rule_names=tuple(entry.rule.name for entry in registry.entries),
        skipped_factories=registry.skipped_factories,
        skipped_rules=registry.skipped_rules,
    )


def create_rule_expansion_provider(rules: Iterable[InferenceRule]):
    """Return a generic goal->expansions function for R3's search engine."""
    catalog = tuple(rules)
    if any(not isinstance(rule, InferenceRule) for rule in catalog):
        raise TypeError("catalog contains a non-InferenceRule")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        output = []
        for rule in catalog:
            candidate = _inverse(rule, goal)
            if candidate is not None:
                output.append(candidate)
        return tuple(output)

    return expand


def build_production_rule_provider():
    """Use existing rule definitions only, without granting citation rights."""
    rules, report = discover_inference_rules()
    return create_rule_expansion_provider(rules), report
