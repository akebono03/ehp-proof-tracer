"""Phase 169 R4A: read-only audit of Toda Proposition 4.4 EHP route to pi_6^4.

This module neither patches production sources nor turns candidates into proof steps.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    shared_expansion_provider,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
from phase165_r12_r15_toda51 import expand_cited_toda51_zero
from phase165_r52_r27_r5_literature import (
    TodaProp44UniversalStatement,
    _toda45_universal_statement,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import GeneratorImage
from toda_rules import TodaSuspensionInjectiveStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent


def git_value(*args: str) -> dict:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    return {"exit_code": result.returncode, "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()}


def source_excerpt(path: Path, start: str, stop: str) -> dict:
    data = path.read_text(encoding="utf-8")
    a = data.find(start)
    b = data.find(stop, a + len(start)) if a != -1 else -1
    if a < 0 or b < 0:
        return {"found": False, "path": str(path), "excerpt": ""}
    return {"found": True, "path": str(path),
            "excerpt": data[a:b + len(stop)]}


def expansion_summaries(expansions) -> list[dict]:
    return [{"rule": getattr(item.rule, "name", type(item.rule).__name__),
             "subgoal_types": [type(goal).__name__ for goal in item.subgoals],
             "subgoals": [repr(goal) for goal in item.subgoals]}
            for item in expansions]


def describe_assertion(bridge, assertion) -> dict:
    ref = bridge.registry.reference(assertion.reference_id)
    return {"id": assertion.assertion_id, "locator": ref.locator,
            "publication_position": ref.publication_position,
            "component_position": assertion.component_position,
            "origin": getattr(assertion.origin, "name", str(assertion.origin)),
            "content_type": type(assertion.content).__name__,
            "content": repr(assertion.content)}


def run_audit() -> dict:
    git = {
        "branch": git_value("branch", "--show-current"),
        "head": git_value("rev-parse", "HEAD"),
        "tracked_changes_before": git_value("diff", "--name-only"),
        "staged_changes_before": git_value("diff", "--cached", "--name-only"),
    }
    original44 = source_excerpt(
        ROOT / "sources" / "toda" / "Toda_04_2.tex",
        r"\begin{proposition}\label{prop:4.4}", r"\end{proposition}",
    )
    original53 = source_excerpt(
        ROOT / "sources" / "toda" / "Toda_05_2.tex",
        r"\begin{proposition}\label{prop:5.3}", r"\qed",
    )
    bridge = build_shared_typed_bridge()
    targets = {
        "pi_5^3": registered_group_goal_candidates(bridge, n=3, k=2),
        "pi_6^4": registered_group_goal_candidates(bridge, n=4, k=2),
    }
    if len(targets["pi_6^4"]) != 1:
        raise ValueError("R4A expects a unique registered pi_6^4 goal")
    goal = targets["pi_6^4"][0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing is None:
        raise ValueError("R4A requires a positioned pi_6^4 source")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    original_claims = tuple(assertion for assertion in bridge.registry._assertions.values()
                            if type(assertion.content) is TodaProp44UniversalStatement)
    screened_claims = tuple(screened.registry.assertion(link.assertion_id)
                            for link in screened.proof_links
                            if link.step is not None and link.step.rule is ProofRule.GIVEN)
    prop44 = [describe_assertion(bridge, entry) for entry in original_claims]
    prop44_screened = tuple(entry.assertion_id for entry in screened_claims
                            if type(entry.content) is TodaProp44UniversalStatement)
    prior_pi53 = tuple(entry.assertion_id for entry in screened_claims
                       if entry.assertion_id.endswith(":pi5_3_group_relation"))
    n3 = TodaPrimaryGroup(5, 3)
    n4 = TodaPrimaryGroup(6, 4)
    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(6, 7))
    e_map = TodaSuspensionMap(n3, n4)
    e_surjection = MapSurjective(e_map)
    e_injection = MapInjective(e_map)
    e_typed_injection = TodaSuspensionInjectiveStatement(e_map)
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    zero_expansions = expand_cited_toda51_zero(target_zero, available)
    surjection_expansions = expand_ehp_exactness_consequences(e_surjection)
    provider = shared_expansion_provider(screened, proof_target=goal)
    provider_inspection = {}
    for name, target in (
        ("map_surjective", e_surjection),
        ("map_injective", e_injection),
        ("toda_suspension_injective", e_typed_injection),
    ):
        try:
            provider_inspection[name] = {
                "expansions": expansion_summaries(provider(target)), "error": None}
        except Exception as exc:
            provider_inspection[name] = {
                "expansions": [], "error": f"{type(exc).__name__}: {exc}"}
    normalizer = []
    if len(targets["pi_5^3"]) == 1:
        source = targets["pi_5^3"][0]
        iso_schema = _toda45_universal_statement()
        normalizer = expansion_summaries(
            expand_cited_toda45_composite_transport(goal, (source, iso_schema))
        )
        generator_goal = GeneratorImage(
            e_map, source.rhs.generator, goal.rhs.generator,
        )
        eta_image_expansions = expansion_summaries(expand_cited_eta_generator(generator_goal))
    else:
        eta_image_expansions = []

    complete_search = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, goal=goal,
    )
    audit = {
        "phase": "169-R4A", "mode": "AUDIT_ONLY",
        "production_modified": False, "full_pytest_run": False,
        "git": git,
        "source": {"proposition44": original44, "proposition53_proof": original53},
        "target_goal": repr(goal), "citing_assertion_id": citing,
        "goal_counts": {key: len(value) for key, value in targets.items()},
        "prop44_registry": prop44,
        "prop44_screened_ids": prop44_screened,
        "prop44_is_prior": [precedes_citing_assertion(bridge, entry.assertion_id, citing)
                            for entry in original_claims],
        "prior_pi53_source_ids": prior_pi53,
        "source_scope": {"source_sphere_dimension": 3, "stem": 2,
                         "toda45_stable_range": False,
                         "n4_is_toda45_stable_base": True},
        "surjectivity": {
            "map": repr(e_map), "zero_target": repr(target_zero),
            "zero_goal_expansions": expansion_summaries(zero_expansions),
            "EHP_candidate_expansions": expansion_summaries(surjection_expansions),
            "EHP_valid_indices": [prop42_exactness_indices(item.subgoals[0])
                                  for item in surjection_expansions],
        },
        "injectivity": {
            "map": repr(e_map),
            "universal_prop44_cited": bool(prop44_screened),
            "provider": {key: provider_inspection[key] for key in
                         ("map_injective", "toda_suspension_injective")},
            "inference_certified": False,
        },
        "generator_transport": {
            "eta_image_expansions": eta_image_expansions,
            "ineligible_toda45_candidates": normalizer,
        },
        "provider": provider_inspection,
        "search": {"status": complete_search.status.value,
                   "steps": len(complete_search.proven_steps),
                   "open_goals": [repr(value) for value in complete_search.open_goals],
                   "diagnostics": list(complete_search.diagnostics)},
        "next_boundary": "Audit only: connect cited Proposition 4.4 injection and EHP surjection in a later implementation, without treating candidates as a proof.",
    }
    audit["git"]["tracked_changes_after"] = git_value("diff", "--name-only")
    audit["git"]["staged_changes_after"] = git_value("diff", "--cached", "--name-only")
    audit["tracked_changes_unchanged"] = (
        audit["git"]["tracked_changes_before"]["stdout"]
        == audit["git"]["tracked_changes_after"]["stdout"]
        and audit["git"]["staged_changes_before"]["stdout"]
        == audit["git"]["staged_changes_after"]["stdout"]
    )
    return audit


def render_markdown(audit: dict) -> str:
    s = audit["search"]
    surj = audit["surjectivity"]
    inj = audit["injectivity"]
    lines = [
        "# Phase 169 R4A — Proposition 4.4 / EHP 経路監査",
        "",
        "本監査は読み取り専用であり、証明完了を宣言しない。",
        "",
        f"- Git HEAD: `{audit['git']['head']['stdout']}`",
        f"- 既存探索: `{s['status']}`、証明 Step: {s['steps']}、未解決 Goal: {len(s['open_goals'])}",
        f"- 原文 Proposition 4.4: {audit['source']['proposition44']['found']}",
        f"- 原文 Proposition 5.3 の証明: {audit['source']['proposition53_proof']['found']}",
        f"- Proposition 4.4 の型付き台帳エントリ数: {len(audit['prop44_registry'])}",
        f"- 引用審査済み Proposition 4.4 の数: {len(audit['prop44_screened_ids'])}",
        f"- Proposition 4.4 出版順が前: {audit['prop44_is_prior']}",
        f"- 直前の π₅³ 出典成分: {list(audit['prior_pi53_source_ids'])}",
        f"- (5.1) による π₆⁷=0 候補: {len(surj['zero_goal_expansions'])}",
        f"- EHP の E 全射候補: {len(surj['EHP_candidate_expansions'])}",
        f"- EHP の添字検証: {surj['EHP_valid_indices']}",
        f"- E 単射の出典登録: {inj['universal_prop44_cited']}",
        f"- 型付き MapInjective 展開候補: {len(inj['provider']['map_injective']['expansions'])}",
        f"- 型付き TodaSuspensionInjective 展開候補: {len(inj['provider']['toda_suspension_injective']['expansions'])}",
        f"- η² 合成生成元の E 像展開候補: {len(audit['generator_transport']['eta_image_expansions'])}",
        f"- 安定範囲外の (4.5) 輸送候補: {len(audit['generator_transport']['ineligible_toda45_candidates'])}",
        f"- Git 追跡ファイルの変更なし: {audit['tracked_changes_unchanged']}",
        "",
        "## 未解決 Goal",
        "",
    ]
    for index, item in enumerate(s["open_goals"], start=1):
        lines.append(f"{index}. `{item}`")
    lines.extend([
        "", "## 判定", "",
        "Proposition 5.3 の原文では π₅³→π₆⁴ の全射性を (5.1)、単射性を Proposition 4.4 によって示す。",
        "この監査はその引用・型付き候補を検査するものであり、単射性が既に証明済みかを候補数だけで判定しない。",
        "Toda (4.5) の n=3,k=2 への適用は許可しない。",
        "", "## 原文 Proposition 4.4", "", "```tex",
        audit["source"]["proposition44"]["excerpt"], "```",
        "", "## 原文 Proposition 5.3 の証明", "", "```tex",
        audit["source"]["proposition53_proof"]["excerpt"], "```", "",
    ])
    return "\n".join(lines)


def main() -> None:
    result = run_audit()
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    json_path = output / "audit.json"
    markdown_path = output / "audit.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(result), encoding="utf-8")
    print("R4A_GIT_HEAD=" + result["git"]["head"]["stdout"])
    print("R4A_PI64_STATUS=" + result["search"]["status"])
    print("R4A_PI64_STEPS=" + str(result["search"]["steps"]))
    print("R4A_PI64_OPEN_GOALS=" + str(len(result["search"]["open_goals"])))
    print("R4A_PROP44_SCREENED=" + str(bool(result["prop44_screened_ids"])))
    print("R4A_EHP_SURJ_OPTIONS=" + str(len(result["surjectivity"]["EHP_candidate_expansions"])))
    print("R4A_PI67_ZERO_OPTIONS=" + str(len(result["surjectivity"]["zero_goal_expansions"])))
    print("R4A_PROP44_INJECTIVITY_CERTIFIED=False")
    print("R4A_TODA45_STABLE_RANGE=False")
    print("R4A_AUDIT_ONLY=True")
    print("R4A_PRODUCTION_MODIFIED=False")
    print("R4A_FULL_PYTEST_RUN=False")
    print("R4A_JSON=" + str(json_path))
    print("R4A_MARKDOWN=" + str(markdown_path))
    if not result["tracked_changes_unchanged"]:
        raise RuntimeError("tracked Git changes occurred during read-only audit")


if __name__ == "__main__":
    main()
