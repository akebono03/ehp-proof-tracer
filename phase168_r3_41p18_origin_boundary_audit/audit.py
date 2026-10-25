"""Audit experimental origin records without modifying application modules.

This tests the Python-facing trust boundary, not a claim that remote Web users
can reach Python callables or that arbitrary mathematical rules are sound.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re
import traceback

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary import UnverifiedProofTree
from phase168_r3_41p17_origin_handoff.origin_handoff import build_origin_bound_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import InferenceRule, ProofRule, ProofStep
from proof_origin_capture import (
    SearchOriginObservation,
    capture_search_origins,
    note_accepted_search_step,
    note_factory_inference,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (
    ("pi3_2", 2, 1, 13, 5),
    ("pi4_3", 3, 1, 19, 6),
    ("pi5_4", 4, 1, 7, 3),
)
WATCHED = (
    "web_group_proof.py",
    "proof_origin_capture.py",
    "phase164_r8_proofstep_factory.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r2_search_adapter.py",
    "phase165_r52_partial_proof.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r55_nk_only_goal.py",
    "phase168_r3_41p17_origin_handoff/origin_handoff.py",
    "phase168_r3_41p13_trust_boundary/verification.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi3_2.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi4_3.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi5_4.md",
)


def source_hashes() -> dict[str, str]:
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in WATCHED
    }


def search_with_context(n: int, k: int):
    """Use precisely the standard registered goal and the emitted screened bridge."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise AssertionError(f"Expected a completed canonical search for ({n},{k})")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise AssertionError(f"No citing assertion for ({n},{k})")
    return result, contexts[-1], citing


def project(result, screened, citing, observation):
    return build_origin_bound_narrative_model(
        result, screened, citing_assertion_id=citing,
        observation=observation,
    )


def expected_rejection(action, exc_type, fragment: str) -> bool:
    try:
        action()
    except exc_type as exc:
        if fragment not in str(exc):
            raise AssertionError(
                f"Unexpected refusal: {type(exc).__name__}: {exc}"
            ) from exc
        return True
    return False


def audit_real_case(name: str, n: int, k: int, inference: int, given: int) -> dict:
    """Check legitimate origin handoff, closure, fulltext and citation parity."""
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections

    with capture_search_origins() as observation:
        result, screened, citing = search_with_context(n, k)
        model = project(result, screened, citing, observation)
        actual = render_model_backed_narrative_markdown(result, model)
        baseline = (
            ROOT / "phase168_r3_41p12_publication_boundary_audit" /
            "baselines" / (name + ".md")
        ).read_text(encoding="utf-8")
        given_count = sum(step.rule is ProofRule.GIVEN for step in model.steps)
        inference_count = sum(step.rule is ProofRule.INFERENCE for step in model.steps)
        _, proof_section = sections(actual)
        used_numbers = {
            int(number) for number in re.findall(r"\[R(\d+)\]", proof_section)
        }
        citation_numbers = {citation.number for citation in model.citations}
        web_text, web_model, web_view = capture(n, k)
        same_step_objects = (
            len(model.steps) == len(result.proven_steps)
            and all(a is b for a, b in zip(model.steps, result.proven_steps))
        )
        row = {
            "inference_count": inference_count,
            "given_count": given_count,
            "factory_outputs_at_least_inference": observation.factory_output_count >= inference,
            "accepted_steps_at_least_proven": observation.accepted_step_count >= inference + given,
            "same_step_objects": same_step_objects,
            "fulltext_equal": actual == baseline,
            "web_fulltext_equal": web_text == baseline,
            "citations_equal": used_numbers == citation_numbers,
            "web_citations_equal": (
                tuple((c.number, c.reference.locator) for c in web_model.citations)
                == tuple((c.number, c.reference.locator) for c in model.citations)
            ),
            "web_partial": web_view.partial_result,
            "reference_count": len(model.citations),
        }
    row["observation_closed_after_scope"] = observation._closed
    row["closed_observation_rejected"] = expected_rejection(
        lambda: project(result, screened, citing, observation), ValueError, "active search",
    )
    row["expected_counts"] = [inference, given]
    row["all_invariants_pass"] = all((
        inference_count == inference,
        given_count == given,
        row["factory_outputs_at_least_inference"],
        row["accepted_steps_at_least_proven"],
        same_step_objects,
        row["fulltext_equal"],
        row["web_fulltext_equal"],
        row["citations_equal"],
        row["web_citations_equal"],
        not row["web_partial"],
        row["observation_closed_after_scope"],
        row["closed_observation_rejected"],
    ))
    if not row["all_invariants_pass"]:
        raise AssertionError(f"Canonical origin audit failed for {name}: {row}")
    return row


def audit_scope_limits() -> dict:
    """Record accepted and rejected scenarios without altering production code."""
    from homotopy_groups import TodaPrimaryGroup
    from phase163_r4_registry_bridge import RegistryBridgeResult

    with capture_search_origins() as observation:
        result, screened, citing = search_with_context(2, 1)
        real_model = project(result, screened, citing, observation)

        # A caller who can invoke the public note functions may attest its
        # own invented rule and invented accepted step in a live context.
        fabricated = ProofStep(
            conclusion=result.conclusion,
            premises=(),
            rule=ProofRule.INFERENCE,
            inference_rule=InferenceRule(name="invented-origin-claim"),
        )
        not_previously_observed = (
            not observation.contains_factory_step(fabricated)
            and not observation.contains_accepted_step(fabricated)
        )
        forged_result = replace(result, proven_steps=(fabricated,))
        forged_initially_rejected = expected_rejection(
            lambda: project(forged_result, screened, citing, observation),
            UnverifiedProofTree, "not accepted",
        )
        note_factory_inference(fabricated)
        note_accepted_search_step(fabricated)
        self_attested_model = project(forged_result, screened, citing, observation)
        explicit_self_attestation_accepted = (
            len(self_attested_model.steps) == 1
            and self_attested_model.steps[0] is fabricated
        )

        # The handoff checks that a cited assertion exists and that GIVEN
        # sources precede it; it does not bind result.target to the conclusion.
        alternative_target = TodaPrimaryGroup(
            group_dimension=result.target.group_dimension + 11,
            sphere_dimension=result.target.sphere_dimension,
        )
        mislabeled_result = replace(result, target=alternative_target)
        mislabeled_model = project(mislabeled_result, screened, citing, observation)
        mismatched_target_accepted = (
            mislabeled_model.target == alternative_target
            and alternative_target != result.target
        )

        # A new wrapper reusing the same registry and link objects passes;
        # wrapper identity is not bound to the earlier search invocation.
        wrapper = RegistryBridgeResult(
            screened.registry, screened.records, screened.proof_links,
        )
        replacement_bridge_wrapper_accepted = (
            wrapper is not screened
            and len(project(result, wrapper, citing, observation).steps)
            == len(real_model.steps)
        )

        # A caller may reuse the observation for two canonical searches.
        second_result, second_screened, second_citing = search_with_context(3, 1)
        first_still_accepted = (
            len(project(result, screened, citing, observation).steps)
            == len(real_model.steps)
        )
        second_also_accepted = (
            len(project(second_result, second_screened, second_citing, observation).steps)
            == len(second_result.proven_steps)
        )
        observation_aggregates_multiple_searches = (
            first_still_accepted and second_also_accepted
        )

        # A different screened bridge from a different search must not be
        # accepted for a result unless its links happen to share identities.
        cross_bridge_rejected = expected_rejection(
            lambda: project(result, second_screened, citing, observation),
            (UnverifiedProofTree, ValueError, KeyError), "",
        )

        with capture_search_origins() as nested:
            nested_cannot_use_outer = expected_rejection(
                lambda: project(result, screened, citing, observation),
                ValueError, "active search",
            )
            nested_not_observing_outer_steps = (
                not nested.contains_factory_step(fabricated)
                and not nested.contains_accepted_step(fabricated)
            )
        outer_restored = (
            len(project(result, screened, citing, observation).steps)
            == len(real_model.steps)
        )

        manually_created_session_rejected = expected_rejection(
            lambda: project(result, screened, citing, SearchOriginObservation()),
            ValueError, "active search",
        )

    result_row = {
        "forged_step_unseen_before_notes": not_previously_observed,
        "forged_step_rejected_before_notes": forged_initially_rejected,
        "self_attested_forged_inference_accepted": explicit_self_attestation_accepted,
        "inconsistent_result_target_accepted": mismatched_target_accepted,
        "replacement_bridge_wrapper_accepted": replacement_bridge_wrapper_accepted,
        "observation_aggregates_multiple_searches": observation_aggregates_multiple_searches,
        "cross_search_bridge_rejected": cross_bridge_rejected,
        "nested_cannot_reuse_outer_observation": nested_cannot_use_outer,
        "nested_does_not_inherit_outer_steps": nested_not_observing_outer_steps,
        "outer_observation_restored": outer_restored,
        "manual_observation_rejected": manually_created_session_rejected,
    }
    return result_row


def render_report(report: dict) -> str:
    lines = [
        "# Phase 168 R3-41P18 — Origin Observation 信頼境界監査", "",
        "監査のみ。アプリ本体、既存テスト、固定基準は変更しない。", "",
        "## 正規の3群", "",
        "| 群 | INFERENCE | GIVEN | Handoff と公開 Web の全文 | Citation |",
        "|---|---:|---:|---|---|",
    ]
    for name, item in report.get("cases", {}).items():
        lines.append(
            f'| {name} | {item["inference_count"]} | {item["given_count"]} | '
            f'{item["fulltext_equal"] and item["web_fulltext_equal"]} | '
            f'{item["citations_equal"] and item["web_citations_equal"]} |'
        )
    lines += ["", "## Python API の境界と留保", ""]
    for key, value in report.get("limits", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines += [
        "", "## 判断", "",
        "- Factory の生成記録と探索側 proved 通知の同一性は、通常経路の観測根拠として有効。",
        "- ただし note_factory_inference / note_accepted_search_step は外部 Python から呼べるため、由来記録を認証として使えない。",
        "- ContextVar の scope は search invocation と一対一とは限らず、複数探索の記録を混在できる。",
        "- Handoff は Result の target・citing assertion と探索 context の一意な紐付けまで保証していない。",
        "- 異なる Bridge のラッパーが同一リンクを持つ場合、元の Bridge オブジェクトの同一性を検証しない。",
        "- これは in-process Python API の制約であり、外部 Web 攻撃の成立を意味しない。",
        "- R3-41P17 の origin handoff を標準 Web に昇格させたり、R3-41P13 matcher replay を除去したりしない。",
        "- partial と既存 API を維持し、Renderer の数学的ガード2件を残す。",
        "- 次の工程では真正な探索呼出に由来する情報を信頼境界内で束ねる最小設計を行う。",
        "", f'**AUDIT_STATUS**: `{report.get("status")}`',
        "", "**FULL_PYTEST_NOT_RUN**", "",
    ]
    if "error" in report:
        lines += ["## エラー", "", "```", report["error"], "```", ""]
    return "\n".join(lines)


def collect_report() -> dict:
    before = source_hashes()
    report: dict = {
        "phase": "168 R3-41P18", "mode": "AUDIT_ONLY",
        "status": "ERROR", "cases": {}, "source_sha256_before": before,
    }
    for name, n, k, inference, given in CASES:
        row = audit_real_case(name, n, k, inference, given)
        report["cases"][name] = row
        print(
            "REAL", name, "INFERENCE", row["inference_count"],
            "GIVEN", row["given_count"],
            "FULLTEXT", row["fulltext_equal"] and row["web_fulltext_equal"],
            "CITATIONS", row["citations_equal"] and row["web_citations_equal"],
            flush=True,
        )
    limits = audit_scope_limits()
    report["limits"] = limits
    print("LIMITS", " ".join(f"{key}={value}" for key, value in limits.items()), flush=True)
    if not all(limits.values()):
        raise AssertionError("An expected origin boundary observation changed")
    after = source_hashes()
    report["source_sha256_after"] = after
    if before != after:
        raise AssertionError("Application source or baseline changed during audit")
    report["status"] = "ORIGIN_BOUNDARY_GAPS_CONFIRMED"
    return report


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report: dict = {"phase": "168 R3-41P18", "mode": "AUDIT_ONLY", "status": "ERROR"}
    try:
        report = collect_report()
    except Exception:
        report["error"] = traceback.format_exc()
        print("AUDIT_ERROR", report["error"], flush=True)
    finally:
        (OUTPUT / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        (OUTPUT / "audit.md").write_text(render_report(report), encoding="utf-8")
        print("AUDIT_STATUS", report["status"], flush=True)
        print("FULL_PYTEST_NOT_RUN", flush=True)
    return 0 if report["status"] == "ORIGIN_BOUNDARY_GAPS_CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
