"""Read-only public EHP search audit after Phase 171 R20R2.

A goal proposal is not evidence. Each goal is passed independently to the
canonical recursive engine; no completed historical proof is injected.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time
import traceback

from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context, _available
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from phase171_r2j_r4_r9_r8_public_cardinality.source import (
    _cited_finite_group_candidates,
    expand_cited_ehp_middle_cardinality,
)
from proof import ProofRule, ProofStep

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
# Reviewed GitHub content blobs (not commit/HEAD IDs).
# Source: akebono03/ehp-proof-tracer @ 788261264e63d202b9e9bfe819212f12e0d0134e.
REVIEWED_SOURCE_BLOBS = {
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r9_shared_math.py": "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}


def git(*args: str) -> str:
    """Restrict calls to read-only repository observations."""
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in permitted:
        raise ValueError("only read-only git commands are allowed")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def preflight() -> dict:
    """Check the reviewed search/provider bytes, regardless of newer commit ID.

    Use Git's read-only hash-object with the path-specific clean filters so
    Windows checkout line endings do not trigger false source mismatches.
    Never repair or reset the worktree. A source mismatch is fatal.
    """
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R20R4 requires develop; no branch will be changed")

    observed_blobs: dict[str, str] = {}
    for relative_path, reviewed_blob in REVIEWED_SOURCE_BLOBS.items():
        path = ROOT / relative_path
        if not path.is_file():
            raise RuntimeError("required production file is missing: " + relative_path)
        command = [
            "git", "hash-object", "--path=" + relative_path,
            relative_path,
        ]
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, check=True,
        )
        observed_blob = result.stdout.strip()
        observed_blobs[relative_path] = observed_blob
        if observed_blob != reviewed_blob:
            raise RuntimeError(
                "production source differs from reviewed GitHub blob: "
                + relative_path + " expected=" + reviewed_blob
                + " actual=" + observed_blob
                + "; no files modified"
            )

    source = (ROOT / "phase165_r3_recursive_search.py").read_text(encoding="utf-8")
    if (
        "def reconstruct_registered_goal(" not in source
        or "first accepted proof wins" not in source
        or "ambiguous registered direct references" not in source
        or "expected a verified registered derivation" not in source
    ):
        raise RuntimeError("reviewed R20R2 first-successful proof search is unavailable")

    return {
        "branch": branch,
        "head": head,
        "reviewed_source_blobs": observed_blobs,
        "tracked_before": git("status", "--porcelain", "--untracked-files=no"),
    }

def proof_ancestry(root: ProofStep, bridge) -> dict:
    """Summarize, but never repair, a proof tree returned by canonical search."""
    visited: set[int] = set()
    active: set[int] = set()
    nodes: list[ProofStep] = []

    def walk(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise ValueError("non-ProofStep premise")
        identity = id(step)
        if identity in active:
            raise ValueError("cyclic ProofStep ancestry")
        if identity in visited:
            return
        active.add(identity)
        if step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):
            raise ValueError("unexpected proof rule in ancestry")
        if step.rule is ProofRule.GIVEN and step.premises:
            raise ValueError("GIVEN leaf has premises")
        if step.rule is ProofRule.INFERENCE and step.inference_rule is None:
            raise ValueError("INFERENCE has no inference rule")
        for premise in step.premises:
            walk(premise)
        active.remove(identity)
        visited.add(identity)
        nodes.append(step)

    walk(root)
    leaves = [node for node in nodes if node.rule is ProofRule.GIVEN]
    fixed_link_ids = [
        link.assertion_id
        for leaf in leaves
        for link in bridge.proof_links
        if link.step is leaf
    ]
    linked_leaf_id_set = {id(link.step) for link in bridge.proof_links if link.step is not None}
    return {
        "total_nodes": len(nodes),
        "inferences": sum(node.rule is ProofRule.INFERENCE for node in nodes),
        "given_leaves": len(leaves),
        "source_linked_given_assertions": sorted(set(fixed_link_ids)),
        "unlinked_existing_given_leaves": sum(id(leaf) not in linked_leaf_id_set for leaf in leaves),
        "inference_rule_names": dict(Counter(
            node.inference_rule.name for node in nodes
            if node.rule is ProofRule.INFERENCE
        )),
    }


def audit_obligation(label: str, goal: object | None, bridge, citing: str, provider) -> dict:
    """Make one independent attempt without adding any assumed premises."""
    if goal is None:
        return {"stage": label, "status": "GOAL_NOT_UNIQUELY_IDENTIFIED"}
    events: list[tuple[str, str]] = []

    def observer(kind: str, observed: object, step: ProofStep | None) -> None:
        events.append((kind, type(observed).__name__))

    start = time.perf_counter()
    result = {"stage": label, "goal": repr(goal)[:2000]}
    try:
        step = reconstruct_registered_goal(
            goal, bridge, citing, provider,
            lookup_mode="typed_reference_publication",
            progress_observer=observer,
            completed_internal_proofs=(),
        )
        if type(step.conclusion) is not type(goal) or step.conclusion != goal:
            raise ValueError("canonical search returned a mismatched conclusion")
        result.update({
            "status": "PROVED",
            "root_rule": step.rule.value,
            "root_inference": step.inference_rule.name if step.inference_rule is not None else None,
            "ancestry": proof_ancestry(step, bridge),
        })
    except RegisteredGoalUnresolved as exc:
        result.update({"status": "UNRESOLVED", "diagnostic": str(exc)[:2000]})
    except Exception as exc:
        result.update({
            "status": "ERROR",
            "diagnostic": f"{type(exc).__name__}: {exc}"[:2000],
            "traceback": traceback.format_exc()[-5000:],
        })
    result["observed_proved_events"] = sum(kind == "proved" for kind, _ in events)
    result["observed_unresolved_events"] = sum(kind == "unresolved" for kind, _ in events)
    result["elapsed_seconds"] = round(time.perf_counter() - start, 3)
    return result


def audit_public_goal(target: object) -> tuple[dict, str | None]:
    """Run the real public entry without reusing preceding audit proofs."""
    start = time.perf_counter()
    try:
        public = search_group_from_registered_goal(
            n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
        )
        complete = (
            public.status is ProofSearchStatus.COMPLETE
            and public.conclusion == target
            and not public.open_goals
        )
        result = {
            "stage": "public_group_search",
            "status": public.status.value,
            "complete": complete,
            "proven_steps": len(public.proven_steps),
            "open_goals": [repr(item)[:1600] for item in public.open_goals[:20]],
            "diagnostics": list(public.diagnostics[:20]),
            "structure_status": public.structure_status.value,
            "web_verified": False,
        }
        rendered = None
        result["narrative_rendered"] = False
        if complete:
            try:
                rendered = render_partial_proof_markdown(public)
                result["narrative_rendered"] = bool(rendered.strip())
                result["narrative_characters"] = len(rendered)
            except Exception as exc:
                result["narrative_error"] = f"{type(exc).__name__}: {exc}"[:2000]
        return result | {"elapsed_seconds": round(time.perf_counter() - start, 3)}, rendered
    except Exception as exc:
        return {
            "stage": "public_group_search",
            "status": "ERROR",
            "complete": False,
            "web_verified": False,
            "diagnostic": f"{type(exc).__name__}: {exc}"[:2000],
            "traceback": traceback.format_exc()[-5000:],
            "elapsed_seconds": round(time.perf_counter() - start, 3),
        }, None


def run_audit(*, right_only: bool) -> tuple[dict, str | None]:
    """Trace right end, cardinality, element order, cyclicity, then public result."""
    screened, target, citing = _screened_context()
    if target.lhs != TodaPrimaryGroup(6, 3) or target.rhs.order != 4:
        raise RuntimeError("screened public target is not the expected 2-primary pi_6^3 goal")
    available = _available(screened)
    provider = shared_expansion_provider(screened, proof_target=target)
    right_candidates = _cited_finite_group_candidates(TodaPrimaryGroup(6, 5), available)
    right = right_candidates[0] if len(right_candidates) == 1 else None
    report = {
        "phase": "171-R20R4",
        "mode": "AUDIT_ONLY_FIRST_SUCCESSFUL_PUBLIC_FRONTIER",
        "target": repr(target),
        "screened_reference_count": len(screened.proof_links),
        "citing_assertion_id": citing,
        "right_end_candidate_count": len(right_candidates),
        "right_end_candidates": [repr(item)[:1600] for item in right_candidates[:5]],
        "new_given_added": 0,
        "completed_proof_imported": False,
        "production_changes": 0,
        "full_pytest": False,
        "stages": [],
    }

    right_result = audit_obligation("pi_6^5_right_end", right, screened, citing, provider)
    report["stages"].append(right_result)
    print("PHASE171_R20R4_RIGHT_END=" + right_result["status"], flush=True)
    if right_only:
        report["public_web_verified"] = False
        return report, None

    root_routes = expand_cited_double_cyclic_root(target, available)
    report["screened_cyclic_root_route_count"] = len(root_routes)
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    card_routes = expand_cited_ehp_middle_cardinality(cardinality, available)
    report["screened_cardinality_route_count"] = len(card_routes)
    card_result = audit_obligation(
        "pi_6^3_cardinality_four", cardinality, screened, citing, provider,
    )
    report["stages"].append(card_result)
    print("PHASE171_R20R4_CARDINALITY_FOUR=" + card_result["status"], flush=True)

    element_order = root_routes[0].subgoals[1] if len(root_routes) == 1 else None
    order_result = audit_obligation(
        "nu_prime_order_four", element_order, screened, citing, provider,
    )
    report["stages"].append(order_result)
    print("PHASE171_R20R4_NU_ORDER_FOUR=" + order_result["status"], flush=True)

    cyclic_goal = CyclicStructureStatement(target.lhs, target.rhs.generator, 4)
    structure_result = audit_obligation(
        "pi_6^3_cyclic_structure", cyclic_goal, screened, citing, provider,
    )
    report["stages"].append(structure_result)
    print("PHASE171_R20R4_CYCLIC_STRUCTURE=" + structure_result["status"], flush=True)

    public_result, markdown = audit_public_goal(target)
    report["stages"].append(public_result)
    report["public_complete"] = public_result["complete"]
    report["public_web_verified"] = False
    print("PHASE171_R20R4_PUBLIC_STATUS=" + public_result["status"], flush=True)
    print("PHASE171_R20R4_PUBLIC_COMPLETE=" + str(public_result["complete"]), flush=True)
    return report, markdown


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--right-only", action="store_true")
    args = parser.parse_args()
    state = preflight()
    print("PHASE171_R20R4_BRANCH=" + state["branch"], flush=True)
    print("PHASE171_R20R4_HEAD=" + state["head"], flush=True)
    print("PHASE171_R20R4_SEARCH_PATCH=FIRST_SUCCESSFUL", flush=True)
    print("PHASE171_R20R4_SOURCE_CHANGES=0", flush=True)
    if args.dry_run:
        print("PHASE171_R20R4_RESULT=PASS_DRY_RUN", flush=True)
        return

    report, rendered = run_audit(right_only=args.right_only)
    after = git("status", "--porcelain", "--untracked-files=no")
    if after != state["tracked_before"]:
        raise RuntimeError("tracked source changed while conducting read-only audit")
    report["git_head"] = state["head"]
    report["tracked_state_unchanged"] = True
    report["audited_at_utc"] = datetime.now(timezone.utc).isoformat()
    output = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    output.mkdir(parents=True, exist_ok=False)
    destination = output / "audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if rendered is not None:
        (output / "rendered_proof.md").write_text(rendered, encoding="utf-8")
    print("PHASE171_R20R4_REPORT=" + str(destination), flush=True)
    print("PHASE171_R20R4_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R4_COMPLETED_PROOFS_IMPORTED=False", flush=True)
    print("PHASE171_R20R4_TRACKED_STATE_UNCHANGED=PASS", flush=True)
    print("PHASE171_R20R4_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R20R4_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
