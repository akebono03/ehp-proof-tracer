"""Read-only diagnosis of root-search equality symmetry recursion.

The wrapper returns the original provider's candidate tuple unchanged. It
observes the existing canonical resolver's active and solved goals via Python
frames, but never alters the resolver, ProofSteps, rules, or registry.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable
from unittest.mock import patch

import phase165_r52_r9_shared_math as shared_math
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _checked_chain, _screened_context
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import reverse_equality
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    git_read,
    preflight,
)

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "audit.json"
MAX_EVENTS = 120


def same_statement(left: object, right: object) -> bool:
    """Use the same equality convention as the canonical proof search."""
    return type(left) is type(right) and left == right


def goal_role(goal: object, root: object, forward: object, reverse: object) -> str | None:
    """Classify only the three concrete goals under this diagnosis."""
    if same_statement(goal, root):
        return "root"
    if same_statement(goal, forward):
        return "forward"
    if same_statement(goal, reverse):
        return "reverse"
    return None


def resolution_stack_snapshot(
    frame: object,
    root: object,
    forward: object,
    reverse: object,
) -> dict:
    """Read the active resolver stack without modifying any resolver local.

    Only an actual frame from phase165_r3_recursive_search.resolve qualifies;
    unrelated stack frames never receive authority as proof evidence.
    """
    current = frame
    while current is not None:
        code = getattr(current, "f_code", None)
        globals_dict = getattr(current, "f_globals", {})
        if (
            getattr(code, "co_name", None) == "resolve"
            and globals_dict.get("__name__") == "phase165_r3_recursive_search"
        ):
            local = current.f_locals
            active = local.get("active", ())
            solved = local.get("solved", ())
            if not isinstance(active, (tuple, list)) or not isinstance(solved, (tuple, list)):
                raise RuntimeError("unexpected canonical resolver state")
            roles = [goal_role(item, root, forward, reverse) or "other" for item in active]
            solved_goals = [entry[0] for entry in solved if isinstance(entry, tuple) and len(entry) == 2]
            return {
                "resolver_found": True,
                "active_depth": len(active),
                "active_roles": roles,
                "root_active": any(same_statement(item, root) for item in active),
                "forward_active": any(same_statement(item, forward) for item in active),
                "reverse_active": any(same_statement(item, reverse) for item in active),
                "forward_solved": any(same_statement(item, forward) for item in solved_goals),
                "reverse_solved": any(same_statement(item, reverse) for item in solved_goals),
            }
        current = getattr(current, "f_back", None)
    return {
        "resolver_found": False,
        "active_depth": 0,
        "active_roles": [],
        "root_active": False,
        "forward_active": False,
        "reverse_active": False,
        "forward_solved": False,
        "reverse_solved": False,
    }


def classify_trace(public_status: str, events: list[dict]) -> str:
    """Classify observed routing, not mathematical completeness."""
    if public_status == "complete":
        return "ROOT_COMPLETE_REQUIRES_TRUST_BOUNDARY"
    reverses = [item for item in events if item["role"] == "reverse"]
    if not reverses:
        return "REVERSE_NOT_VISITED_IN_PUBLIC_ROOT"
    if any(
        item["stack"]["forward_active"]
        and item["symmetry_exact"] == 1
        and item["routes_total"] == 1
        for item in reverses
    ):
        return "REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD"
    if any(item["symmetry_exact"] == 0 for item in reverses):
        return "REVERSE_ROUTE_MISSING_IN_ROOT_CONTEXT"
    if any(item["routes_total"] > 1 for item in reverses):
        return "MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT"
    return "ROOT_PARTIAL_WITHOUT_OBSERVED_DIRECT_SYMMETRY_CYCLE"


class ProviderFactoryObserver:
    """Wrap only the existing root provider, preserving its exact results."""

    def __init__(
        self,
        factory: Callable,
        root: object,
        forward: object,
        reverse: object,
    ) -> None:
        if not callable(factory):
            raise TypeError("factory must be callable")
        self.factory = factory
        self.root = root
        self.forward = forward
        self.reverse = reverse
        self.root_provider_instances = 0
        self.focus_calls = {"root": 0, "forward": 0, "reverse": 0}
        self.events: list[dict] = []
        self.dropped_events = 0

    def __call__(self, *args, **kwargs):
        provider = self.factory(*args, **kwargs)
        if not callable(provider):
            raise TypeError("shared provider factory returned a noncallable")
        if not same_statement(kwargs.get("proof_target"), self.root):
            return provider
        self.root_provider_instances += 1

        def observed(goal: object):
            role = goal_role(goal, self.root, self.forward, self.reverse)
            if role is None:
                return provider(goal)
            self.focus_calls[role] += 1
            stack = resolution_stack_snapshot(
                sys._getframe(1), self.root, self.forward, self.reverse,
            )
            routes = provider(goal)
            if not isinstance(routes, tuple):
                raise TypeError("provider contract violated")
            if len(self.events) < MAX_EVENTS:
                matching = sum(
                    getattr(item.rule, "name", None) == "equality symmetry"
                    and item.subgoals == (self.forward,)
                    for item in routes
                )
                self.events.append({
                    "role": role,
                    "stack": stack,
                    "routes_total": len(routes),
                    "symmetry_exact": matching,
                    "rules": [str(getattr(item.rule, "name", "<unnamed>")) for item in routes[:15]],
                })
            else:
                self.dropped_events += 1
            return routes

        return observed


def inspect_public_root() -> dict:
    """Observe the authentic public group search through a temporary wrapper."""
    original_bridge = shared_math.build_shared_typed_bridge()
    screened, root, citing = _screened_context()
    chain, _available = _checked_chain(screened, citing)
    forward = chain.alpha_composition
    reverse = reverse_equality(forward)
    if reverse is None:
        raise RuntimeError("R11 has no reverse equality to diagnose")
    observer = ProviderFactoryObserver(
        shared_math.shared_expansion_provider, root, forward, reverse,
    )
    contexts: list[object] = []
    with patch.object(shared_math, "shared_expansion_provider", observer):
        public = search_group_from_registered_goal(
            n=3,
            k=3,
            bridge=original_bridge,
            goal=root,
            context_sink=contexts.append,
        )
    if len(contexts) != 1:
        raise RuntimeError("public search did not expose a unique root context")
    public_chain, _ = _checked_chain(contexts[0], citing)
    if public_chain.alpha_composition != forward:
        raise RuntimeError("public context disagrees with the screened R11 equality")
    first_open = public.open_goals[0] if public.open_goals else None
    return {
        "phase": "171-R2J-R4-R9-R13",
        "mode": "ROOT_STACK_AUDIT_ONLY",
        "root_goal": repr(root),
        "forward_goal": repr(forward),
        "reverse_goal": repr(reverse),
        "public_search_status": public.status.value,
        "public_open_count": len(public.open_goals),
        "public_proven_steps": len(public.proven_steps),
        "first_open_is_reverse": first_open is not None and same_statement(first_open, reverse),
        "public_diagnostics": list(public.diagnostics[:10]),
        "root_provider_instances": observer.root_provider_instances,
        "focus_calls": observer.focus_calls,
        "events": observer.events,
        "dropped_events": observer.dropped_events,
        "classification": classify_trace(public.status.value, observer.events),
        "new_given_added": 0,
        "existing_source_modified": False,
        "completed_proof_replayed": False,
        "full_pytest": False,
        "web_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    pre = preflight()
    print("PHASE171_R13_BRANCH=" + pre["branch"], flush=True)
    print("PHASE171_R13_HEAD=" + pre["head"], flush=True)
    print("PHASE171_R13_R11_BASELINE=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R13_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect_public_root()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked source changed during root audit")
    report["git_head"] = pre["head"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R13_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R13_FIRST_OPEN_IS_REVERSE=" + str(report["first_open_is_reverse"]), flush=True)
    print("PHASE171_R13_FOCUS_CALLS=" + json.dumps(report["focus_calls"], ensure_ascii=False), flush=True)
    print("PHASE171_R13_ROOT_PROVIDER_INSTANCES=" + str(report["root_provider_instances"]), flush=True)
    print("PHASE171_R13_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R13_NEW_GIVEN=0", flush=True)
    print("PHASE171_R13_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R13_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R13_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
