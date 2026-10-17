"""Phase 165 R10: canonical inventory for public zero-argument inference rule factories.

A rule ID identifies a *factory*, not a mathematical equivalence class.
No reference or ProofStep is conferred by registry membership.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import inspect

from proof import InferenceRule


@dataclass(frozen=True)
class RegisteredInferenceRule:
    rule_id: str
    rule: InferenceRule
    factory_module: str
    factory_name: str
    backward_pattern_candidate: bool


@dataclass(frozen=True)
class RuleRegistrySnapshot:
    entries: tuple[RegisteredInferenceRule, ...]
    modules: tuple[str, ...]
    skipped_factories: tuple[str, ...]
    skipped_rules: tuple[str, ...]

    def rules(self) -> tuple[InferenceRule, ...]:
        return tuple(entry.rule for entry in self.entries)

    def by_id(self, rule_id: str) -> RegisteredInferenceRule:
        matches = tuple(entry for entry in self.entries if entry.rule_id == rule_id)
        if len(matches) != 1:
            raise KeyError(rule_id)
        return matches[0]


def build_rule_registry(module_names: tuple[str, ...]) -> RuleRegistrySnapshot:
    """Read each configured factory once; reject duplicate stable factory IDs.

    Deliberately does not instantiate factories requiring arguments/witnesses.
    The supplied module order controls rule priority and preserves R8's contract.
    """
    if not isinstance(module_names, tuple) or not all(
        isinstance(name, str) and name for name in module_names
    ):
        raise TypeError("module_names must be a tuple of nonempty names")
    entries: list[RegisteredInferenceRule] = []
    skipped: list[str] = []
    seen_ids: set[str] = set()
    for module_name in module_names:
        module = import_module(module_name)
        for name, factory in sorted(vars(module).items()):
            if not (
                name.endswith("_inference_rule")
                and callable(factory)
                and getattr(factory, "__module__", None) == module.__name__
            ):
                continue
            rule_id = f"{module_name}.{name}"
            if rule_id in seen_ids:
                raise ValueError(f"duplicate rule ID: {rule_id}")
            seen_ids.add(rule_id)
            try:
                signature = inspect.signature(factory)
                required = [
                    parameter
                    for parameter in signature.parameters.values()
                    if parameter.default is inspect.Parameter.empty
                    and parameter.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        inspect.Parameter.KEYWORD_ONLY,
                    )
                ]
                if required:
                    skipped.append(f"{rule_id}:requires-input")
                    continue
                rule = factory()
            except (ValueError, TypeError, AttributeError, RuntimeError) as exc:
                skipped.append(f"{rule_id}:{type(exc).__name__}")
                continue
            if not isinstance(rule, InferenceRule):
                skipped.append(f"{rule_id}:not-rule")
                continue
            entries.append(
                RegisteredInferenceRule(
                    rule_id=rule_id,
                    rule=rule,
                    factory_module=module_name,
                    factory_name=name,
                    backward_pattern_candidate=(
                        rule.conclusion_pattern is not None and bool(rule.premise_patterns)
                    ),
                )
            )
    return RuleRegistrySnapshot(
        entries=tuple(entries),
        modules=module_names,
        skipped_factories=tuple(skipped),
        skipped_rules=tuple(
            entry.rule.name for entry in entries if entry.rule.conclusion_pattern is None
        ),
    )
