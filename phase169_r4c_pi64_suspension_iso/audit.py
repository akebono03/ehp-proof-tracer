"""Inspect the newly connected E-isomorphism and public pi6_4 goal; no fabricated proof."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
from proof import ProofRule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def ancestors(step):
    seen = set()
    stack = [step]
    result = []
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        result.append(node)
        stack.extend(node.premises)
    return tuple(result)


def main() -> None:
    bridge = build_shared_typed_bridge()
    target_candidates = registered_group_goal_candidates(bridge, n=4, k=2)
    if len(target_candidates) != 1:
        raise RuntimeError("pi6_4 registered goal is not unique")
    target = target_candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise RuntimeError("pi6_4 has no citation target")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    e = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    goal = TodaSuspensionIsomorphismStatement(e)
    proof = reconstruct_registered_goal(
        goal, screened, citing, provider, lookup_mode="typed_reference",
    )
    if (proof.conclusion != goal or proof.rule is not ProofRule.INFERENCE
            or len(proof.premises) != 2
            or tuple(node.conclusion for node in proof.premises) !=
            (MapInjective(e), MapSurjective(e))
            or any(node.rule is not ProofRule.INFERENCE for node in proof.premises)):
        raise RuntimeError("R4C E isomorphism does not have two proved map properties")
    traced = ancestors(proof)
    cited_types = (
        TodaProp44UniversalStatement,
        TodaProp42GeneralExactnessStatement,
        Toda51BelowDiagonalZeroStatement,
    )
    source_presence = {
        cls.__name__: any(step.rule is ProofRule.GIVEN and type(step.conclusion) is cls
                          for step in traced)
        for cls in cited_types
    }
    if not all(source_presence.values()):
        raise RuntimeError("E isomorphism missing required actual earlier source leaves")
    search = search_group_from_registered_goal(n=4, k=2, bridge=bridge, goal=target)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    report = {
        "phase": "169-R4C",
        "head": head,
        "goal": repr(target),
        "iso": repr(goal),
        "iso_derived": True,
        "iso_rule": proof.inference_rule.name if proof.inference_rule else None,
        "map_properties": [repr(x.conclusion) for x in proof.premises],
        "cited_source_ancestors": source_presence,
        "citation_screened": True,
        "toda45_stable_range_relaxed": False,
        "pi6_4_status": search.status.value,
        "pi6_4_steps": len(search.proven_steps),
        "pi6_4_open_goals": [repr(x) for x in search.open_goals],
        "pi6_4_diagnostics": list(search.diagnostics),
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 169 R4C — π₅³ → π₆⁴ 懸垂同型の証明接続", "",
        "- 引用済み Proposition 4.4 を用いた単射性: INFERENCE",
        "- Proposition 4.2 (4.4) と (5.1) による全射性: INFERENCE",
        "- E の同型: 2 つの INFERENCE から導出",
        "- Toda (4.5) の安定範囲: 変更なし", "",
        "## 出典祖先", "",
    ]
    for name, exists in source_presence.items():
        lines.append(f"- `{name}`: `{exists}`")
    lines.extend([
        "", "## 公開証明探索", "",
        f"- π₆⁴ 探索状態: `{search.status.value}`",
        f"- 証明 Step: `{len(search.proven_steps)}`",
        f"- 未解決 Goal: `{len(search.open_goals)}`", "",
    ])
    if search.open_goals:
        for unresolved in search.open_goals:
            lines.append(f"- `{unresolved!r}`")
    lines.extend([
        "", "未解決項目は完成証明として表示しない。",
        "この Phase は E 同型の証明接続に限定し、Renderer は変更しない。", "",
    ])
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R4C_GIT_HEAD=" + head)
    print("R4C_E_ISOMORPHISM_PROVED=True")
    print("R4C_PROVENANCE_PROP44_PROP42_TODA51=True")
    print("R4C_PI64_STATUS=" + search.status.value)
    print("R4C_PI64_STEPS=" + str(len(search.proven_steps)))
    print("R4C_PI64_OPEN_GOALS=" + str(len(search.open_goals)))
    print("R4C_FULL_PYTEST_RUN=False")
    print("R4C_REPORT=" + str(output / "audit.md"))


if __name__ == "__main__":
    main()
