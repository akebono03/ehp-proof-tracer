"""Unified, conservative registration for backward rule sources.

No factory requiring arguments is invoked. No rule is certified by registration.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import inspect
from typing import Callable

from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
from proof import InferenceRule


@dataclass(frozen=True)
class RegisteredBackwardRule:
    rule_id: str
    rule: InferenceRule
    origin: str
    eligibility: str


class UnifiedBackwardRuleRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegisteredBackwardRule] = {}

    def register(self, rule_id: str, rule: InferenceRule, *, origin: str,
                 eligibility: str = "CANDIDATE_NOT_CERTIFIED") -> None:
        if not rule_id or not isinstance(rule_id, str):
            raise ValueError("rule_id must be a nonempty string")
        if not isinstance(rule, InferenceRule):
            raise TypeError("rule must be InferenceRule")
        if not origin or not isinstance(origin, str):
            raise ValueError("origin must be a nonempty string")
        if rule_id in self._entries:
            raise ValueError("duplicate rule ID: " + rule_id)
        self._entries[rule_id] = RegisteredBackwardRule(rule_id, rule, origin, eligibility)

    def entries(self) -> tuple[RegisteredBackwardRule, ...]:
        return tuple(self._entries.values())

    def rules(self) -> tuple[InferenceRule, ...]:
        return tuple(entry.rule for entry in self._entries.values())


def build_unified_backward_rule_registry(
    *, module_names: tuple[str, ...] = DEFAULT_RULE_MODULES,
    extra_rules: tuple[tuple[str, InferenceRule], ...] = (),
) -> tuple[UnifiedBackwardRuleRegistry, dict]:
    """Read the same eligible no-arg factories as R8, with stable source IDs.

    extra_rules are explicitly supplied and never obtained by guessing factory args.
    """
    registry = UnifiedBackwardRuleRegistry()
    skipped: list[str] = []
    for module_name in module_names:
        module = import_module(module_name)
        for name, factory in sorted(vars(module).items()):
            if not (name.endswith("_inference_rule") and callable(factory)
                    and getattr(factory, "__module__", None) == module.__name__):
                continue
            rule_id = module_name + "." + name
            try:
                signature = inspect.signature(factory)
                required = [p for p in signature.parameters.values()
                            if p.default is inspect.Parameter.empty
                            and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                           inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                           inspect.Parameter.KEYWORD_ONLY)]
                if required:
                    skipped.append(rule_id + ":requires-input")
                    continue
                rule = factory()
            except (ValueError, TypeError, AttributeError, RuntimeError) as exc:
                skipped.append(rule_id + ":" + type(exc).__name__)
                continue
            if not isinstance(rule, InferenceRule):
                skipped.append(rule_id + ":not-rule")
                continue
            registry.register(rule_id, rule, origin="R8_FACTORY")
    for rule_id, rule in extra_rules:
        registry.register(rule_id, rule, origin="EXPLICIT_REGISTERED")
    report = {"registered": len(registry.entries()),
              "skipped": skipped,
              "rule_ids": [e.rule_id for e in registry.entries()]}
    return registry, report
