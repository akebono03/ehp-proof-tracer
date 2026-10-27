"""R7 after-patch canonical search and publication-proof-tree regression audit."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view

OUTPUT = Path(__file__).resolve().parent / "output"
ROOT = Path(__file__).resolve().parent.parent


def audit_case(n: int, k: int, bridge, must_be_complete: bool) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    status = result.status
    report = {
        "n": n, "k": k, "status": status.value,
        "steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "root_premises": None,
        "publication_proof_tree_verified": False,
        "web_key": None,
    }
    if must_be_complete and status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError(f"pi_{n+k}^{n} regressed from complete: {result.open_goals!r}")
    if status is ProofSearchStatus.COMPLETE:
        if result.open_goals or len(contexts) != 1:
            raise RuntimeError("complete proof missing screened context or has open goals")
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        if citing is None:
            raise RuntimeError("completed group lacks uniquely positioned citation")
        verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
        root = result.proven_steps[-1]
        if root.rule is not ProofRule.INFERENCE:
            raise RuntimeError("complete group root is not inference-derived")
        report["publication_proof_tree_verified"] = True
        report["root_premises"] = len(root.premises)
        view = build_standard_web_group_proof_view(n, k, mode="narrative")
        report["web_key"] = view.key
        if view.key != "generic-complete-proof" or view.partial_result:
            raise RuntimeError("completed proof was not exposed by shared Web")
    return report


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], check=True,
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()
    bridge = build_shared_typed_bridge()
    report = {
        "phase": "169-R7",
        "kind": "after-patch focused audit",
        "git_head": head,
        "cases": [],
        "full_pytest_run": False,
    }
    for n in (5, 6, 7, 8):
        label = f"pi_{n+2}^{n}"
        try:
            item = audit_case(n, 2, bridge, must_be_complete=n in (5, 6))
            report["cases"].append(item)
            print(f"R7_{label}_STATUS=" + str(item["status"]))
            print(f"R7_{label}_STEPS=" + str(item["steps"]))
            print(f"R7_{label}_OPEN_GOALS=" + str(item["open_goals"]))
        except Exception as exc:
            if n in (5, 6):
                raise
            report["cases"].append({
                "n": n, "k": 2, "status": "not_verified",
                "error_type": type(exc).__name__, "error": str(exc),
            })
            print(f"R7_{label}_STATUS=not_verified")
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 169 R7 — 任意回数懸垂の限定監査", "",
        "- Git HEAD: `" + head + "`",
        "- 本番変更: `phase165_r52_r9_shared_math.py::shared_expansion_provider`",
        "- 全体 pytest: 未実行", "",
        "| 目標群 | 探索結果 | ProofStep | Open Goal | Proof Tree 検証 | Web |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in report["cases"]:
        label = f"π_{item['n']+2}^{item['n']}"
        lines.append("| " + label + " | " + item["status"] + " | "
                     + str(item.get("steps", "—")) + " | "
                     + str(item.get("open_goals", "—")) + " | "
                     + str(item.get("publication_proof_tree_verified", False)) + " | "
                     + str(item.get("web_key", "—")) + " |")
    lines += ["", "π₉⁷、π₁₀⁸ については完成証明を仮定しない。",
              "未解決があれば partial を維持する。", ""]
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R7_AUDIT_JSON=" + str(OUTPUT / "audit.json"))
    print("R7_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
