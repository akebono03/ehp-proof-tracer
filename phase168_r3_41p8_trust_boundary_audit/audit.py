"""R3-41P8: audit proof-step trust boundary without editing application files.

Synthetic counterfeit ProofSteps are diagnostic inputs, never mathematical facts.
The trusted public search is separately compared to the R3-41P7 fulltexts.
"""
from __future__ import annotations

from dataclasses import replace
import difflib
import hashlib
import json
from pathlib import Path
import re
import traceback
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
FIXTURES = PACKAGE / "fixtures"
CASES = (("pi3_2", 2, 1, 18, 4), ("pi4_3", 3, 1, 25, 4), ("pi5_4", 4, 1, 10, 3))
SOURCE_NAMES = (
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase166_r3ac_stable_notation.py",
    "phase165_r12_r11_prop42_unified.py",
    "phase165_r12_r12_ehp_consequences.py",
)


def hash_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def citation_integrity(model, rendered: str) -> bool:
    from phase168_r3_38_frozen_fulltext_audit.audit import sections
    _, proof = sections(rendered)
    used = {int(x) for x in re.findall(r"\[R(\d+)\]", proof)}
    registered = {c.number for c in model.citations}
    if used != registered:
        return False
    if not all(c.statement_bodies for c in model.citations):
        return False
    if not all(0 <= i < len(model.steps) and c.number in model.step_citation_numbers[i]
               for c in model.citations for i in c.step_indices):
        return False
    return all(any(c.number == number and i in c.step_indices for c in model.citations)
               for i, nums in enumerate(model.step_citation_numbers) for number in nums)


def public_case_audit():
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from phase168_r3_39f_frozen_comparison.audit import assess
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement

    results = {}
    sample = None
    for name, n, k, steps, refs in CASES:
        text, model, _view = capture(n, k)
        expected = (FIXTURES / f"{name}_current.md").read_text(encoding="utf-8-sig")
        (OUTPUT / f"{name}_current.md").write_text(text, encoding="utf-8")
        diff = "".join(difflib.unified_diff(
            expected.splitlines(keepends=True), text.splitlines(keepends=True),
            fromfile=f"R3-41P7/{name}", tofile=f"R3-41P8/{name}",
        ))
        (OUTPUT / f"{name}_fulltext.diff").write_text(diff, encoding="utf-8")
        _, proof = sections(text)
        benchmark = assess(name, proof)
        results[name] = {
            "steps": len(model.steps),
            "reference_count": len(model.citations),
            "fulltext_identical": text == expected,
            "citation_integrity": citation_integrity(model, text),
            "benchmark_pass": all(c["present"] for c in benchmark),
            "premises_present": all(any(s is p or s == p for s in model.steps)
                                    for step in model.steps for p in step.premises),
            "expected_counts": len(model.steps) == steps and len(model.citations) == refs,
        }
        for step in model.steps:
            if sample is None and isinstance(step.conclusion, EHPImageEqualsKernelStatement):
                sample = step
    if sample is None:
        raise AssertionError("No real EHPImageEqualsKernelStatement found in the 3 public searches")
    return results, sample


def stable_eta_counterfeit_probe():
    """Demonstrate why a structurally coherent but unverified model is unsafe."""
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase166_r3ac_stable_notation import stable_eta_notation_rule
    import phase166_r3ac_stable_notation as eta_rules
    from phase168_r3_27_typed_statement_projection import project_stable_eta_notation_transition
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, NarrativeCitation
    from proof import LiteratureReference, ProofRule, ProofStep, Relation
    from toda_rules import toda_eta_family_definition_statement

    source = toda_eta_family_definition_statement(3).element
    correct_target = toda_eta_family_definition_statement(5).element
    counterfeit_target = toda_eta_family_definition_statement(4).element
    group = TodaPrimaryGroup(6, 5)
    transported = Relation(group, FiniteCyclicGroup(2, IteratedSuspension(source, 2)))
    true_goal = Relation(group, FiniteCyclicGroup(2, correct_target))
    fake_goal = Relation(group, FiniteCyclicGroup(2, counterfeit_target))
    transported_step = ProofStep(transported, (), ProofRule.GIVEN)
    definition_step = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    correct_step = ProofStep(true_goal, (transported_step, definition_step), ProofRule.INFERENCE,
                             inference_rule=stable_eta_notation_rule(true_goal))
    fake_step = ProofStep(fake_goal, (transported_step, definition_step), ProofRule.INFERENCE,
                          inference_rule=stable_eta_notation_rule(fake_goal))
    citation = NarrativeCitation(1, LiteratureReference(label="synthetic eta citation"), (1,))
    correct_model = ProofNarrativeModel((transported_step, definition_step, correct_step),
                                       (citation,), ((), (1,), ()), 2)
    fake_model = replace(correct_model, steps=(transported_step, definition_step, fake_step))
    correct_text = project_stable_eta_notation_transition(correct_model, 2)
    fake_text = project_stable_eta_notation_transition(fake_model, 2)
    guard_pass = eta_rules._stable_eta_renaming_shape(transported, fake_goal)
    guard_false = stable_eta_notation_rule(fake_goal).match_guard((transported_step, definition_step), {})
    with patch.object(eta_rules, "_stable_eta_renaming_shape", return_value=True):
        bypass_text = project_stable_eta_notation_transition(fake_model, 2)
    return {
        "model_accepts_counterfeit_step": fake_model.steps[-1] == fake_step,
        "same_typed_group_and_order": transported.lhs == fake_goal.lhs
            and transported.rhs.order == fake_goal.rhs.order,
        "counterfeit_inference_rule_has_matching_conclusion_pattern":
            fake_step.inference_rule.conclusion_pattern == fake_goal,
        "counterfeit_has_definition_citation": bool(fake_model.step_citation_numbers[1]),
        "genuine_projection": correct_text,
        "unverified_rule_guard_accepts_counterfeit": guard_false,
        "original_shape_validator_accepts_counterfeit": guard_pass,
        "current_projection_rejects_counterfeit": fake_text is None,
        "forced_validator_bypass_output": bypass_text,
        "forced_bypass_would_emit_false_equation": bool(bypass_text) and r"\eta_{4}" in bypass_text,
    }


def ehp_counterfeit_probe(real_step):
    """Forge mutually compatible typed premises with invalid EHP indices."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement, ehp_image_equals_kernel_inference_rule,
    )
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase168_r3_27_typed_statement_projection import typed_sentence
    import phase168_r3_27_typed_statement_projection as projection
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
    from proof import ProofRule, ProofStep
    from toda_rules import TodaProp42ExactnessStatement

    valid_window = real_step.conclusion.window
    source = valid_window.source_term
    invalid_window = replace(valid_window, source_term=TodaPrimaryGroup(
        source.group_dimension + 1, source.sphere_dimension,
    ))
    fake_exact = ProofStep(TodaProp42ExactnessStatement(invalid_window), (), ProofRule.GIVEN)
    fake_image = ProofStep(EHPImageEqualsKernelStatement(invalid_window),
                           (fake_exact,), ProofRule.INFERENCE,
                           inference_rule=ehp_image_equals_kernel_inference_rule())
    fake_model = ProofNarrativeModel((fake_exact, fake_image), (), ((), ()), 1)
    guard_pass = fake_image.inference_rule.match_guard(fake_image.premises, {})
    baseline = typed_sentence(real_step.conclusion, real_step)
    counterfeit = typed_sentence(fake_image.conclusion, fake_image)
    with patch.object(projection, "prop42_exactness_indices", return_value=(2, 4, "delta_e")):
        bypass = typed_sentence(fake_image.conclusion, fake_image)
    return {
        "model_accepts_counterfeit_step": fake_model.steps[-1] == fake_image,
        "exactness_premise_window_matches_conclusion":
            fake_exact.conclusion.window == fake_image.conclusion.window,
        "original_indices_are_invalid": prop42_exactness_indices(fake_exact.conclusion) is None,
        "unverified_rule_guard_accepts_counterfeit": guard_pass,
        "real_proof_projection": baseline,
        "current_projection_rejects_counterfeit": counterfeit is None,
        "forced_validator_bypass_output": bypass,
        "forced_bypass_would_emit_false_exactness": bypass is not None,
    }


def evaluate(report):
    cases = report.get("cases", {})
    probes = report.get("counterfeit_probes", {})
    stable = probes.get("stable_eta", {})
    ehp = probes.get("ehp", {})
    checks = [
        len(cases) == len(CASES),
        all(item.get("fulltext_identical") and item.get("citation_integrity")
            and item.get("benchmark_pass") and item.get("premises_present")
            and item.get("expected_counts") for item in cases.values()),
        stable.get("model_accepts_counterfeit_step") is True,
        stable.get("same_typed_group_and_order") is True,
        stable.get("counterfeit_inference_rule_has_matching_conclusion_pattern") is True,
        stable.get("counterfeit_has_definition_citation") is True,
        stable.get("unverified_rule_guard_accepts_counterfeit") is False,
        stable.get("original_shape_validator_accepts_counterfeit") is False,
        stable.get("current_projection_rejects_counterfeit") is True,
        stable.get("forced_bypass_would_emit_false_equation") is True,
        ehp.get("model_accepts_counterfeit_step") is True,
        ehp.get("exactness_premise_window_matches_conclusion") is True,
        ehp.get("original_indices_are_invalid") is True,
        ehp.get("unverified_rule_guard_accepts_counterfeit") is False,
        ehp.get("current_projection_rejects_counterfeit") is True,
        ehp.get("forced_bypass_would_emit_false_exactness") is True,
    ]
    return all(checks), checks


def report_text(report):
    lines = [
        "# Phase 168 R3-41P8 — ProofStep trust boundary audit",
        "",
        "監査のみ。本体コード、既存テスト、データベースを変更しない。",
        "",
        "## 3群の公開表示",
        "",
        "| 群 | ProofStep | Reference | R3-41P7全文一致 | Citation | 固定基準 |",
        "|---|---:|---:|---|---|---|",
    ]
    for name, *_ in CASES:
        c = report.get("cases", {}).get(name, {})
        lines.append(f'| {name} | {c.get("steps")} | {c.get("reference_count")} | '
                     f'{c.get("fulltext_identical")} | {c.get("citation_integrity")} | '
                     f'{c.get("benchmark_pass")} |')
    lines += [
        "", "## 偽の型付き ProofStep を利用した境界テスト", "",
        "ProofNarrativeModel は引用と Step を格納するデータモデルであり、推論規則を適用した証明書ではない。",
        "以下の人工 Step は監査入力に限り、文献や群構造の新しい事実とは扱わない。", "",
    ]
    for name in ("stable_eta", "ehp"):
        lines.append(f"### {name}")
        lines.append("")
        for key, value in report.get("counterfeit_probes", {}).get(name, {}).items():
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
    lines += [
        "## 結論", "",
        "- 公開された3群の証明は維持されている。",
        "- 有効な出典付き Step の存在と、数学的に正しい推論済みであることは別の性質である。",
        "- もし推論規則の guard と同等の検証なしに任意の Model を受理するなら、偽の数学的本文を表示し得る。",
        "- 数学的再検証を完全に追放するには、検証済み Proof Tree からのみ表示へ渡す trust boundary を確定する必要がある。",
        "- この監査は本体の実装変更を行わない。全体 pytest は Phase 終了まで実行しない。",
        "",
        f'監査状態: **{report.get("status", "UNKNOWN")}**', "",
    ]
    return "\n".join(lines)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "R3-41P8", "audit_only": True, "sources": {},
        "cases": {}, "counterfeit_probes": {}, "status": "RUNNING",
    }
    for name in SOURCE_NAMES:
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(str(path))
        report["sources"][name] = hash_bytes(path.read_bytes())
    try:
        cases, ehp_step = public_case_audit()
        report["cases"] = cases
        report["counterfeit_probes"]["stable_eta"] = stable_eta_counterfeit_probe()
        report["counterfeit_probes"]["ehp"] = ehp_counterfeit_probe(ehp_step)
        passed, checks = evaluate(report)
        report["checks"] = checks
        report["status"] = "PASS" if passed else "FAIL"
    except Exception:
        report["status"] = "ERROR"
        report["error"] = traceback.format_exc()
    (OUTPUT / "audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT / "audit.md").write_text(report_text(report), encoding="utf-8")
    for name, value in report.get("cases", {}).items():
        print(f'{name} steps={value["steps"]} refs={value["reference_count"]}'
              f' FULLTEXT={value["fulltext_identical"]} CITATIONS={value["citation_integrity"]}')
    for name, item in report.get("counterfeit_probes", {}).items():
        print(f'COUNTERFEIT {name}: model_accepts={item.get("model_accepts_counterfeit_step")}'
              f' rule_guard_accepts={item.get("unverified_rule_guard_accepts_counterfeit")}'
              f' current_projection_rejects={item.get("current_projection_rejects_counterfeit")}'
              f' bypass_exposes_false_claim={item.get("forced_bypass_would_emit_false_equation", item.get("forced_bypass_would_emit_false_exactness"))}')
    if "error" in report:
        print(report["error"])
    print("R3-41P8_STATUS", report["status"])
    print("REPORT", OUTPUT / "audit.md")
    print("APPLICATION_SOURCE_UNCHANGED")
    print("FULL_PYTEST_NOT_RUN")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
