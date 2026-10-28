"""Live read-only proof audit AFTER the R3 cited Definition registration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10eo_r3_reviewed_definition_bridge.reviewed_definitions import (
    reviewed_definition_ids,
    verified_reviewed_definitions,
)


def run_audit() -> dict:
    reviewed = verified_reviewed_definitions()
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=30, k=11, bridge=bridge, context_sink=contexts.append,
    )
    trust = "NOT_APPLICABLE_INCOMPLETE"
    if result.status is ProofSearchStatus.COMPLETE:
        if not contexts or result.conclusion is None:
            raise RuntimeError("completed proof has no verification context")
        citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        inference, given = verify_proof_tree_for_narrative(
            result, contexts[-1], citing_assertion_id=citing_id,
            derived_target_without_citing_id=citing_id is None,
        )
        trust = "PASS"
    report = {
        "phase": "169 R10EO-R3",
        "mode": "REVIEWED_SOURCE_REGISTRATION",
        "reviewed_definition_ids": sorted(reviewed_definition_ids()),
        "verified_reviewed_definition_positions": [item[2] for item in reviewed],
        "pi41_30_status": result.status.value,
        "pi41_30_open_goal_types": [type(goal).__name__ for goal in result.open_goals],
        "pi41_30_open_goal_details": [repr(goal)[:1600] for goal in result.open_goals],
        "pi41_30_diagnostics": list(result.diagnostics),
        "pi41_30_trust": trust,
        "proof_tree_trust_required_when_complete": True,
        "inference_rules_added": False,
        "full_pytest_run": False,
    }
    if trust == "PASS":
        report["verified_inference_steps"] = inference
        report["verified_given_steps"] = given
    return report


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise SystemExit("Usage: python -m phase169_r10eo_r3_reviewed_definition_bridge.audit --output DIRECTORY")
    directory = Path(sys.argv[2]).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    data = run_audit()
    (directory / "audit.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# R10EO-R3 — 審査済み Definition の引用登録監査", "",
        "本監査では採用済み転写を使用する。原著印刷版の独立照合済みとはみなさない。", "",
        f"- 登録された Definition ID: {data['reviewed_definition_ids']}",
        f"- 引用の位置: {data['verified_reviewed_definition_positions']}",
        f"- $\\pi_{{41}}^{{30}}$ 探索結果: `{data['pi41_30_status']}`",
        f"- 未解決 Goal: {data['pi41_30_open_goal_types']}",
        f"- Trust Boundary: {data['pi41_30_trust']}", "",
        "新しい生成元専用推論規則は追加していない。", "",
    ]
    (directory / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R10EO_R3_REVIEWED_IDS=" + str(data["reviewed_definition_ids"]))
    print("R10EO_R3_PI41_30_STATUS=" + data["pi41_30_status"])
    print("R10EO_R3_PI41_30_OPEN_GOALS=" + str(data["pi41_30_open_goal_types"]))
    print("R10EO_R3_PI41_30_TRUST=" + data["pi41_30_trust"])
    print("R10EO_R3_AUDIT_PATH=" + str(directory / "audit.json"))


if __name__ == "__main__":
    main()
