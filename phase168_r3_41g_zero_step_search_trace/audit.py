"""Trace accepted proof steps and root expansions without changing search rules.

The audit wraps the existing observer and expansion provider but leaves their
return values and invocation order unchanged. This is observation only.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any, Callable
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
CASES = (
    ("pi6_4", 4, 2),
    ("pi6_3", 3, 3),
    ("pi5_4_control", 4, 1),
    ("pi4_3_control", 3, 1),
)
SOURCES = (
    "phase165_r3_recursive_search.py",
    "phase165_r52_r2_search_adapter.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r55_nk_only_goal.py",
    "phase168_r3_5_model_renderer.py",
)
MAX_EXCERPT = 220
MAX_EVENTS = 160
MAX_EXPANSIONS = 140
MAX_ROOT_RULES = 80


def excerpt(value: object, limit: int = MAX_EXCERPT) -> str:
    rendered = repr(value)
    return rendered if len(rendered) <= limit else rendered[:limit] + " [truncated]"


@dataclass
class SearchObservation:
    """Audit-only measurements. No assertions or proof steps are manufactured."""

    reconstruction_calls: int = 0
    lookup_modes: list[str] = field(default_factory=list)
    root_goal: object | None = None
    event_counts: Counter = field(default_factory=Counter)
    logged_events: list[dict[str, object]] = field(default_factory=list)
    expansion_calls: int = 0
    expansion_options: int = 0
    logged_expansions: list[dict[str, object]] = field(default_factory=list)
    root_provider_calls: int = 0
    root_option_count: int = 0
    root_rule_names: list[str] = field(default_factory=list)
    accepted_steps: list[object] = field(default_factory=list)
    unresolved_targets: list[object] = field(default_factory=list)
    no_option_targets: list[object] = field(default_factory=list)

    def observe(self, kind: str, goal: object, step: object) -> None:
        self.event_counts[kind] += 1
        if len(self.logged_events) < MAX_EVENTS:
            rule = getattr(getattr(step, "inference_rule", None), "name", None)
            self.logged_events.append({
                "kind": kind, "goal_type": type(goal).__name__,
                "goal": excerpt(goal), "step_rule": rule,
            })
        if kind == "proved" and step is not None:
            self.accepted_steps.append(step)
        elif kind == "unresolved":
            if len(self.unresolved_targets) < MAX_EVENTS:
                self.unresolved_targets.append(goal)

    def observe_options(self, goal: object, options: tuple) -> None:
        self.expansion_calls += 1
        self.expansion_options += len(options)
        if not options and len(self.no_option_targets) < MAX_EVENTS:
            self.no_option_targets.append(goal)
        if self.root_goal is not None and (
            goal is self.root_goal
            or (type(goal) is type(self.root_goal) and goal == self.root_goal)
        ):
            self.root_provider_calls += 1
            self.root_option_count += len(options)
            for option in options:
                name = option.rule.name
                if len(self.root_rule_names) < MAX_ROOT_RULES:
                    self.root_rule_names.append(name)
        if len(self.logged_expansions) < MAX_EXPANSIONS:
            self.logged_expansions.append({
                "goal_type": type(goal).__name__,
                "goal": excerpt(goal),
                "option_count": len(options),
                "rules": [option.rule.name for option in options[:16]],
                "first_subgoals": [
                    [excerpt(child) for child in option.subgoals[:6]]
                    for option in options[:8]
                ],
            })


def instrument_reconstruction(
    original: Callable[..., object],
    args: tuple,
    kwargs: dict,
    observation: SearchObservation,
) -> object:
    """Call the original search exactly once, forwarding its observed events.

    Do not substitute an expansion, register a rule, or modify an observed
    ProofStep. Preserve the original observer by chaining callbacks.
    """
    if len(args) < 4:
        raise TypeError("Expected canonical reconstruction's four arguments")
    observation.reconstruction_calls += 1
    if observation.root_goal is None:
        observation.root_goal = args[0]
    observation.lookup_modes.append(str(kwargs.get("lookup_mode", "legacy")))
    original_provider = args[3]
    original_observer = kwargs.get("progress_observer")

    def traced_provider(goal: object) -> tuple:
        options = original_provider(goal)
        if isinstance(options, tuple):
            observation.observe_options(goal, options)
        return options

    def chained_observer(kind: str, goal: object, step: object) -> None:
        if original_observer is not None:
            original_observer(kind, goal, step)
        observation.observe(kind, goal, step)

    passed_args = list(args)
    passed_args[3] = traced_provider
    passed_kwargs = dict(kwargs)
    passed_kwargs["progress_observer"] = chained_observer
    return original(*passed_args, **passed_kwargs)


def classify_search(
    *, status: str, reconstruct_calls: int,
    root_provider_calls: int, root_option_count: int,
    accepted_event_count: int,
) -> str:
    """Classification describes the observed route, not mathematical truth."""
    if status == "complete":
        return "COMPLETE_CONTROL"
    if reconstruct_calls == 0:
        return "FAILED_BEFORE_RECONSTRUCTION"
    if root_provider_calls == 0:
        return "ROOT_NOT_EXPANDED_OR_DIRECTLY_RESOLVED"
    if root_option_count == 0:
        return "ROOT_NO_EXPANSIONS"
    if accepted_event_count == 0:
        return "ROOT_EXPANSIONS_BUT_NO_ACCEPTED_PROOF_STEPS"
    return "ROOT_EXPANSIONS_WITH_SOME_ACCEPTED_STEPS_BUT_UNRESOLVED"


def run_case(name: str, n: int, k: int) -> dict[str, object]:
    """Observe the actual registered-goal entry point and its screened context."""
    import phase165_r52_r2_search_adapter as search_adapter
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from proof import ProofRule

    measurement = SearchObservation()
    contexts = []
    original = search_adapter.reconstruct_registered_goal

    def spy(*args, **kwargs):
        return instrument_reconstruction(original, args, kwargs, measurement)

    try:
        bridge = build_shared_typed_bridge()
        with patch.object(search_adapter, "reconstruct_registered_goal", spy):
            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge,
                context_sink=contexts.append,
            )
        context = contexts[-1] if contexts else bridge
        direct_sources = sum(
            link.step is not None
            and measurement.root_goal is not None
            and type(link.step.conclusion) is type(measurement.root_goal)
            and link.step.conclusion == measurement.root_goal
            and link.step.rule is ProofRule.GIVEN
            for link in context.proof_links
        )
        accepted_missing_from_result = sum(
            not any(step is found for found in result.proven_steps)
            for step in measurement.accepted_steps
        )
        status = result.status.value
        classification = classify_search(
            status=status,
            reconstruct_calls=measurement.reconstruction_calls,
            root_provider_calls=measurement.root_provider_calls,
            root_option_count=measurement.root_option_count,
            accepted_event_count=measurement.event_counts["proved"],
        )
        record: dict[str, object] = {
            "name": name, "n": n, "k": k, "status": status,
            "result_proof_step_count": len(result.proven_steps),
            "result_open_goal_count": len(result.open_goals),
            "result_open_goal_types": [type(goal).__name__ for goal in result.open_goals],
            "result_diagnostics": list(result.diagnostics),
            "context_capture_count": len(contexts),
            "context_proof_link_count": len(context.proof_links),
            "context_given_link_count": sum(
                link.step is not None and link.step.rule is ProofRule.GIVEN
                for link in context.proof_links
            ),
            "direct_root_given_sources": direct_sources,
            "reconstruction_calls": measurement.reconstruction_calls,
            "lookup_modes": measurement.lookup_modes,
            "root_goal_type": type(measurement.root_goal).__name__
                if measurement.root_goal is not None else None,
            "root_goal": excerpt(measurement.root_goal)
                if measurement.root_goal is not None else None,
            "root_provider_calls": measurement.root_provider_calls,
            "root_expansion_count": measurement.root_option_count,
            "root_expansion_rules": measurement.root_rule_names,
            "total_provider_calls": measurement.expansion_calls,
            "total_expansion_options": measurement.expansion_options,
            "proved_event_count": measurement.event_counts["proved"],
            "unresolved_event_count": measurement.event_counts["unresolved"],
            "accepted_events_not_in_result": accepted_missing_from_result,
            "first_events": measurement.logged_events,
            "first_expansions": measurement.logged_expansions,
            "no_option_goals": [excerpt(goal) for goal in measurement.no_option_targets[:30]],
            "unresolved_goals": [excerpt(goal) for goal in measurement.unresolved_targets[:30]],
            "classification": classification,
            "capture_error": None,
        }
        print(
            name, "status", status,
            "result_steps", len(result.proven_steps),
            "proved_events", measurement.event_counts["proved"],
            "root_rules", measurement.root_option_count,
            "expansion_calls", measurement.expansion_calls,
            "unresolved_events", measurement.event_counts["unresolved"],
            "classification", classification,
        )
        return record
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        print(name, "CAPTURE_ERROR", message)
        return {"name": name, "n": n, "k": k, "capture_error": message}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [run_case(name, n, k) for name, n, k in CASES]
    hashes = {
        filename: hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
        for filename in SOURCES
    }
    report = {
        "phase": "168 R3-41G",
        "mode": "READ_ONLY_ACTUAL_SEARCH_ZERO_STEP_DIAGNOSTICS",
        "cases": cases,
        "source_sha256": hashes,
        "capture_errors": sum(c.get("capture_error") is not None for c in cases),
        "full_pytest_run": False,
        "production_code_modified": False,
        "cautions": [
            "No proof or reference source is added or removed by the instrumentation.",
            "The trace uses accepted-proof and unresolved callbacks of the existing engine.",
            "A goal with zero derivations may still have backward expansion candidates.",
            "The renderer cannot show ProofSteps absent from PartialProofResult.",
            "The audit is a sample, not an exhaustive 112-group survey.",
        ],
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 168 R3-41G — 実探索での証明 Step 0件の原因監査", "",
        "読み取り専用。登録済み命題・推論・ProofStep を変更せず観測する。", "",
        "| 対象 | 状態 | 探索 Step | 採用イベント | 根の展開候補 | 展開呼出 | 未解決イベント | 分類 |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for c in cases:
        if c["capture_error"] is not None:
            lines.append(f'| {c["name"]} | 取得失敗 | - | - | - | - | - | {c["capture_error"]} |')
            continue
        lines.append(
            f'| {c["name"]} | {c["status"]} | {c["result_proof_step_count"]} | '
            f'{c["proved_event_count"]} | {c["root_expansion_count"]} | '
            f'{c["total_provider_calls"]} | {c["unresolved_event_count"]} | '
            f'{c["classification"]} |'
        )
    lines.extend((
        "", "## 判断の境界", "",
        "- 完成例と未完成例で、探索候補と採用済み ProofStep の違いを調べる。",
        "- 探索候補が存在することは、その前提の証明を意味しない。",
        "- result.proven_steps にない証明を Renderer へ補充しない。",
        "- Reference の欠落を証明できるのは、実際に引用付き ProofStep が存在する場合に限る。",
        "- 詳細は audit.json の root_expansion_rules、first_expansions、unresolved_goals を確認する。",
        "- 全体 pytest は Phase 終了時まで実施しない。", "",
    ))
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
        for filename in ("audit.json", "audit.md"):
            archive.write(OUTPUT / filename, arcname=filename)
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)
    print("ACTUAL_SEARCH_SAMPLE", len(cases),
          "CAPTURE_ERRORS", report["capture_errors"])
    print("IMPLEMENTATION_UNCHANGED; full pytest NOT run")
    if report["capture_errors"]:
        raise SystemExit("R3-41G capture failure(s); inspect audit.json")


if __name__ == "__main__":
    main()
