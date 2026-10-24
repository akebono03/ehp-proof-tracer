"""R3-41P12: audit literature precedence along the public narrative path.

This file is deliberately read-only with respect to application modules.
"""
from __future__ import annotations

import json
import re
import sys
import traceback
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
BASELINES = PACKAGE / "baselines"


def evaluate_publication(citing_id, linked_ids, checker):
    """Fail closed for unknown target; report, never grant, publication trust."""
    if not linked_ids:
        return "MISSING_LINK"
    if citing_id is None:
        return "UNVERIFIABLE_TARGET"
    if not all(checker(source_id, citing_id) for source_id in linked_ids):
        return "NOT_PRIOR"
    return "PRIOR"


def citation_numbers_in_proof(proof):
    return set(int(x) for x in re.findall(r"\[R(\d+)\]", proof))


def audit_case(name, n, k):
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    import phase165_r55_nk_only_goal as search_module
    import phase168_r3_4_link_bridge as link_module
    import phase168_r3_5_model_renderer as renderer_module
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase168_r3_38_frozen_fulltext_audit.audit import sections
    from phase168_r3_39f_frozen_comparison.audit import assess
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    from web_group_proof import build_standard_web_group_proof_view

    _ = search_group_from_registered_goal
    originally_search = search_module.search_group_from_registered_goal
    originally_link = link_module.build_linked_proof_narrative_model
    originally_render = renderer_module.render_model_backed_narrative_markdown
    captures = {"search": [], "linked": [], "render": []}

    def observe_search(*args, **kwargs):
        original_bridge = kwargs.get("bridge")
        result = originally_search(*args, **kwargs)
        captures["search"].append((result, original_bridge))
        return result

    def observe_link(result, bridge):
        model = originally_link(result, bridge)
        captures["linked"].append((result, bridge, model))
        return model

    def observe_render(result, model):
        text = originally_render(result, model)
        captures["render"].append((text, result, model))
        return text

    with patch.object(search_module, "search_group_from_registered_goal", side_effect=observe_search), \
         patch.object(link_module, "build_linked_proof_narrative_model", side_effect=observe_link), \
         patch.object(renderer_module, "render_model_backed_narrative_markdown", side_effect=observe_render):
        view = build_standard_web_group_proof_view(n=n, k=k)
    if len(captures["search"]) != 1 or len(captures["linked"]) != 1 or len(captures["render"]) != 1:
        raise AssertionError("The public path must search, link, and render once")
    result, unscreened = captures["search"][0]
    linked_result, screened, model = captures["linked"][0]
    rendered, render_result, render_model = captures["render"][0]
    if (linked_result is not result or render_result is not result
            or render_model is not model or unscreened is None):
        raise AssertionError("Public path handoff identity mismatch")
    if model.steps != result.proven_steps:
        raise AssertionError("Model differs from searched proof steps")

    baseline = (BASELINES / (name + ".md")).read_text(encoding="utf-8")
    reference, proof = sections(rendered)
    source_nums = citation_numbers_in_proof(proof)
    model_nums = {c.number for c in model.citations}
    benchmark_ok = all(entry["present"] for entry in assess(name, proof))

    # In the existing public path the citing target is resolved from the
    # unscreened registry BEFORE source screening. Do not infer a target from
    # a displayed heading, and do not claim an implicit target is positioned.
    citing_id = resolve_specialized_goal_citing_id(unscreened, result.conclusion)
    citing_info = None
    if citing_id is not None:
        citing_assertion = unscreened.registry.assertion(citing_id)
        citing_ref = unscreened.registry.reference(citing_assertion.reference_id)
        citing_info = {
            "assertion_id": citing_id,
            "reference_id": citing_assertion.reference_id,
            "locator": citing_ref.locator,
            "publication_position": citing_ref.publication_position,
            "component_position": citing_assertion.component_position,
        }

    given_entries = []
    for index, step in enumerate(model.steps):
        if step.rule is not ProofRule.GIVEN:
            continue
        matches = [
            link for link in screened.proof_links
            if link.step is not None and (link.step is step or link.step == step)
        ]
        sources = []
        for link in matches:
            assertion = screened.registry.assertion(link.assertion_id)
            ref = screened.registry.reference(assertion.reference_id)
            sources.append({
                "assertion_id": link.assertion_id,
                "reference_id": assertion.reference_id,
                "locator": ref.locator,
                "publication_position": ref.publication_position,
                "component_position": assertion.component_position,
                "fixed": assertion.origin is AssertionOrigin.FIXED_STATEMENT,
                "matches_step_conclusion": assertion.content == step.conclusion,
            })
        position_status = evaluate_publication(
            citing_id,
            [source["assertion_id"] for source in sources],
            lambda source_id, target_id: precedes_citing_assertion(unscreened, source_id, target_id),
        )
        given_entries.append({
            "step_index": index,
            "source_count": len(sources),
            "sources": sources,
            "publication_check": position_status,
            "all_fixed_and_matching": bool(sources) and all(
                source["fixed"] and source["matches_step_conclusion"] for source in sources
            ),
        })

    status_counts = {key: sum(row["publication_check"] == key for row in given_entries)
                     for key in ("PRIOR", "UNVERIFIABLE_TARGET", "NOT_PRIOR", "MISSING_LINK")}
    given_provenance_ok = all(row["all_fixed_and_matching"] for row in given_entries)
    publication_certified = (status_counts["PRIOR"] == len(given_entries)
                             and bool(given_entries))
    record = {
        "steps": len(model.steps),
        "inference_steps": sum(s.rule is ProofRule.INFERENCE for s in model.steps),
        "given_count": len(given_entries),
        "citing_target": citing_info,
        "position_counts": status_counts,
        "publication_certified": publication_certified,
        "fixed_link_coverage": given_provenance_ok,
        "fulltext_equal": rendered == baseline,
        "citation_numbers_equal": source_nums == model_nums,
        "benchmark_ok": benchmark_ok,
        "given_entries": given_entries,
    }
    (OUTPUT / f"{name}_current.md").write_text(rendered, encoding="utf-8")
    print(f"{name} GIVEN={len(given_entries)} PRIOR={status_counts['PRIOR']} "
          f"UNVERIFIABLE={status_counts['UNVERIFIABLE_TARGET']} "
          f"NOT_PRIOR={status_counts['NOT_PRIOR']} "
          f"TARGET_BOUND={citing_info is not None} "
          f"FULLTEXT={record['fulltext_equal']} CITATIONS={record['citation_numbers_equal']}", flush=True)
    return record


def write_report(report):
    rows = [
        "# Phase 168 R3-41P12 — Publication boundary audit",
        "",
        "本監査は証明対象の文献位置と、使用したGIVENの先行関係を調査する。",
        "アプリ本体と既存テストは変更しない。",
        "",
        "| 群 | GIVEN | PRIOR | TARGET未解決 | NOT_PRIOR | 位置の保証 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for name, value in report.get("cases", {}).items():
        counts = value["position_counts"]
        rows.append(f"| {name} | {value['given_count']} | {counts['PRIOR']} | "
                    f"{counts['UNVERIFIABLE_TARGET']} | {counts['NOT_PRIOR']} | "
                    f"{'確定' if value['publication_certified'] else '未確定'} |")
    rows.extend((
        "", "## 監査上の解釈", "",
        "- PRIOR: 既存の publication_position/component_position 規則に従って先行する。",
        "- UNVERIFIABLE_TARGET: 証明対象の位置付き命題IDを確定できないため文献順を保証しない。",
        "- NOT_PRIOR: 前提が証明対象より前にないことを検出。",
        "- 使用出典の同一性・固定命題との対応は、独立の監査列として確認する。",
        "- 文献位置の判定は数学的な命題の真偽を証明しない。",
        "- R3-41P10のmatcher再検証との統合・本体改修は未実施。",
        "", f"**AUDIT_STATUS**: {report.get('status', 'ERROR')}",
        "**FULL_PYTEST_NOT_RUN**", "",
    ))
    if report.get("error"):
        rows.extend(("## 実行エラー", "", "```", report["error"], "```"))
    (OUTPUT / "audit.md").write_text("\n".join(rows), encoding="utf-8")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {"phase": "R3-41P12", "audit_only": True, "cases": {},
              "status": "ERROR", "total_publication_certified": False}
    try:
        for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
            report["cases"][name] = audit_case(name, n, k)
        content_ok = all(x["fulltext_equal"] and x["citation_numbers_equal"]
                         and x["benchmark_ok"] and x["fixed_link_coverage"]
                         and x["position_counts"]["NOT_PRIOR"] == 0
                         and x["position_counts"]["MISSING_LINK"] == 0
                         for x in report["cases"].values())
        report["total_publication_certified"] = all(
            x["publication_certified"] for x in report["cases"].values()
        )
        # The audit can complete with unbound target positions, but that is
        # explicitly not a certification. A detected violation is a failure.
        report["status"] = "PASS" if content_ok else "FAIL"
    except Exception:
        report["error"] = traceback.format_exc()
        print("AUDIT_ERROR " + report["error"], file=sys.stderr, flush=True)
    finally:
        (OUTPUT / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        write_report(report)
        print("REPORT", OUTPUT / "audit.md", flush=True)
        print("AUDIT_STATUS", report["status"], flush=True)
        print("PUBLICATION_CERTIFIED", report["total_publication_certified"], flush=True)
        print("APPLICATION_SOURCE_UNCHANGED", flush=True)
        print("FULL_PYTEST_NOT_RUN", flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
