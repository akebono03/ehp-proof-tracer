"""Diagnose actual proof obligations for pi_7^5 without importing a DB Goal as GIVEN."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def diagnostic_attempt(goal, screened, citing: str, provider) -> dict:
    """Independently solve a typed subgoal; never turn it into a new GIVEN."""
    observations = []

    def observe(kind, target, step):
        if kind == "unresolved":
            description = type(target).__name__ + ": " + repr(target)
            if description not in observations:
                observations.append(description)

    try:
        step = reconstruct_registered_goal(
            goal, screened, citing, provider,
            lookup_mode="typed_reference_publication",
            progress_observer=observe,
        )
    except RegisteredGoalUnresolved as error:
        return {
            "proved": False,
            "error": str(error),
            "unresolved": observations[:25],
            "proof_rule": None,
            "steps_in_subtree": 0,
        }
    ancestors = []
    pending = [step]
    seen = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        ancestors.append(current)
        pending.extend(current.premises)
    return {
        "proved": step.conclusion == goal,
        "error": None,
        "unresolved": observations[:25],
        "proof_rule": step.rule.value,
        "steps_in_subtree": len(ancestors),
        "given_leaf_types": sorted(set(
            type(item.conclusion).__name__
            for item in ancestors if item.rule is ProofRule.GIVEN
        )),
        "inference_rule": (
            step.inference_rule.name if step.inference_rule is not None else None
        ),
    }


def summarize(report: dict) -> str:
    """Print diagnostics only; never describe an unresolved goal as certified."""
    lines = [
        "# Phase 169 R5A — π₇⁵ 輸送前提の監査", "",
        f"- Git HEAD: `{report['head']}`",
        f"- π₇⁵ target citation: `{report['target_citation']}`",
        f"- π₆⁴ source eligibility: `{report['prior_eligibility']}`",
        f"- π₆⁴ source reason: `{report['prior_reason']}`",
        f"- π₆⁴ source citation: `{report['prior_source_citation']}`",
        f"- screened π₆⁴ GIVEN: `{report['screened_lower_given']}`",
        f"- screened Toda (4.5) schema: `{report['screened_toda45']}`",
        f"- 本来の cited Toda (4.5) root options: `{report['actual_cited_options']}`",
        f"- Goal-only diagnostic options: `{report['goal_only_options']}`", "",
        "## 各部分目標の実探索", "",
    ]
    for name, item in report["attempts"].items():
        lines.extend([
            f"### {name}", "",
            f"- solved: `{item['proved']}`",
            f"- rule: `{item['proof_rule']}`",
            f"- size: `{item['steps_in_subtree']}`",
        ])
        if item["error"]:
            lines.append(f"- error: `{item['error']}`")
        for unresolved in item["unresolved"][:8]:
            lines.append(f"- open: `{unresolved}`")
        lines.append("")
    lines.extend([
        "## 境界", "",
        "Goal-only diagnostic options は Provider に追加していない。",
        "DB の π₆⁴ を GIVEN に変換していない。",
        "発見された subgoal の証明に成功した場合のみ後続 Phase の接続候補とする。",
        "Toda (4.5) の安定範囲と文献順は変更しない。", "",
    ])
    return "\n".join(lines)


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=5, k=2)
    lower_goals = database_structured_group_goal_candidates(n=4, k=2)
    if len(targets) != 1 or len(lower_goals) != 1:
        raise RuntimeError("unique typed goals for pi_7^5 and pi_6^4 are required")
    target, lower = targets[0], lower_goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise RuntimeError("pi_7^5 citation must be resolved before screening")
    prior = resolve_prior_group_result(
        bridge, source_n=4, source_k=2, citing_assertion_id=citing,
    )
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    actual = expand_cited_toda45_composite_transport(target, available)
    # Probe an unattested lower goal only as a future subgoal in a candidate
    # expansion; this expanded tuple is never installed into the real provider.
    synthetic_options = expand_cited_toda45_composite_transport(
        target, (lower,) + available,
    )
    iso = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=1, source_group=lower.lhs, target_group=target.lhs,
    ))
    tests = {"lower_group_pi6_4": lower, "toda45_concrete_iso": iso}
    if synthetic_options:
        tests["eta_squared_generator_image"] = synthetic_options[0].subgoals[2]
    attempts = {
        name: diagnostic_attempt(goal, screened, citing, provider)
        for name, goal in tests.items()
    }
    return {
        "phase": "169-R5A", "mode": "AUDIT_ONLY",
        "head": git("rev-parse", "HEAD"),
        "target_citation": citing,
        "target": repr(target),
        "lower_goal": repr(lower),
        "prior_eligibility": prior.eligible,
        "prior_reason": prior.reason,
        "prior_source_citation": prior.source_assertion_id,
        "screened_lower_given": any(claim == lower for claim in available),
        "screened_toda45": any(isinstance(x, Toda45IsomorphismStatement) for x in available),
        "actual_cited_options": len(actual),
        "goal_only_options": len(synthetic_options),
        "goal_only_subgoal_types": [
            [type(item).__name__ for item in opt.subgoals]
            for opt in synthetic_options
        ],
        "attempts": attempts,
        "production_modified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("requires develop branch")
    before = git("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(summarize(report), encoding="utf-8")
    after = git("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("R5A changed tracked files; inspect the audit outputs")
    for field in (
        "head", "target_citation", "prior_eligibility", "prior_reason",
        "prior_source_citation", "screened_lower_given", "screened_toda45",
        "actual_cited_options", "goal_only_options",
    ):
        print(f"R5A_{field.upper()}={report[field]}")
    for name, item in report["attempts"].items():
        print(f"R5A_{name.upper()}_PROVED={item['proved']}")
        print(f"R5A_{name.upper()}_SUBTREE_STEPS={item['steps_in_subtree']}")
        if item["error"]:
            print(f"R5A_{name.upper()}_ERROR={item['error']}")
    print("R5A_TRACKED_STATUS_UNCHANGED=True")
    print("R5A_PRODUCTION_MODIFIED=False")
    print("R5A_FULL_PYTEST_RUN=False")
    print("R5A_REPORT=" + str(OUTPUT / "audit.md"))
    print("R5A_JSON=" + str(OUTPUT / "audit.json"))


if __name__ == "__main__":
    main()
