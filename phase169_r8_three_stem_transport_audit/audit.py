"""Phase 169 R8 — non-mutating 3-stem proof-dependency inspection.

Runs public proof searches and screened premise diagnostics, without writing
production files or manufacturing ProofSteps.
"""
from __future__ import annotations

import json
import subprocess
import traceback
from datetime import datetime, timezone
from pathlib import Path

from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r7_general_stable_transport.rule import (
    _consecutive_generator_image_goals,
    expand_prior_general_stable_transport,
)
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
CASES = ((5, 3), (6, 3), (7, 3))


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        return "UNAVAILABLE: " + result.stderr.strip()
    return result.stdout.strip()


def _context(bridge, goal):
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        return None, None, (), "citing_id_missing"
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion
        for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    return citing_id, screened, available, "screened"


def _compact_prior(prior, goal):
    result = {
        "n": prior.source_n,
        "k": prior.source_k,
        "eligible": prior.eligible,
        "reason": prior.reason,
        "positioned_citation": prior.source_assertion_id,
        "has_candidate_relation": prior.relation is not None,
    }
    if prior.relation is not None:
        images = _consecutive_generator_image_goals(prior.relation, goal)
        result["typed_image_goals"] = None if images is None else len(images)
        if images:
            result["image_types"] = [type(x).__name__ for x in images]
            result["first_generator_image"] = repr(images[0])
    return result


def diagnose_case(bridge, n: int, k: int) -> dict:
    output: dict = {"n": n, "k": k, "group": f"pi_{n+k}^{n}"}
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    output["goal_candidates"] = len(candidates)
    if len(candidates) != 1:
        output["diagnosis"] = "goal_not_unique"
        return output
    goal = candidates[0]
    output["goal"] = repr(goal)
    citing_id, screened, available, state = _context(bridge, goal)
    output["citation_status"] = state
    output["citing_assertion_id"] = citing_id
    output["admitted_given_count"] = len(available)
    if screened is not None:
        output["has_toda45_source"] = any(
            isinstance(x, Toda45IsomorphismStatement) for x in available
        )
        providers = shared_expansion_provider(
            screened, proof_target=goal,
        )
        root_options = providers(goal)
        output["shared_root_candidates"] = len(root_options)
        output["shared_general_transport_root_candidates"] = sum(
            "arbitrary-fold stable cyclic" in option.rule.name
            for option in root_options
        )
        output["direct_general_transport_candidates"] = len(
            expand_prior_general_stable_transport(
                goal, available, screened, proof_target=goal,
            )
        )
        possible_sources = []
        for source_n in range(k + 2, n):
            prior = resolve_prior_group_result(
                screened, source_n=source_n, source_k=k,
                citing_assertion_id=citing_id,
            )
            possible_sources.append(_compact_prior(prior, goal))
        output["prior_sources"] = possible_sources
        if output["direct_general_transport_candidates"]:
            expansion = expand_prior_general_stable_transport(
                goal, available, screened, proof_target=goal,
            )[0]
            output["general_transport_subgoals"] = [
                type(statement).__name__ for statement in expansion.subgoals
            ]
            output["generator_image_subgoals"] = sum(
                isinstance(statement, GeneratorImage)
                for statement in expansion.subgoals
            )
    try:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        output["proof_status"] = result.status.value
        output["proof_steps"] = len(result.proven_steps)
        output["unresolved_goal_count"] = len(result.open_goals)
        output["unresolved_goal_types"] = [type(x).__name__ for x in result.open_goals]
        output["root_rule_name"] = (
            result.proven_steps[-1].inference_rule.name
            if result.proven_steps and result.proven_steps[-1].inference_rule is not None
            else None
        )
    except Exception as exc:
        output["search_exception"] = type(exc).__name__ + ": " + str(exc)
        output["search_traceback"] = traceback.format_exc(limit=5)
    return output


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("Audit requires develop branch; actual branch: " + branch)
    before = _git("status", "--porcelain=v1", "--untracked-files=no")
    report: dict = {
        "phase": "169-R8",
        "mode": "AUDIT_ONLY",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "branch": branch,
        "local_head": _git("rev-parse", "HEAD"),
        "remote_develop": _git("ls-remote", "origin", "refs/heads/develop"),
        "working_tree_before": before,
        "cases": [],
        "whole_pytest_run": False,
        "production_files_modified": False,
    }
    bridge = build_shared_typed_bridge()
    for n, k in CASES:
        try:
            item = diagnose_case(bridge, n, k)
        except Exception as exc:
            item = {
                "n": n, "k": k,
                "diagnostic_exception": type(exc).__name__ + ": " + str(exc),
                "traceback": traceback.format_exc(limit=7),
            }
        report["cases"].append(item)
        print("R8_PI_%d_%d_STATUS=%s" % (
            n + k, n,
            item.get("proof_status", "diagnostic_incomplete"),
        ))
        print("R8_PI_%d_%d_GENERAL_CANDIDATES=%s" % (
            n + k, n,
            item.get("direct_general_transport_candidates", "unknown"),
        ))
    after = _git("status", "--porcelain=v1", "--untracked-files=no")
    report["working_tree_after"] = after
    report["working_tree_unchanged"] = before == after
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 169 R8 — 3-stem 安定輸送の依存関係監査", "",
        "- モード: AUDIT_ONLY", 
        "- Git HEAD: `" + report["local_head"] + "`",
        "- 既存 tracked files 不変: `" + str(report["working_tree_unchanged"]) + "`",
        "- 全体 pytest: 未実行", "",
        "| 群 | 証明状態 | ProofStep | 未解決 Goal | 共通輸送候補 |",
        "|---|---|---:|---:|---:|",
    ]
    for item in report["cases"]:
        name = f"π_{item['n']+item['k']}^{item['n']}"
        lines.append("| " + name + " | "
                     + str(item.get("proof_status", "not_verified")) + " | "
                     + str(item.get("proof_steps", "—")) + " | "
                     + str(item.get("unresolved_goal_count", "—")) + " | "
                     + str(item.get("direct_general_transport_candidates", "—")) + " |")
        for p in item.get("prior_sources", []):
            lines.append("\n" + name + " の先行候補 π_"
                         + str(p["n"]+p["k"]) + "^" + str(p["n"])
                         + ": 文献順利用=" + str(p["eligible"])
                         + ", 理由=" + p["reason"]
                         + ", 型付き画像数=" + str(p.get("typed_image_goals", "不明")))
    lines += [
        "", "## 解釈の注意", "",
        "- 先行 group Relation は DB の候補であり GIVEN ではない。",
        "- `eligible` は文献順の可否であり、群構造の証明完成ではない。",
        "- `direct_general_transport_candidates` は証明候補であり complete ではない。",
        "- 画像の型付き構築と、画像の実際の証明は別段階。",
        "- 3-stem 公開 Provider の変更・R6B の実行は一切行わない。",
        "- 数値的な安定範囲は k=3 の n>=5。", "",
    ]
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R8_AUDIT_ONLY=True")
    print("R8_PRODUCTION_PATCHED=False")
    print("R8_TRACKED_WORKTREE_UNCHANGED=" + str(before == after))
    print("R8_OUTPUT=" + str(OUTPUT / "audit.md"))
    print("R8_WHOLE_PYTEST_RUN=False")
    return 0 if before == after else 2


if __name__ == "__main__":
    raise SystemExit(main())
