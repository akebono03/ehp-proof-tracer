"""Phase 169 R2: non-mutating diagnostic of the live pi_5^3 proof frontier.

Uses the canonical search, typed registry, and existing expansion providers.
It never installs new rules, gives unproved facts, or modifies application files.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import sys
import traceback

PACKAGE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_DIR.parent
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    shared_expansion_provider,
)
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
from phase165_r57_r16_web_proof_order import REVIEWED_PROOF_TARGET_ORDER
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
from proof import ProofRule

REVIEWED_GIT_HEAD = "28bac5f61267b4381aaeb4fd5a623623bc5f18ce"


def describe_expansion(expansion, position: int) -> dict[str, object]:
    return {
        "position": position,
        "rule_name": getattr(expansion.rule, "name", repr(expansion.rule)),
        "rule_type": type(expansion.rule).__name__,
        "subgoal_count": len(expansion.subgoals),
        "subgoals": [
            {"type": type(item).__name__, "repr": repr(item)}
            for item in expansion.subgoals
        ],
    }


def describe_linked_leaves(bridge, target_goal, base_goal, citing_id):
    """Report only actual screened fixed GIVEN links (not registry-only goals)."""
    result = []
    counts = Counter()
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        entry = bridge.registry.assertion(link.assertion_id)
        if step.conclusion != entry.content:
            continue
        label = type(entry.content).__name__
        counts[label] += 1
        equals_base = entry.content == base_goal
        equals_target = entry.content == target_goal
        interesting_type = any(
            token in label.lower()
            for token in ("isomorphism", "generatorimage", "suspension", "toda45")
        )
        if not (equals_base or equals_target or interesting_type):
            continue
        eligible = None
        if citing_id is not None:
            try:
                eligible = bool(precedes_citing_assertion(bridge, entry.assertion_id, citing_id))
            except (ValueError, TypeError, KeyError) as error:
                eligible = f"UNRESOLVED:{type(error).__name__}"
        result.append({
            "assertion_id": entry.assertion_id,
            "reference_id": entry.reference_id,
            "type": label,
            "is_exact_pi4_2_group_goal": equals_base,
            "is_exact_pi5_3_goal": equals_target,
            "precedes_citing_assertion": eligible,
            "conclusion_repr": repr(entry.content),
        })
    return {"given_type_counts": dict(counts), "relevant_leaves": result}


def load_prior_baseline():
    p = REPOSITORY_ROOT / "phase169_r1_two_stem_baseline_audit" / "output" / "two_stem_baseline.json"
    if not p.is_file():
        return {"available": False, "expected_path": str(p)}
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    rows = data.get("results", [])
    items = []
    for row in rows:
        items.append({
            "target": row.get("target"),
            "status": row.get("status"),
            "step_count": row.get("proven_step_count"),
            "open_goals": row.get("open_goals", []),
            "diagnostics": row.get("diagnostics", []),
            "candidates": row.get("candidates", []),
            "publication_order": row.get("publication_order", {}),
        })
    return {"available": True, "path": str(p), "groups": items}


def audit():
    prior = load_prior_baseline()
    bridge = build_shared_typed_bridge()
    source = registered_group_goal_candidates(bridge, n=2, k=2)
    target = registered_group_goal_candidates(bridge, n=3, k=2)
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    source_result = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    if len(target) != 1:
        return {
            "prior_baseline": prior,
            "pi4_candidate_count": len(source),
            "pi5_candidate_count": len(target),
            "status": result.status.value,
            "diagnostics": list(result.diagnostics),
            "audit_status": "STOP_NONUNIQUE_GOAL",
        }
    if not contexts:
        return {
            "prior_baseline": prior,
            "pi4_candidate_count": len(source),
            "pi5_candidate_count": len(target),
            "status": result.status.value,
            "diagnostics": list(result.diagnostics),
            "audit_status": "STOP_NO_SCREENED_CONTEXT",
        }

    screened = contexts[-1]
    goal = target[0]
    cited = resolve_specialized_goal_citing_id(bridge, goal)
    provider = shared_expansion_provider(screened, proof_target=goal)
    frontier = [goal]
    for item in result.open_goals:
        if not any(type(old) is type(item) and old == item for old in frontier):
            frontier.append(item)

    per_goal = []
    for item in frontier:
        expansions = provider(item)
        per_goal.append({
            "type": type(item).__name__,
            "repr": repr(item),
            "backward_candidate_count": len(expansions),
            "candidate_rules": dict(Counter(
                getattr(expansion.rule, "name", repr(expansion.rule))
                for expansion in expansions
            )),
            "candidate_details": [
                describe_expansion(expansion, index)
                for index, expansion in enumerate(expansions, start=1)
            ],
        })

    pi4_relation = source[0] if len(source) == 1 else None
    if source_result.status is ProofSearchStatus.COMPLETE:
        pi4_relation = source_result.conclusion
    prior_rules = (
        "toda_prop53_n3_eta_square_suspension_bridge_inference_rule",
        "toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule",
    )
    return {
        "audit_status": "OBSERVED",
        "prior_baseline": prior,
        "goal_pi4_2": [repr(item) for item in source],
        "goal_pi5_3": [repr(item) for item in target],
        "pi4_current_search_status": source_result.status.value,
        "pi4_current_steps": len(source_result.proven_steps),
        "pi4_current_conclusion": repr(source_result.conclusion),
        "pi5_current_search_status": result.status.value,
        "pi5_current_steps": len(result.proven_steps),
        "pi5_diagnostics": list(result.diagnostics),
        "pi5_open_goals": [repr(item) for item in result.open_goals],
        "citing_assertion_id": cited,
        "current_default_rule_modules": list(DEFAULT_RULE_MODULES),
        "contains_toda_rules_directly": "toda_rules" in DEFAULT_RULE_MODULES,
        "historical_phase162_factories": list(prior_rules),
        "reviewed_proof_targets": [list(pair) for pair in REVIEWED_PROOF_TARGET_ORDER],
        "pi4_registered_as_ordered_prior": (2, 2) in REVIEWED_PROOF_TARGET_ORDER,
        "pi5_target_has_reviewed_catalog": (3, 2) in REVIEWED_PROOF_TARGET_ORDER,
        "toda45_stable_range_for_pi4_n2_stem2": 2 >= 2 + 2,
        "toda45_stable_range_for_pi5_n3_stem2": 3 >= 2 + 2,
        "linked_reference_audit": describe_linked_leaves(
            screened, goal, pi4_relation, cited,
        ),
        "frontier_expansions": per_goal,
    }


def render_report(data: dict[str, object]) -> str:
    lines = [
        "Phase 169 R2 — pi_5^3 typed backward gap audit",
        "AUDIT_ONLY / NO RULE OR PROOF MODIFICATION",
        f"REVIEWED_GIT_HEAD={REVIEWED_GIT_HEAD}",
        f"AUDIT_STATUS={data.get('audit_status')}",
        "",
    ]
    baseline = data.get("prior_baseline", {})
    lines.append(f"R1_BASELINE_AVAILABLE={baseline.get('available')}")
    for group in baseline.get("groups", []):
        lines.extend([
            f"R1_TARGET={group.get('target')}",
            f"  STATUS={group.get('status')} STEPS={group.get('step_count')}",
            "  R1_OPEN_GOALS:",
        ])
        lines.extend(f"    {item}" for item in group.get("open_goals", []))
        lines.extend(f"  DIAGNOSTIC: {text}" for text in group.get("diagnostics", []))
    lines.extend([
        "",
        f"PI4_STATUS={data.get('pi4_current_search_status')}",
        f"PI4_STEPS={data.get('pi4_current_steps')}",
        f"PI4_CONCLUSION={data.get('pi4_current_conclusion')}",
        f"PI5_STATUS={data.get('pi5_current_search_status',data.get('status'))}",
        f"PI5_STEPS={data.get('pi5_current_steps')}",
        f"PI5_CITING_ID={data.get('citing_assertion_id')}",
        f"DIRECT_TODA_RULES_DISCOVERY={data.get('contains_toda_rules_directly')}",
        f"REVIEWED_PROOF_TARGETS={data.get('reviewed_proof_targets')}",
        f"PI4_REGISTERED_AS_ORDERED_PRIOR={data.get('pi4_registered_as_ordered_prior')}",
        f"PI5_HAS_REVIEWED_ORDER_CATALOG={data.get('pi5_target_has_reviewed_catalog')}",
        f"TODA45_VALID_PI4_N2_STEM2={data.get('toda45_stable_range_for_pi4_n2_stem2')}",
        f"TODA45_VALID_PI5_N3_STEM2={data.get('toda45_stable_range_for_pi5_n3_stem2')}",
        "",
        "ACTIVE GOAL REPRESENTATIONS",
    ])
    lines.extend(f"  pi4: {value}" for value in data.get("goal_pi4_2", []))
    lines.extend(f"  pi5: {value}" for value in data.get("goal_pi5_3", []))
    lines.extend(["", "SEARCH DIAGNOSTICS"])
    lines.extend(f"  {msg}" for msg in data.get("pi5_diagnostics", data.get("diagnostics", [])))
    lines.extend(["", "SCREENED GIVEN REFERENCE LEAVES"])
    ref = data.get("linked_reference_audit", {})
    lines.append(f"  TYPE_COUNTS={ref.get('given_type_counts')}")
    for leaf in ref.get("relevant_leaves", []):
        lines.extend([
            f"  ASSERTION {leaf['assertion_id']} TYPE={leaf['type']} ELIGIBLE={leaf['precedes_citing_assertion']}",
            f"    MATCH_PI4={leaf['is_exact_pi4_2_group_goal']} MATCH_PI5={leaf['is_exact_pi5_3_goal']}",
            f"    {leaf['conclusion_repr']}",
        ])
    for entry in data.get("frontier_expansions", []):
        lines.extend([
            "",
            f"FRONTIER_GOAL: {entry['type']}: {entry['repr']}",
            f"CANDIDATE_COUNT={entry['backward_candidate_count']}",
            f"CANDIDATE_RULES={entry['candidate_rules']}",
        ])
        for option in entry["candidate_details"]:
            lines.append(f"  RULE {option['position']}: {option['rule_name']}")
            for goal in option["subgoals"]:
                lines.append(f"    {goal['type']}: {goal['repr']}")
    lines.extend([
        "",
        "CAUTION: A registered group Goal is not a mathematical premise.",
        "Only a screened GIVEN, or a correctly derived ProofStep, may be used.",
        "A proposed backward expansion is not a completed proof.",
        "The historical Phase 162 factories are only contextual diagnostics.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    out = PACKAGE_DIR / "output"
    out.mkdir(parents=True, exist_ok=True)
    try:
        result = audit()
    except Exception:
        (out / "audit_error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        print("R2_AUDIT_ERROR: see output/audit_error.txt", flush=True)
        return 2
    (out / "pi53_gap.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out / "pi53_gap.txt").write_text(render_report(result), encoding="utf-8")
    print("R2_AUDIT_STATUS", result.get("audit_status"), flush=True)
    print("PI4_STATUS", result.get("pi4_current_search_status"), flush=True)
    print("PI5_STATUS", result.get("pi5_current_search_status"), flush=True)
    print("PI5_OPEN_GOALS", len(result.get("pi5_open_goals", [])), flush=True)
    print("PI4_PRIOR_REGISTERED", result.get("pi4_registered_as_ordered_prior"), flush=True)
    print("TODA45_PI5_ELIGIBLE", result.get("toda45_stable_range_for_pi5_n3_stem2"), flush=True)
    for index, entry in enumerate(result.get("frontier_expansions", []), start=1):
        print(f"FRONTIER_{index}_CANDIDATES", entry["backward_candidate_count"], flush=True)
        print("  GOAL", entry["repr"], flush=True)
        print("  RULES", entry["candidate_rules"], flush=True)
    print("REPORT", out / "pi53_gap.txt", flush=True)
    return 0 if result.get("audit_status") == "OBSERVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
