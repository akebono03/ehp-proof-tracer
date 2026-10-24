"""Phase 168 R3-41P10: audit-only generic ProofStep replay at the Model boundary.

This module does not modify application modules, ProofSteps, or existing tests.
The prototype deliberately replays inference matching: it is NOT a certificate
and NOT an implementation recommendation without evaluating its costs.
"""
from __future__ import annotations

import json
import traceback
from dataclasses import replace
from pathlib import Path
from time import perf_counter
from typing import Any

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))


def normalized_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def primitive_step_role(step: Any) -> str:
    """Return a descriptive role, without inferring validity."""
    from proof import ProofRule
    if step.rule is ProofRule.INFERENCE:
        return "INFERENCE"
    if step.rule is ProofRule.GIVEN:
        return "GIVEN"
    return str(getattr(step.rule, "value", step.rule))


def replay_model_inferences(model: Any) -> dict[str, Any]:
    """Prototype an *optional* generic boundary check using existing matchers.

    Every inference must use premises present by identity in the Model, pass
    the existing rule matcher, and reproduce its typed conclusion. Non-inference
    steps are counted, not certified. This is mathematical RE-validation and is
    intentionally AUDIT-ONLY, not part of the renderer or model builder.
    """
    from proof import ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step

    steps = model.steps
    items: list[dict[str, Any]] = []
    counts: dict[str, int] = {"INFERENCE": 0, "GIVEN": 0, "OTHER": 0}
    started = perf_counter()
    for index, step in enumerate(steps):
        role = primitive_step_role(step)
        counts[role if role in counts else "OTHER"] += 1
        if step.rule is not ProofRule.INFERENCE:
            continue
        row: dict[str, Any] = {
            "step_index": index,
            "conclusion_type": type(step.conclusion).__name__,
            "premise_count": len(step.premises),
            "rule_name": getattr(step.inference_rule, "name", None),
        }
        if step.inference_rule is None:
            row.update({"accepted": False, "failure": "MISSING_RULE"})
            items.append(row)
            continue
        if any(not any(parent is present for present in steps) for parent in step.premises):
            row.update({"accepted": False, "failure": "PREMISE_NOT_IN_MODEL"})
            items.append(row)
            continue
        try:
            matches = find_inference_matches_for_rule(step.inference_rule, step.premises)
            matched = tuple(
                match for match in matches
                if len(match.premises) == len(step.premises)
                and all(found is actual for found, actual in zip(match.premises, step.premises))
            )
            produces = [
                derive_inference_proof_step(match).conclusion == step.conclusion
                for match in matched
            ]
            row["matching_premise_bindings"] = len(matched)
            row["accepted"] = any(produces)
            if not row["accepted"]:
                row["failure"] = "CONCLUSION_MISMATCH" if matched else "RULE_MATCH_REJECTED"
        except Exception as error:
            row.update({"accepted": False, "failure": type(error).__name__, "error": str(error)})
        items.append(row)
    elapsed = round((perf_counter() - started) * 1000, 3)
    return {
        "step_count": len(steps),
        "roles": counts,
        "replayed_count": len(items),
        "accepted_count": sum(1 for item in items if item["accepted"]),
        "all_inferences_accepted": all(item["accepted"] for item in items),
        "milliseconds": elapsed,
        "failures": [item for item in items if not item["accepted"]],
        "details": items,
        "given_certified": False,
    }


def construct_counterfeits(genuine_pi43_model: Any) -> dict[str, Any]:
    """Build two falsified results that the existing generic dataclasses admit."""
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase166_r3ac_stable_notation import stable_eta_notation_rule
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from proof import ProofRule, ProofStep, Relation
    from toda_rules import toda_eta_family_definition_statement

    source_eta = toda_eta_family_definition_statement(3).element
    wrong_eta = toda_eta_family_definition_statement(4).element
    target_group = TodaPrimaryGroup(6, 5)
    transported = Relation(target_group, FiniteCyclicGroup(2, IteratedSuspension(source_eta, 2)))
    wrong_goal = Relation(target_group, FiniteCyclicGroup(2, wrong_eta))
    source_step = ProofStep(transported, (), ProofRule.GIVEN)
    definition_step = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    bad_stable = ProofStep(
        wrong_goal, (source_step, definition_step), ProofRule.INFERENCE,
        inference_rule=stable_eta_notation_rule(wrong_goal),
    )
    stable_result = make_partial_proof_result(
        n=5, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(source_step, definition_step, bad_stable),
        conclusion=wrong_goal,
    )
    stable_model = build_proof_narrative_model(stable_result)
    stable_replay = replay_model_inferences(stable_model)

    original = next(
        step for step in genuine_pi43_model.steps
        if isinstance(step.conclusion, EHPImageEqualsKernelStatement)
        and step.rule is ProofRule.INFERENCE
    )
    old_window = original.conclusion.window
    old_target = old_window.target_term
    bad_target = TodaPrimaryGroup(
        old_target.group_dimension + 1, old_target.sphere_dimension,
    )
    bad_ehp_conclusion = EHPImageEqualsKernelStatement(
        replace(old_window, target_term=bad_target)
    )
    bad_ehp = replace(original, conclusion=bad_ehp_conclusion)
    ehp_steps = genuine_pi43_model.steps + (bad_ehp,)
    ehp_result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=ehp_steps, conclusion=bad_ehp_conclusion,
    )
    ehp_model = build_proof_narrative_model(ehp_result)
    ehp_replay = replay_model_inferences(ehp_model)
    relevant_failures = [
        item for item in ehp_replay["failures"]
        if item["step_index"] == len(ehp_steps) - 1
    ]
    return {
        "stable_eta": {
            "partial_result_accepted": True,
            "model_accepted": True,
            "generic_replay_rejects": not stable_replay["all_inferences_accepted"],
            "failure": stable_replay["failures"],
        },
        "ehp_exactness": {
            "partial_result_accepted": True,
            "model_accepted": True,
            "generic_replay_rejects": bool(relevant_failures),
            "failure": relevant_failures,
        },
    }


def render_summary(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 168 R3-41P10 — Generic ProofStep replay (audit only)",
        "",
        "この監査は、既存 matcher による Model 入口での一括検証を試作する。",
        "証明済みの証拠を新規発行するものではなく、探索後に数学的検証を再実行する方式である。",
        "",
        "| 群 | 推論 Step | 汎用再検証 PASS | 時間(ms) | 前回全文一致 | Citation |",
        "|---|---:|---:|---:|---|---|",
    ]
    for name, case in report.get("cases", {}).items():
        x = case.get("replay", {})
        lines.append(
            f'| {name} | {x.get("replayed_count", "?")} | '
            f'{x.get("accepted_count", "?")} | {x.get("milliseconds", "?")} | '
            f'{case.get("fulltext_equal", False)} | {case.get("citations_ok", False)} |'
        )
    lines += ["", "## 人工的な偽の推論"]
    for name, case in report.get("counterfeits", {}).items():
        lines.append(
            f'- {name}: Model受け入れ={case.get("model_accepted")}, '
            f'汎用再検証で拒否={case.get("generic_replay_rejects")}, '
            f'失敗内容={case.get("failure")}'
        )
    lines += [
        "",
        "## 信頼境界に関する解釈",
        "- `ProofStep` と `ProofNarrativeModel` 自身は証明済み証明書ではない。",
        "- `find_inference_matches_for_rule()` による再検証は表示から数学を分離できるが、探索時の検証と重複する。",
        "- GIVEN の出典・文献順をこの試作は再認証しない。",
        "- ここで PASS しても全群・全 API について検証済みと宣言するものではない。",
        "- 監査結果を評価するまで、本体の Renderer / Model / Search に変更しない。",
        "",
        f'**AUDIT_STATUS**: {report.get("status")}',
        '**FULL_PYTEST_NOT_RUN**',
        '',
    ]
    if report.get("error"):
        lines += ['```text', report['error'], '```', '']
    return "\n".join(lines)


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    report: dict[str, Any] = {"phase": "R3-41P10", "audit_only": True, "cases": {}, "counterfeits": {}, "status": "ERROR"}
    try:
        from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
        from phase168_r3_39f_frozen_comparison.audit import assess
        actual_models: dict[str, Any] = {}
        for name, n, k in CASES:
            markdown, model, _ = capture(n, k)
            baseline = (PACKAGE / 'baselines' / f'{name}_current.md').read_text(encoding='utf-8-sig')
            replay = replay_model_inferences(model)
            _, proof = sections(markdown)
            citations = {item.number for item in model.citations}
            import re
            cited = {int(value) for value in re.findall(r'\[R(\d+)\]', proof)}
            case = {
                "fulltext_equal": normalized_newlines(markdown) == normalized_newlines(baseline),
                "citations_ok": cited == citations,
                "benchmark_ok": all(item["present"] for item in assess(name, proof)),
                "replay": replay,
            }
            report['cases'][name] = case
            actual_models[name] = model
            (OUTPUT / f'{name}_current.md').write_text(markdown, encoding='utf-8')
            print(f'{name} INFERENCE={replay["replayed_count"]} MATCHED={replay["accepted_count"]} '
                  f'REPLAY_OK={replay["all_inferences_accepted"]} '
                  f'FULLTEXT={case["fulltext_equal"]} CITATIONS={case["citations_ok"]} '
                  f'MS={replay["milliseconds"]}', flush=True)
        report['counterfeits'] = construct_counterfeits(actual_models['pi4_3'])
        for name, item in report['counterfeits'].items():
            print(f'COUNTERFEIT {name} MODEL_ACCEPTS={item["model_accepted"]} '
                  f'REPLAY_REJECTS={item["generic_replay_rejects"]}', flush=True)
        all_cases = all(
            case['fulltext_equal'] and case['citations_ok'] and case['benchmark_ok']
            and case['replay']['all_inferences_accepted']
            for case in report['cases'].values()
        ) and len(report['cases']) == len(CASES)
        all_forgery = all(
            item['model_accepted'] and item['generic_replay_rejects']
            for item in report['counterfeits'].values()
        ) and len(report['counterfeits']) == 2
        report['status'] = 'PASS' if all_cases and all_forgery else 'FAIL'
    except Exception:
        report['error'] = traceback.format_exc()
        report['status'] = 'ERROR'
    (OUTPUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    (OUTPUT / 'audit.md').write_text(render_summary(report), encoding='utf-8')
    if report.get('error'):
        print('AUDIT_ERROR', report['error'], flush=True)
    print('AUDIT_STATUS', report['status'], flush=True)
    print('REPORT', OUTPUT / 'audit.md', flush=True)
    print('APPLICATION_SOURCE_UNCHANGED', flush=True)
    print('FULL_PYTEST_NOT_RUN', flush=True)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
