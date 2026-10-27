"""Prove exactly one map property; report the remaining group search status."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from proof import ProofRule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    bridge = build_shared_typed_bridge()
    target = registered_group_goal_candidates(bridge, n=4, k=2)[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise RuntimeError("citing source missing")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    injection = MapInjective(mapping)
    proof = reconstruct_registered_goal(
        injection, screened, citing, provider, lookup_mode="typed_reference",
    )
    if (proof.rule is not ProofRule.INFERENCE or proof.conclusion != injection
            or len(proof.premises) != 1 or proof.premises[0].rule is not ProofRule.GIVEN
            or proof.premises[0].conclusion != TodaProp44UniversalStatement()):
        raise RuntimeError("injection did not derive from the real cited source")
    result = search_group_from_registered_goal(n=4, k=2, bridge=bridge, goal=target)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    report = {
        "phase": "169-R4B",
        "head": head,
        "source": "Proposition 4.4",
        "map_injectivity_status": "CERTIFIED",
        "map_injectivity_is_inference": True,
        "map_injectivity_source_is_given": True,
        "proof_rule": proof.inference_rule.name if proof.inference_rule is not None else None,
        "pi6_4_search_status": result.status.value,
        "pi6_4_steps": len(result.proven_steps),
        "pi6_4_unresolved": [repr(x) for x in result.open_goals],
        "toda45_outside_stable_range_for_pi5_3": True,
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 169 R4B — Proposition 4.4 の単射性接続", "",
        "- Proposition 4.4: citation-screened GIVEN を使用", 
        "- E: π₅³ → π₆⁴ の単射性: INFERENCE により検証", 
        f"- π₆⁴ 全体: {result.status.value}",
        f"- 未解決 Goal: {len(result.open_goals)}", "",
        "## 範囲", "",
        "Toda (4.5) の安定範囲を変更せず、E 全射性・E 同型・群構造は新規に断定しない。", "",
    ]
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R4B_GIT_HEAD=" + head)
    print("R4B_PROP44_INJECTIVITY_CERTIFIED=True")
    print("R4B_PI64_STATUS=" + result.status.value)
    print("R4B_PI64_STEPS=" + str(len(result.proven_steps)))
    print("R4B_PI64_OPEN_GOALS=" + str(len(result.open_goals)))
    print("R4B_FULL_PYTEST_RUN=False")
    print("R4B_REPORT=" + str(output / "audit.md"))


if __name__ == "__main__":
    main()
