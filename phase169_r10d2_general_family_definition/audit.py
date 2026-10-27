"""Focused production checks; record search failures instead of falsifying success."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, build_cited_stable_family_definitions,
    verified_source_positions,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def nu(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="ν" + str(n).translate(_SUB),
        dimension=n, source=n + 3, target=n,
        generator=GeneratorSymbol(family="ν", index=n),
    )


def main() -> None:
    bridge = build_shared_typed_bridge()
    cited = tuple((assertion.content, bridge.registry.reference(assertion.reference_id))
                  for assertion in bridge.registry._assertions.values()
                  if isinstance(assertion.content, CitedStableFamilyDefinition))
    if sorted(source.family_id for source, _ in cited) != [4, 9]:
        raise RuntimeError("reviewed ν/σ general definitions not registered exactly once")
    for source, ref in cited:
        expected = dict(verified_source_positions())[source.family_id]
        if ref.publication_position != expected:
            raise RuntimeError("cited-family publication rank missing or changed")
    goal, = registered_group_goal_candidates(bridge, n=8, k=3)
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    available = ()
    candidate_count = 0
    if citing is not None:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing,
            explicit_publication_target=True,
        )
        available = tuple(link.step.conclusion for link in screened.proof_links
                          if link.step is not None and link.step.rule is ProofRule.GIVEN)
        nu_definition = CitedStableFamilyDefinition(4, 4, 3)
        if available.count(nu_definition) != 1:
            raise RuntimeError("ν source not admitted as a single prior citation")
        image = GeneratorImage(
            TodaSuspensionMap(TodaPrimaryGroup(8, 5), TodaPrimaryGroup(9, 6)),
            nu(5), nu(6),
        )
        options = shared_expansion_provider(screened, proof_target=goal)(image)
        candidate_count = len(options)
        if not any(option.rule.name.startswith("consecutive cited stable-family")
                   for option in options):
            raise RuntimeError("general GeneratorImage rule not connected")
    searches = []
    for n, k in ((8, 1), (8, 2), (5, 3), (6, 3), (7, 3), (8, 3)):
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        searches.append({
            "group": f"pi_{n+k}^{n}",
            "stem": k,
            "status": result.status.value,
            "proof_steps": len(result.proven_steps),
            "open_goals": len(result.open_goals),
            "diagnostics": list(result.diagnostics),
        })
        print(f"R10D2_PI_{n+k}^{n}_STATUS={result.status.value}")
    if any(case["status"] != "complete" for case in searches[:2]):
        raise RuntimeError("previously completed 1-stem or 2-stem regressed")
    report = {
        "phase": "169-R10D2",
        "branch": "develop",
        "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip(),
        "source_position_by_family_id": dict(verified_source_positions()),
        "reviewed_family_count": len(cited),
        "all_db_families_are_proven": False,
        "nu_public_image_options": candidate_count,
        "three_stem_completed": searches[-1]["status"] == "complete",
        "cases": searches,
        "full_pytest_run": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(
        "# Phase 169 R10D2 限定監査\n\n"
        "型付き系列定義は ν・σ を同一推論規則で扱う。"
        "掲載順は採用された TeX 転記原稿に基づき、原本の独立検証ではない。\n\n"
        "| 群 | 状態 | ProofStep | 未解決 |\n|---|---|---:|---:|\n"
        + "\n".join(f"| {x['group']} | {x['status']} | {x['proof_steps']} | {x['open_goals']} |"
                    for x in searches)
        + "\n\n全体 pytest は未実行。\n",
        encoding="utf-8",
    )
    print("R10D2_GENERAL_FAMILY_IDS=4,9")
    print("R10D2_NU_IMAGE_CANDIDATE_COUNT=" + str(candidate_count))
    print("R10D2_PI11_8_COMPLETE=" + str(report["three_stem_completed"]))
    print("R10D2_AUDIT=" + str(OUTPUT / "audit.json"))
    print("R10D2_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
