"""Phase 165 R57-R24: discover typed backward rule candidates only.

R23 unifies conclusions. R24 discovers candidate rules from explicit catalogs
or the existing R8 factory inventory. R25 owns premise generation; no proof is
created or accepted here. A builder-only rule is never reverse-matched.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r57_r23_conclusion_unification import (
    ConclusionUnification,
    unify_inference_conclusion,
)
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
from proof import InferenceRule
from rule_catalog import (
    InferenceRuleCatalog,
    InferenceRuleCatalogEntry,
    find_goal_compatible_rule_entries,
)


@dataclass(frozen=True)
class DiscoveredRuleCandidate:
    """A candidate to be expanded later, not an established proof."""

    key: str
    unification: ConclusionUnification
    source: str


def discover_catalog_goal_candidates(
    catalog: InferenceRuleCatalog, goal: object
) -> tuple[DiscoveredRuleCandidate, ...]:
    """Select eligible registered rules and verify their conclusion patterns.

    Existing catalog safety and compatibility gates are retained. Exact type
    compatibility alone is not enough to establish a unification.
    """
    if not isinstance(catalog, InferenceRuleCatalog):
        raise TypeError("catalog must be InferenceRuleCatalog")
    found: list[DiscoveredRuleCandidate] = []
    for entry in find_goal_compatible_rule_entries(catalog, goal):
        match = unify_inference_conclusion(entry.rule, goal)
        if match is not None:
            found.append(DiscoveredRuleCandidate(entry.key, match, "catalog"))
    return tuple(found)


def discover_explicit_goal_candidates(
    rules: tuple[InferenceRule, ...], goal: object
) -> tuple[DiscoveredRuleCandidate, ...]:
    """Select matches from a caller-supplied, explicitly trusted rule tuple.

    Repeated identities are emitted once; distinct rules sharing a name remain
    distinct. Caller ordering is preserved.
    """
    if not isinstance(rules, tuple) or any(not isinstance(rule, InferenceRule) for rule in rules):
        raise TypeError("rules must be a tuple of InferenceRule")
    found: list[DiscoveredRuleCandidate] = []
    seen_ids: set[int] = set()
    for index, rule in enumerate(rules):
        if id(rule) in seen_ids:
            continue
        seen_ids.add(id(rule))
        match = unify_inference_conclusion(rule, goal)
        if match is not None:
            found.append(DiscoveredRuleCandidate(f"explicit:{index}:{rule.name}", match, "explicit"))
    return tuple(found)


def discover_factory_goal_candidates(
    goal: object, module_names: tuple[str, ...] = DEFAULT_RULE_MODULES
) -> tuple[tuple[DiscoveredRuleCandidate, ...], object]:
    """Reuse R8's inspected zero-argument factory discovery.

    The accompanying R8 report records skipped factories and opaque rules.
    Factory discovery is not evidence that a cited theorem or proof exists.
    """
    if not isinstance(module_names, tuple) or any(not isinstance(name, str) for name in module_names):
        raise TypeError("module_names must be a tuple of module strings")
    rules, report = discover_inference_rules(module_names)
    candidates = discover_explicit_goal_candidates(rules, goal)
    return (
        tuple(DiscoveredRuleCandidate(
            key=candidate.key.replace("explicit:", "factory:", 1),
            unification=candidate.unification,
            source="factory",
        ) for candidate in candidates),
        report,
    )
