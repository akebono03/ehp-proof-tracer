"""Observe proof-step origins and screened-bridge identity without changing search.

This is a runtime boundary audit, not an independently trusted certificate.
It deliberately never marks a ProofStep or a Narrative Model as verified.
"""
from __future__ import annotations

import hashlib
import json
import re
import traceback
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (
    ("pi3_2", 2, 1, (13, 5)),
    ("pi4_3", 3, 1, (19, 6)),
    ("pi5_4", 4, 1, (7, 3)),
)
WATCHED = (
    "web_group_proof.py",
    "proof.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r2_search_adapter.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r52_partial_proof.py",
    "phase165_r55_nk_only_goal.py",
    "phase166_r3c_publication_order.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_41p13_trust_boundary/verification.py",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi3_2.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi4_3.md",
    "phase168_r3_41p12_publication_boundary_audit/baselines/pi5_4.md",
)


def source_hashes() -> dict[str, str]:
    """Detect unexpected mutations of the real modules and frozen baselines."""
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in WATCHED
    }


def observe_search_origin(n: int, k: int) -> tuple[object, object, object, dict]:
    """Trace factory outputs, search observations and exact bridge identity.

    Monkey patches wrap (not replace) the normal implementations. The
    recursive matcher, constructor, search and publication checks still run.
    The result is diagnostic evidence only: an arbitrary caller can supply
    its own expansion provider or bridge through other public Python APIs.
    """
    import phase165_r3_recursive_search as recursive
    import phase165_r52_r2_search_adapter as adapter
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    bridge = build_shared_typed_bridge()
    screened_contexts = []
    reconstructed = []
    derived_objects: dict[int, object] = {}
    observed_objects: set[int] = set()
    real_constructor = recursive.derive_inference_proof_step
    real_reconstruct = adapter.reconstruct_registered_goal

    def track_constructor(match):
        step = real_constructor(match)
        derived_objects[id(step)] = step
        return step

    def track_reconstruction(*args, **kwargs):
        reconstructed.append((args[0], args[1], args[2]))
        existing = kwargs.get("progress_observer")

        def observed(kind, target, step):
            if kind == "proved" and step is not None:
                observed_objects.add(id(step))
            if existing is not None:
                existing(kind, target, step)

        kwargs["progress_observer"] = observed
        return real_reconstruct(*args, **kwargs)

    with (
        patch.object(recursive, "derive_inference_proof_step", side_effect=track_constructor),
        patch.object(adapter, "reconstruct_registered_goal", side_effect=track_reconstruction),
    ):
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=screened_contexts.append,
        )

    if result.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError(f"Expected complete real search, got {result.status}")
    if not screened_contexts:
        raise AssertionError("Canonical search did not publish a screened context")
    screened = screened_contexts[-1]
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise AssertionError("Canonical group goal has no positioned citation target")

    inferred = tuple(step for step in result.proven_steps if step.rule is ProofRule.INFERENCE)
    givens = tuple(step for step in result.proven_steps if step.rule is ProofRule.GIVEN)
    unsupported = tuple(step for step in result.proven_steps
                        if step.rule not in (ProofRule.INFERENCE, ProofRule.GIVEN))
    derived_in_search = sum(derived_objects.get(id(step)) is step for step in inferred)
    emitted_as_proved = sum(id(step) in observed_objects for step in result.proven_steps)
    real_bridge_used = any(
        candidate is screened and type(goal) is type(result.conclusion)
        and goal == result.conclusion and assertion_id == citing
        for goal, candidate, assertion_id in reconstructed
    )
    screened_given = 0
    screened_given_identity = 0
    prior_given = 0
    for step in givens:
        valid_links = []
        for link in screened.proof_links:
            if link.step is None or link.step != step:
                continue
            assertion = screened.registry.assertion(link.assertion_id)
            if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
                continue
            if type(assertion.content) is not type(step.conclusion):
                continue
            if assertion.content != step.conclusion:
                continue
            valid_links.append(link)
        if valid_links:
            screened_given += 1
            if any(link.step is step for link in valid_links):
                screened_given_identity += 1
            if any(precedes_citing_assertion(screened, link.assertion_id, citing)
                   for link in valid_links):
                prior_given += 1

    counts = (len(inferred), len(givens))
    data = {
        "steps": len(result.proven_steps),
        "inference_count": counts[0],
        "given_count": counts[1],
        "unsupported_count": len(unsupported),
        "factory_output_identity_count": derived_in_search,
        "observer_proved_identity_count": emitted_as_proved,
        "screened_given_link_count": screened_given,
        "screened_given_object_identity_count": screened_given_identity,
        "prior_given_count": prior_given,
        "search_received_the_same_screened_bridge": real_bridge_used,
        "search_reconstruction_calls": len(reconstructed),
        "factory_output_total": len(derived_objects),
        "citing_assertion_id": citing,
        "verification_token_recorded_in_result": False,
    }
    return result, screened, bridge, data


def audit_case(name: str, n: int, k: int, expected: tuple[int, int]) -> dict:
    """Check origin observations, existing checker and frozen Web narrative."""
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model

    result, screened, original, row = observe_search_origin(n, k)
    expected_steps = sum(expected)
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    checked = verify_proof_tree_for_narrative(
        result, screened, citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, screened)
    rendered, public_model, view = capture(n, k)
    baseline = (ROOT / "phase168_r3_41p12_publication_boundary_audit"
                / "baselines" / (name + ".md")).read_text(encoding="utf-8")
    references, proof = sections(rendered)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / (name + "_current.md")).write_text(rendered, encoding="utf-8")
    (OUTPUT / (name + "_reference.txt")).write_text(references, encoding="utf-8")
    (OUTPUT / (name + "_proof.txt")).write_text(proof, encoding="utf-8")
    used_citations = {int(x) for x in re.findall(r"\[R(\d+)\]", proof)}
    model_citations = {c.number for c in public_model.citations}

    row.update({
        "verification_counts": list(checked),
        "expected_counts": list(expected),
        "model_step_identity_preserved": all(
            left is right for left, right in zip(result.proven_steps, model.steps)
        ) and len(result.proven_steps) == len(model.steps),
        "web_fulltext_equal": rendered == baseline,
        "citation_numbers_equal": used_citations == model_citations,
        "web_partial": view.partial_result,
        "reference_section_present": bool(references),
        "proof_section_present": bool(proof),
    })
    required = (
        row["steps"] == expected_steps,
        row["inference_count"] == expected[0],
        row["given_count"] == expected[1],
        row["unsupported_count"] == 0,
        row["factory_output_identity_count"] == expected[0],
        row["observer_proved_identity_count"] == expected_steps,
        row["screened_given_link_count"] == expected[1],
        row["prior_given_count"] == expected[1],
        row["search_received_the_same_screened_bridge"],
        row["verification_counts"] == list(expected),
        row["model_step_identity_preserved"],
        row["web_fulltext_equal"],
        row["citation_numbers_equal"],
        not row["web_partial"],
        row["reference_section_present"],
        row["proof_section_present"],
    )
    row["observed_invariants_pass"] = all(required)
    if not row["observed_invariants_pass"]:
        raise AssertionError("R3-41P16 origin invariant failure for " + name
                             + ": " + json.dumps(row, ensure_ascii=False, default=str))
    return row


def trust_scope_probes() -> dict:
    """Retain known P14 counterexamples and confirm projection guards remain."""
    from phase168_r3_41p14_trust_boundary_audit.audit import (
        probe_raw_model, probe_supplied_bridge, probe_supplied_rule,
        probe_projection_guards,
    )
    rule = probe_supplied_rule()
    bridge = probe_supplied_bridge()
    model = probe_raw_model()
    guards = probe_projection_guards()
    return {
        "generic_matcher_accepts_self_supplied_rule": bool(
            rule["self_supplied_rule_accepted_by_generic_matcher"]
        ),
        "generic_checker_accepts_self_supplied_bridge": bool(
            bridge["caller_supplied_bridge_can_authorize_its_own_given"]
        ),
        "artificial_target_statement_does_not_match_result": not bool(
            bridge["target_assertion_matches_conclusion"]
        ),
        "bare_model_accepts_unregistered_given": bool(
            model["bare_model_accepts_unregistered_given"]
        ),
        "projection_guards_unchanged": all(guards.values()),
        "rule_registry_is_not_an_independent_mathematical_certificate": True,
    }


def render_report(report: dict) -> str:
    lines = [
        "# Phase 168 R3-41P16 — 推論規則・Bridge 由来の監査", "",
        "アプリ本体、既存テスト、既存の固定基準は変更しない。", "",
        "## 実際の3群での経路照合", "",
        "| 群 | INFERENCE | factory 同一オブジェクト | GIVEN | 選別済み Bridge | 入口確認 | 本文一致 |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for name, row in report.get("cases", {}).items():
        lines.append(
            f'| {name} | {row["inference_count"]} | {row["factory_output_identity_count"]} | '
            f'{row["given_count"]} | {row["screened_given_link_count"]} | '
            f'{row["search_received_the_same_screened_bridge"]} | {row["web_fulltext_equal"]} |'
        )
    scope = report.get("scope", {})
    lines += [
        "", "## 信頼境界の限界", "",
        f'- 任意に与えた規則が既存 matcher を通過可能: `{scope.get("generic_matcher_accepts_self_supplied_rule")}`',
        f'- 任意に与えた Bridge が GIVEN を承認可能: `{scope.get("generic_checker_accepts_self_supplied_bridge")}`',
        f'- 任意 Model に未登録 GIVEN を格納可能: `{scope.get("bare_model_accepts_unregistered_given")}`',
        f'- Renderer 側の2つの形状チェックは維持: `{scope.get("projection_guards_unchanged")}`',
        "", "## 次工程に対する設計判断", "",
        "- 正規経路の監査で確認したオブジェクト同一性は、公開 API 全体の信頼性証明ではない。",
        "- Backward Search の導出結果と screened Bridge の由来を結び付ける情報は、現在の PartialProofResult に存在しない。",
        "- 信頼境界の一般化には、探索時に確定した根拠の受け渡し・改変防止と、未認証 Model の区別が必要。",
        "- ゼロ前提の自作規則が既存 matcher で通過するため、単なる再照合は規則自体の正当性を保証しない。",
        "- 数学的検証エンジンや別の規則台帳を追加して解決しない。",
        "- 今回は観測のみで、Renderer の2チェックは除去しない。",
        "- partial・既存 API は変更せず、全体 pytest は Phase 終了まで実行しない。",
        "", f'**AUDIT_STATUS**: `{report.get("status", "ERROR")}`',
        "", "**FULL_PYTEST_NOT_RUN**", "",
    ]
    if "error" in report:
        lines += ["## 実行エラー", "", "```", report["error"], "```", ""]
    return "\n".join(lines)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {"phase": "168 R3-41P16", "mode": "AUDIT_ONLY", "status": "ERROR", "cases": {}}
    try:
        before = source_hashes()
        report["source_sha256_before"] = before
        for name, n, k, expected in CASES:
            row = audit_case(name, n, k, expected)
            report["cases"][name] = row
            print("REAL", name,
                  "INFERENCE", row["inference_count"],
                  "FACTORY", row["factory_output_identity_count"],
                  "GIVEN", row["given_count"],
                  "SCREENED", row["screened_given_link_count"],
                  "SAME_BRIDGE", row["search_received_the_same_screened_bridge"],
                  "FULLTEXT", row["web_fulltext_equal"], flush=True)
        report["scope"] = trust_scope_probes()
        after = source_hashes()
        report["source_sha256_after"] = after
        if before != after:
            raise AssertionError("Application or frozen baseline changed during audit")
        expected_scope = report["scope"]
        if not all(expected_scope.values()):
            raise AssertionError("Previously observed trust boundary caveat changed")
        report["status"] = "ORIGIN_TRACED_LIMITS_CONFIRMED"
    except Exception:
        report["error"] = traceback.format_exc()
        print("AUDIT_ERROR", report["error"], flush=True)
    finally:
        (OUTPUT / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (OUTPUT / "audit.md").write_text(render_report(report), encoding="utf-8")
        print("AUDIT_STATUS", report["status"], flush=True)
        print("APPLICATION_SOURCE_UNCHANGED", flush=True)
        print("FULL_PYTEST_NOT_RUN", flush=True)
    return 0 if report["status"] == "ORIGIN_TRACED_LIMITS_CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
