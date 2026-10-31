"""Phase 171 R20R10: read-only tracing of canonical public proof search.

No ProofStep is supplied to the search; an observer wraps, but does not
replace, the canonical recursion. Diagnostic files are outside the repository.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Callable

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
REVIEWED_BLOBS = {
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "cd85ba1e645c1ff9e10e834e74e99437b9988172",
    "phase171_r2j_r4_r3_double_image_bridge/source.py": "1622c073c18e0267c64322d99dce4d36d7ed7507",
    "phase171_r2j_r4_r7_nonzero_nu_order/source.py": "5862ffaa1cc4a6c1046bc153eb8893a75ced3e7a",
    "phase171_r2j_r4_r9_r7_public_cyclic_root/source.py": "45c61377773c098b3e450c83d1b736dab26037de",
    "phase171_r2j_r4_r9_r8_public_cardinality/source.py": "679e871a3fc4a554f55d900621d3849b92645e9e",
    "phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py": "bd9f28e6ccd93b343bc6124779e1b0fe08f8795b",
}
BASELINE_RELATIVE = Path(
    "phase171_r20r9_public_cited_double_image/output/"
    "20261031_022442_237785/audit.json"
)
TRACE_LIMIT = 6000
REPR_LIMIT = 1800


def git_blob_sha(data: bytes) -> str:
    """Compute the Git blob object ID of complete file bytes."""
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def reviewed_blob_matches(data: bytes, expected: str) -> bool:
    """Accept only a reviewed blob, allowing changes of newline convention."""
    lf = data.replace(b"\r\n", b"\n")
    return expected in {
        git_blob_sha(data),
        git_blob_sha(lf),
        git_blob_sha(lf.replace(b"\n", b"\r\n")),
    }


def read_only_git(*args: str) -> str:
    if args not in {
        ("rev-parse", "HEAD"),
        ("branch", "--show-current"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only reviewed read-only Git commands are permitted")
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True,
        text=True, check=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def preflight() -> dict[str, Any]:
    branch = read_only_git("branch", "--show-current")
    head = read_only_git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("read-only audit requires develop branch; no branch is changed")
    guarded = {}
    for relative, expected in REVIEWED_BLOBS.items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("reviewed production file missing: " + relative)
        data = path.read_bytes()
        if not reviewed_blob_matches(data, expected):
            raise RuntimeError(
                "reviewed content mismatch: " + relative +
                " (HEAD alone is not sufficient; no changes were made)"
            )
        guarded[relative] = expected
    return {
        "branch": branch,
        "head": head,
        "reviewed_source_blob_guards": guarded,
        "tracked_status_before": read_only_git(
            "status", "--porcelain", "--untracked-files=no"
        ),
    }


def short(value: object, limit: int = REPR_LIMIT) -> str:
    value_repr = repr(value)
    return value_repr if len(value_repr) <= limit else value_repr[:limit] + "<TRUNCATED>"


def describe(value: object) -> dict[str, str]:
    return {"type": type(value).__name__, "repr": short(value)}


def distinct_goals(goals: list[object]) -> list[object]:
    result = []
    for goal in goals:
        if not any(type(goal) is type(other) and goal == other for other in result):
            result.append(goal)
    return result


class PublicTrace:
    """Capture live canonical calls without fabricating or accepting proof steps."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.dropped_events = 0
        self.query_roots: list[object] = []
        self.expanded: list[tuple[object, tuple[object, ...]]] = []
        self.proved: list[object] = []
        self.unresolved: list[object] = []
        self.contexts: list[object] = []
        self.sequence = 0

    def add(self, kind: str, goal: object, **extras: Any) -> None:
        self.sequence += 1
        if len(self.events) < TRACE_LIMIT:
            self.events.append({
                "index": self.sequence,
                "kind": kind,
                "goal": describe(goal),
                **extras,
            })
        else:
            self.dropped_events += 1

    def context_sink(self, bridge: object) -> None:
        self.contexts.append(bridge)

    def traced_reconstruct(
        self, canonical: Callable[..., object], goal: object, bridge: object,
        citing_assertion_id: str, expansion_provider: Callable[..., object],
        **kwargs: Any,
    ) -> object:
        """Delegate to the original recursion with the same args and returns."""
        self.query_roots.append(goal)
        self.add("search_root", goal, citing_id=citing_assertion_id,
                 lookup_mode=kwargs.get("lookup_mode", "legacy"))
        previous_observer = kwargs.get("progress_observer")

        def observe(kind: str, observed_goal: object, step: object) -> None:
            if kind == "proved":
                self.proved.append(observed_goal)
            elif kind == "unresolved":
                self.unresolved.append(observed_goal)
            self.add(kind, observed_goal, proof_rule=(
                getattr(getattr(step, "rule", None), "name", None)
                if step is not None else None
            ))
            if previous_observer is not None:
                previous_observer(kind, observed_goal, step)

        def expand(observed_goal: object) -> object:
            options = expansion_provider(observed_goal)
            if isinstance(options, tuple):
                self.expanded.append((observed_goal, options))
                items = [
                    {
                        "rule": getattr(option.rule, "name", type(option.rule).__name__),
                        "subgoals": [describe(child) for child in option.subgoals],
                    }
                    for option in options[:16]
                ]
                self.add("expand", observed_goal, candidate_count=len(options),
                         candidates=items, candidates_truncated=max(0, len(options) - 16))
            else:
                self.add("invalid_expansion", observed_goal)
            return options

        kwargs["progress_observer"] = observe
        return canonical(goal, bridge, citing_assertion_id, expand, **kwargs)

    def last_options_for(self, goal: object) -> tuple[object, ...] | None:
        for searched, options in reversed(self.expanded):
            if type(searched) is type(goal) and searched == goal:
                return options
        return None

    def has(self, category: str, goal: object) -> bool:
        return any(type(old) is type(goal) and old == goal
                   for old in getattr(self, category))

    def unresolved_summary(self) -> list[dict[str, Any]]:
        result = []
        for goal in distinct_goals(self.unresolved):
            options = self.last_options_for(goal)
            result.append({
                "goal": describe(goal),
                "proved_later": self.has("proved", goal),
                "candidate_count_at_last_expansion": len(options) if options is not None else None,
                "classification": (
                    "NO_BACKWARD_PROPOSAL" if options == () else
                    "PREMISE_OR_INFERENCE_NOT_COMPLETED" if options is not None else
                    "UNRESOLVED_WITHOUT_EXPANSION"
                ),
                "candidate_rules": [getattr(o.rule, "name", "unknown") for o in options[:12]]
                if options is not None else [],
                "premises": [
                    {
                        "rule": getattr(o.rule, "name", "unknown"),
                        "subgoals": [
                            {**describe(subgoal), "proved_in_public_search": self.has("proved", subgoal)}
                            for subgoal in o.subgoals
                        ],
                    }
                    for o in options[:8]
                ] if options is not None else [],
            })
        return result


def compare_reference_proof(trace: PublicTrace, goal: object) -> dict[str, Any]:
    """Inspect old certified steps only after public search, never import them."""
    from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
    from proof import ProofRule

    root, ancestors, original = build_cyclic_pi63_proof()
    if root.conclusion != goal or root.rule is not ProofRule.INFERENCE:
        raise RuntimeError("R4-R8 reference goal is inconsistent with public group target")
    if original.get("new_given_added") != 0:
        raise RuntimeError("R4-R8 reference reports introduced mathematical GIVEN")
    details = []
    for step in ancestors:
        if step.rule is not ProofRule.INFERENCE:
            continue
        current = step.conclusion
        options = trace.last_options_for(current)
        expected_premises = tuple(parent.conclusion for parent in step.premises)
        matching = [
            option for option in options or ()
            if option.subgoals == expected_premises
            and getattr(option.rule, "name", None) == getattr(step.inference_rule, "name", None)
        ]
        details.append({
            "goal": describe(current),
            "rule": getattr(step.inference_rule, "name", None),
            "reference_premises": [describe(x) for x in expected_premises],
            "public_goal_expanded": options is not None,
            "matching_public_proposal": bool(matching),
            "public_accepted_proof": trace.has("proved", current),
            "public_reported_unresolved": trace.has("unresolved", current),
        })
    return {
        "reference_root_matches_public_goal": True,
        "reference_inference_count": len(details),
        "reference_new_given_added": 0,
        "inferences": details,
    }


def audit_public() -> tuple[dict[str, Any], PublicTrace]:
    """Run the original public entry point, wrapping instrumentation only."""
    import phase165_r52_r2_search_adapter as adapter
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context

    screened, goal, _ = _screened_context()
    trace = PublicTrace()
    canonical = adapter.reconstruct_registered_goal

    def wrapper(goal, bridge, citing_assertion_id, expansion_provider, **kwargs):
        return trace.traced_reconstruct(
            canonical, goal, bridge, citing_assertion_id, expansion_provider,
            **kwargs,
        )

    adapter.reconstruct_registered_goal = wrapper
    try:
        public = search_group_from_registered_goal(
            n=3, k=3, bridge=build_shared_typed_bridge(), goal=goal,
            context_sink=trace.context_sink,
        )
    finally:
        adapter.reconstruct_registered_goal = canonical

    if not trace.query_roots:
        raise RuntimeError("no canonical search was observed; instrumentation path changed")
    target_contexts = [
        bridge for bridge in trace.contexts
        if any(link.step is not None for link in bridge.proof_links)
    ]
    source_claims = []
    if target_contexts:
        from proof import ProofRule
        from unified_statement_registry import AssertionOrigin
        context = target_contexts[-1]
        for link in context.proof_links:
            assertion = context.registry.assertion(link.assertion_id)
            if (
                link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == link.step.conclusion
            ):
                source_claims.append({
                    "assertion_id": link.assertion_id,
                    "conclusion_type": type(link.step.conclusion).__name__,
                    "conclusion": short(link.step.conclusion, 800),
                })
    result = {
        "public_status": public.status.value,
        "public_complete": (
            public.status.value == "complete"
            and public.conclusion == goal and not public.open_goals
        ),
        "public_goal": describe(goal),
        "public_open_goals": [describe(item) for item in public.open_goals],
        "public_diagnostics": list(public.diagnostics),
        "public_accepted_steps": len(public.proven_steps),
        "search_queries_observed": len(trace.query_roots),
        "traced_events": trace.sequence,
        "events_retained": len(trace.events),
        "events_dropped": trace.dropped_events,
        "recorded_provider_expansions": len(trace.expanded),
        "recorded_proved_events": len(trace.proved),
        "recorded_unresolved_events": len(trace.unresolved),
        "event_kinds": dict(Counter(e["kind"] for e in trace.events)),
        "unresolved_details": trace.unresolved_summary(),
        "screened_fixed_given_count": len(source_claims),
        "screened_fixed_given_sources": source_claims,
        "trace_events": trace.events,
    }
    return result, trace


def output_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    return Path(base) / "EHPProofTracerRecovery" / "phase171_r20r10_read_only"


def run(*, dry_run: bool = False, skip_reference_comparison: bool = False) -> dict[str, Any]:
    before = preflight()
    print("PHASE171_R20R10_BRANCH=" + before["branch"], flush=True)
    print("PHASE171_R20R10_HEAD=" + before["head"], flush=True)
    print("PHASE171_R20R10_SOURCE_CONTENT_GUARD=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20R10_DRY_RUN=PASS", flush=True)
        return before
    baseline_file = ROOT / BASELINE_RELATIVE
    baseline = None
    if baseline_file.is_file():
        baseline = json.loads(baseline_file.read_text(encoding="utf-8-sig"))
    public, trace = audit_public()
    reference = (
        None if skip_reference_comparison
        else compare_reference_proof(trace, goal_from_result(public, trace))
    )
    after_status = read_only_git("status", "--porcelain", "--untracked-files=no")
    after_head = read_only_git("rev-parse", "HEAD")
    if after_status != before["tracked_status_before"] or after_head != before["head"]:
        raise RuntimeError("the repository tracked status or HEAD changed during audit")
    report = {
        "phase": "171-R20R10",
        "mode": "READ_ONLY_PUBLIC_RECURSION_FRONTIER_AUDIT",
        "git_head": before["head"],
        "source_content_guard": "PASS",
        "baseline_r20r9": {
            "available": baseline is not None,
            "public_status": baseline.get("public_status") if baseline else None,
            "public_open_goals": baseline.get("public_open_goals") if baseline else None,
            "public_diagnostics": baseline.get("public_diagnostics") if baseline else None,
        },
        "public": public,
        "reference_comparison": reference,
        "new_given_added_by_auditor": 0,
        "completed_proofs_imported_into_public_search": False,
        "production_files_modified": False,
        "tracked_worktree_unchanged": True,
        "full_pytest": False,
        "web_verified": False,
    }
    destination_folder = output_dir() / datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S_%f"
    )
    destination_folder.mkdir(parents=True, exist_ok=False)
    destination = destination_folder / "audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R10_PUBLIC_STATUS=" + public["public_status"], flush=True)
    print("PHASE171_R20R10_PUBLIC_COMPLETE=" + str(public["public_complete"]), flush=True)
    print("PHASE171_R20R10_UNRESOLVED=" + str(len(public["unresolved_details"])), flush=True)
    print("PHASE171_R20R10_TRACE_EVENTS=" + str(public["traced_events"]), flush=True)
    print("PHASE171_R20R10_REPORT=" + str(destination), flush=True)
    print("PHASE171_R20R10_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R10_COMPLETED_PROOFS_IMPORTED=False", flush=True)
    print("PHASE171_R20R10_RESULT=PASS_READ_ONLY_AUDIT", flush=True)
    return report


def goal_from_result(public: dict[str, Any], trace: PublicTrace) -> object:
    """Retrieve the actual public target without reconstructing a proof."""
    for query in trace.query_roots:
        if describe(query) == public["public_goal"]:
            return query
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    return _screened_context()[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-reference-comparison", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run, skip_reference_comparison=args.skip_reference_comparison)


if __name__ == "__main__":
    main()
