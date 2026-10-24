"""Audit only: trust-boundary invocation, independent model entry, and guards.

No application files, existing tests, registries or baselines are modified.
Synthetic routes mock internal collaborators to characterize control flow; they
are not demonstrations of remote-input exploits or certificates of mathematics.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import re
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (("pi3_2", 2, 1, (13, 5)),
         ("pi4_3", 3, 1, (19, 6)),
         ("pi5_4", 4, 1, (7, 3)))
WATCHED = (
    "web_group_proof.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r2_search_adapter.py",
    "phase165_r52_partial_proof.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_41p13_trust_boundary/verification.py",
    "phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi3_2.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi4_3.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi5_4.md",
)


def watched_hashes() -> dict[str, str]:
    """Track application/test/baseline integrity across this read-only run."""
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in WATCHED
    }


def probe_web_route(*, context: bool, positioned: bool,
                    unsupported_rule: bool = False, partial: bool = False,
                    reject: bool = False) -> dict[str, object]:
    """Observe a synthetic search handoff using mocked collaborators.

    This changes no global code outside the lifetime of the mock context.
    It intentionally supplies an artificial PartialProofResult to exercise the
    exact branch conditions in the standard Web entry point.
    """
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from proof import ProofRule, ProofStep
    from web_group_proof import build_standard_web_group_proof_view
    from phase168_r3_41p13_trust_boundary import UnverifiedProofTree

    status = ProofSearchStatus.PARTIAL if partial else ProofSearchStatus.COMPLETE
    rule = ProofRule.RELATION if unsupported_rule else ProofRule.GIVEN
    step = ProofStep(conclusion="synthetic target", premises=(), rule=rule)
    result = make_partial_proof_result(
        n=2, k=1, status=status,
        proven_steps=(step,),
        open_goals=("unsolved synthetic child",) if partial else (),
        diagnostics=("unresolved",) if partial else (),
        conclusion=None if partial else step.conclusion,
    )
    unscreened = object()
    screened = object()
    projected = object()
    view = object()
    calls = {"verify": 0, "resolve": 0, "model": 0, "render": 0,
             "used_screened_bridge": False}

    def search(*, context_sink=None, **kwargs):
        if context and context_sink is not None:
            context_sink(screened)
        return result

    def resolve(*args, **kwargs):
        calls["resolve"] += 1
        return "synthetic:target" if positioned else None

    def verify(*args, **kwargs):
        calls["verify"] += 1
        if reject:
            raise UnverifiedProofTree("synthetic unverified tree")
        return (0, 1)

    def model_project(searched, bridge):
        calls["model"] += 1
        calls["used_screened_bridge"] = bridge is screened
        return projected

    def render(searched, *, narrative_model=None, **kwargs):
        calls["render"] += 1
        if searched is not result or narrative_model is not projected:
            raise AssertionError("unexpected result/model identity")
        return view

    with (
        patch("phase165_r52_r9_shared_math.build_shared_typed_bridge",
              return_value=unscreened),
        patch("phase165_r55_nk_only_goal.search_group_from_registered_goal",
              side_effect=search),
        patch("phase166_r3t_goal_source_binding.goal_source.resolve_specialized_goal_citing_id",
              side_effect=resolve),
        patch("phase168_r3_41p13_trust_boundary.verify_proof_tree_for_narrative",
              side_effect=verify),
        patch("phase168_r3_4_link_bridge.build_linked_proof_narrative_model",
              side_effect=model_project),
        patch("phase165_r52_r3_web_adapter.build_partial_web_group_proof_view",
              side_effect=render),
    ):
        rejected = False
        try:
            actual = build_standard_web_group_proof_view(n=2, k=1)
        except UnverifiedProofTree:
            rejected = True
        else:
            if actual is not view:
                raise AssertionError("public Web route returned unexpected view")
    return {
        "status": status.value,
        "screened_context_supplied": context,
        "citing_position_supplied": positioned,
        "unsupported_step_rule": unsupported_rule,
        "verification_forced_reject": reject,
        "rejected": rejected,
        **calls,
    }


def probe_raw_model() -> dict[str, object]:
    """Demonstrate that a bare Model is storage, not a verification seal."""
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from proof import ProofRule, ProofStep

    fabricated = ProofStep(
        conclusion="invented source assertion", premises=(), rule=ProofRule.GIVEN,
    )
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fabricated,), conclusion=fabricated.conclusion,
    )
    model = build_proof_narrative_model(result)
    return {
        "bare_model_accepts_unregistered_given": any(
            step is fabricated for step in model.steps
        ),
        "model_has_trust_certificate": hasattr(model, "verified")
        or hasattr(model, "validation_certificate"),
        "step_count": len(model.steps),
    }


def probe_supplied_rule() -> dict[str, object]:
    """Check that the generic matcher does not authenticate rule registration.

    An artificial zero-premise rule can validate its own output, as documented
    by R3-41P13's scope. This is not reachable merely by sending (n,k) to the
    canonical search; it illustrates why generic Model trust is not established.
    """
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from proof import InferenceRule, ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, LiteratureEntry, ReferenceKind,
        UnifiedStatementRegistry,
    )

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="synthetic_target_ref", kind=ReferenceKind.PROPOSITION,
        locator="Synthetic target", publication_position=100,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="synthetic_target", reference_id="synthetic_target_ref",
        kind=AssertionKind.STATEMENT, content="invented conclusion",
    ))
    bridge = RegistryBridgeResult(registry, (), ())
    forged_rule = InferenceRule(
        name="unregistered artificial zero-premise rule",
        conclusion_builder=lambda premises: "invented conclusion",
    )
    fabricated = ProofStep(
        conclusion="invented conclusion", premises=(), rule=ProofRule.INFERENCE,
        inference_rule=forged_rule,
    )
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fabricated,), conclusion="invented conclusion",
    )
    counts = verify_proof_tree_for_narrative(
        result, bridge, citing_assertion_id="synthetic_target",
    )
    return {
        "self_supplied_rule_accepted_by_generic_matcher": counts == (1, 0),
        "counts": list(counts),
        "registered_rule_identity_was_checked": False,
    }



def probe_supplied_bridge() -> dict[str, object]:
    """Show that a caller-supplied registry is not a trusted search provenance.

    The artificial source is entered by the same test as the artificial target.
    The check proves only consistency with *that supplied* bridge, not that it
    came from the canonical publication-screening step.
    """
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from proof import ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin,
        LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
    )

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="synthetic_source_ref", kind=ReferenceKind.PROPOSITION,
        locator="Synthetic source", publication_position=100,
    ))
    registry.add_reference(LiteratureEntry(
        reference_id="synthetic_target_ref", kind=ReferenceKind.PROPOSITION,
        locator="Synthetic target", publication_position=200,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="synthetic_source", reference_id="synthetic_source_ref",
        kind=AssertionKind.STATEMENT, content="artificial GIVEN",
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="synthetic_target", reference_id="synthetic_target_ref",
        kind=AssertionKind.STATEMENT, content="a different target",
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    fabricated = ProofStep(
        conclusion="artificial GIVEN", premises=(), rule=ProofRule.GIVEN,
    )
    bridge = RegistryBridgeResult(registry, (), (
        ProofStepLink(assertion_id="synthetic_source", step=fabricated),
    ))
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fabricated,), conclusion=fabricated.conclusion,
    )
    counts = verify_proof_tree_for_narrative(
        result, bridge, citing_assertion_id="synthetic_target",
    )
    return {
        "caller_supplied_bridge_can_authorize_its_own_given": counts == (0, 1),
        "counts": list(counts),
        "target_assertion_matches_conclusion": (
            registry.assertion("synthetic_target").content == result.conclusion
        ),
    }


def probe_projection_guards() -> dict[str, bool]:
    """Verify both existing presentation-side shape gates remain active."""
    from phase168_r3_27_typed_statement_projection import (
        project_stable_eta_notation_transition, typed_sentence,
    )

    def calls_name(fn, name):
        source = inspect.getsource(fn)
        parsed = ast.parse(source)
        return any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == name
            for node in ast.walk(parsed)
        )

    return {
        "stable_eta_shape_guard_present": calls_name(
            project_stable_eta_notation_transition, "_stable_eta_renaming_shape"
        ),
        "prop42_exactness_guard_present": calls_name(
            typed_sentence, "prop42_exactness_indices"
        ),
    }


def probe_real_proofs() -> dict[str, dict]:
    """Check the three published baseline groups, including inline citations."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

    bridge = build_shared_typed_bridge()
    output = {}
    for name, n, k, expected in CASES:
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        if result.status is not ProofSearchStatus.COMPLETE or not contexts:
            raise AssertionError("expected complete contextual proof: " + name)
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        if citing is None:
            raise AssertionError("positioned target missing: " + name)
        counts = verify_proof_tree_for_narrative(
            result, contexts[-1], citing_assertion_id=citing,
        )
        rendered, model, view = capture(n, k)
        original = (
            ROOT / "phase168_r3_41p12_publication_boundary_audit" / "baselines"
            / (name + ".md")
        ).read_text(encoding="utf-8")
        reference, proof = sections(rendered)
        citation_numbers = {int(x) for x in re.findall(r"\[R(\d+)\]", proof)}
        model_numbers = {c.number for c in model.citations}
        row = {
            "proof_steps": len(model.steps),
            "inference_count": counts[0],
            "given_count": counts[1],
            "expected_counts": list(expected),
            "counts_match": counts == expected,
            "fulltext_equal": rendered == original,
            "citation_numbers_equal": citation_numbers == model_numbers,
            "reference_section_present": bool(reference),
            "proof_section_present": bool(proof),
            "web_partial": bool(view.partial_result),
        }
        output[name] = row
        if not all((row["counts_match"], row["fulltext_equal"],
                    row["citation_numbers_equal"], row["reference_section_present"],
                    row["proof_section_present"], not row["web_partial"])):
            raise AssertionError("real fulltext/citation regression: " + name)
        (OUTPUT / (name + "_current.md")).write_text(rendered, encoding="utf-8")
    return output


def report_markdown(report: dict) -> str:
    cases = report.get("cases", {})
    routes = report.get("routes", {})
    lines = [
        "# Phase 168 R3-41P14 — Trust Boundary 経路監査", "",
        "本監査は読み取り専用。アプリ本体、既存テスト、固定基準は変更しない。", "",
        "## 3群の監査", "",
        "| 群 | 推論 | GIVEN | 本文・Reference全文一致 | Citation |",
        "|---|---:|---:|---|---|",
    ]
    for name, row in cases.items():
        lines.append(
            f'| {name} | {row["inference_count"]} | {row["given_count"]} | '
            f'{row["fulltext_equal"]} | {row["citation_numbers_equal"]} |'
        )
    lines += ["", "## 標準Web経路の人工入力による境界監査", "",
              "※内部関数をモックした構造テストであり、外部ユーザーからの攻撃可能性を立証するものではない。", "",
              "| ケース | 検証呼出 | Model構築 | 拒否 |",
              "|---|---:|---:|---|"]
    for name, row in routes.items():
        lines.append(
            f'| {name} | {row["verify"]} | {row["model"]} | {row["rejected"]} |'
        )
    raw = report.get("raw_model", {})
    supplied = report.get("supplied_rule", {})
    guards = report.get("projection_guards", {})
    bridge = report.get("supplied_bridge", {})
    lines += [
        "", "## 非認証Modelと検証関数の境界", "",
        f'- 未登録GIVENを直接Modelへ格納可能: `{raw.get("bare_model_accepts_unregistered_given")}`',
        f'- Model自身の信頼証明を確認できる: `{raw.get("model_has_trust_certificate")}`',
        f'- 自作推論規則が汎用matcherを通過: `{supplied.get("self_supplied_rule_accepted_by_generic_matcher")}`',
        f'- 人工Bridgeを渡してGIVENを検証可能: `{bridge.get("caller_supplied_bridge_can_authorize_its_own_given")}`',
        f'- 人工Bridgeの対象命題と結果の一致: `{bridge.get("target_assertion_matches_conclusion")}`',
        "- 人工Bridgeは正規のscreened bridgeを模した入力であって、公開Webの証明入力ではない。",
        "- 自作規則テストは正規のBackward Searchによる規則生成を偽装していない。",
        "- P13の関数は任意のルール集合についての独立した証明検証器ではない。",
        "", "## Rendererに残る2つの防御", "",
        f'- Stable eta の形状チェック: `{guards.get("stable_eta_shape_guard_present")}`',
        f'- Proposition 4.2 完全性の形状チェック: `{guards.get("prop42_exactness_guard_present")}`',
        "", "## 設計上の判断", "",
        "- Complete の検証適用条件は fail-closed（検証不能なら拒否）にする必要がある。",
        "- partial と明示的な互換APIを今回の変更対象へ拡大しない。",
        "- 公開Web経路のTrust Boundaryだけを改善しても、任意のModelの数学的健全性は保証しない。",
        "- Rendererの2チェックは信頼境界が全経路で確立するまで維持する。",
        "- 今回は監査のみ。次工程で既存API・表示を保つ最小改修を検討する。",
        "- 全体pytestはPhase終了時まで実行しない。",
        "", f'**AUDIT_STATUS**: `{report.get("status", "ERROR")}`',
        "", "**FULL_PYTEST_NOT_RUN**", "",
    ]
    if report.get("error"):
        lines += ["## エラー", "", "```", report["error"], "```", ""]
    return "\n".join(lines)


def main() -> int:
    import traceback
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {"phase": "168 R3-41P14", "mode": "AUDIT_ONLY",
              "status": "ERROR", "cases": {}, "routes": {}}
    try:
        start = watched_hashes()
        report["source_sha256_before"] = start
        report["cases"] = probe_real_proofs()
        probes = {
            "positioned_complete": dict(context=True, positioned=True),
            "missing_context": dict(context=False, positioned=True),
            "missing_citing_position": dict(context=True, positioned=False),
            "unsupported_rule": dict(context=True, positioned=True,
                                     unsupported_rule=True),
            "validator_rejection": dict(context=True, positioned=True, reject=True),
            "partial": dict(context=True, positioned=True, partial=True),
        }
        report["routes"] = {
            name: probe_web_route(**options) for name, options in probes.items()
        }
        report["raw_model"] = probe_raw_model()
        report["supplied_rule"] = probe_supplied_rule()
        report["supplied_bridge"] = probe_supplied_bridge()
        report["projection_guards"] = probe_projection_guards()
        end = watched_hashes()
        report["source_sha256_after"] = end
        if start != end:
            raise AssertionError("read-only audit unexpectedly changed a watched file")
        route = report["routes"]
        expected = {
            "positioned_complete": (1, 1, False),
            "missing_context": (0, 1, False),
            "missing_citing_position": (0, 1, False),
            "unsupported_rule": (0, 1, False),
            "validator_rejection": (1, 0, True),
            "partial": (0, 1, False),
        }
        for name, (verify, model, reject) in expected.items():
            entry = route[name]
            if (entry["verify"], entry["model"], entry["rejected"]) != (verify, model, reject):
                raise AssertionError("unexpected route behavior: " + name)
        if not (report["raw_model"]["bare_model_accepts_unregistered_given"]
                and report["supplied_rule"]["self_supplied_rule_accepted_by_generic_matcher"]
                and report["supplied_bridge"]["caller_supplied_bridge_can_authorize_its_own_given"]
                and not report["supplied_bridge"]["target_assertion_matches_conclusion"]
                and all(report["projection_guards"].values())):
            raise AssertionError("unexpected raw model, matcher or projection guard behavior")
        report["status"] = "BOUNDARY_GAPS_CONFIRMED"
    except Exception:
        report["error"] = traceback.format_exc()
    finally:
        (OUTPUT / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (OUTPUT / "audit.md").write_text(report_markdown(report), encoding="utf-8")
        for name, row in report.get("routes", {}).items():
            print("ROUTE", name, "VERIFY", row["verify"],
                  "MODEL", row["model"], "REJECT", row["rejected"], flush=True)
        for name, row in report.get("cases", {}).items():
            print("REAL", name, "INFERENCE", row["inference_count"],
                  "GIVEN", row["given_count"],
                  "FULLTEXT", row["fulltext_equal"],
                  "CITATIONS", row["citation_numbers_equal"], flush=True)
        if report.get("error"):
            print("AUDIT_ERROR", report["error"], flush=True)
        print("AUDIT_STATUS", report["status"], flush=True)
        print("APPLICATION_SOURCE_UNCHANGED", flush=True)
        print("FULL_PYTEST_NOT_RUN", flush=True)
    return 0 if report["status"] == "BOUNDARY_GAPS_CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
