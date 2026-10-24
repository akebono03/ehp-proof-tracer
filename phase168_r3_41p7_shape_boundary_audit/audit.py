"""R3-41P7 audit-only: locate redundant renderer rule validation and fail-closed behavior.

No source, test, citation registry or proof search implementation is modified.
"""
from __future__ import annotations

import ast
from collections import Counter
from dataclasses import replace
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys
import traceback
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUT = PACKAGE / "output"
BASELINES = PACKAGE / "fixtures"

CASES = (("pi3_2", 2, 1, 18, 4), ("pi4_3", 3, 1, 25, 4), ("pi5_4", 4, 1, 10, 3))
SOURCE_FILES = (
    "phase168_r3_27_typed_statement_projection.py",
    "phase166_r3ac_stable_notation.py",
    "phase165_r12_r11_prop42_unified.py",
    "phase165_r12_r12_ehp_consequences.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_3_proof_narrative_model.py",
)
GITHUB_DEVELOP_SHA = {
    "phase168_r3_27_typed_statement_projection.py": "f14a155939f95dc414ad8f3022a7a2fb21e5e4cf",
    "phase166_r3ac_stable_notation.py": "de8619628b45dd9d04ba1aebfea98a4899e2d72a",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase168_r3_5_model_renderer.py": "66509896c60d431427e3c18e70a911d7bebe8d7c",
    "phase168_r3_3_proof_narrative_model.py": "1080843a2a90bf60f0b8096d3c5542a24a9abb7c",
}
VALIDATION_FUNCTIONS = ("_stable_eta_renaming_shape", "prop42_exactness_indices")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def static_inventory(source: str) -> list[dict[str, object]]:
    tree = ast.parse(source)
    results: list[dict[str, object]] = []
    scopes: list[str] = []

    class Find(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            scopes.append(node.name)
            self.generic_visit(node)
            scopes.pop()

        def visit_Call(self, node: ast.Call) -> None:
            name = (
                node.func.id if isinstance(node.func, ast.Name)
                else node.func.attr if isinstance(node.func, ast.Attribute)
                else ""
            )
            if name in VALIDATION_FUNCTIONS:
                results.append({
                    "function": ".".join(scopes),
                    "line": node.lineno,
                    "validator": name,
                })
            self.generic_visit(node)

    Find().visit(tree)
    return results


def source_inventory() -> dict[str, object]:
    output = {}
    for name in SOURCE_FILES:
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(str(path))
        source = path.read_text(encoding="utf-8-sig")
        output[name] = {
            "sha256": sha256_file(path),
            "github_develop_blob_sha": GITHUB_DEVELOP_SHA[name],
            "lines": len(source.splitlines()),
            "validator_calls": static_inventory(source),
        }
    return output


def provenance(model, text: str) -> dict[str, object]:
    from phase168_r3_38_frozen_fulltext_audit.audit import sections
    _, proof = sections(text)
    used = {int(n) for n in re.findall(r"\[R(\d+)\]", proof)}
    expected = {citation.number for citation in model.citations}
    valid_links = all(
        0 <= i < len(model.steps)
        and citation.number in model.step_citation_numbers[i]
        for citation in model.citations for i in citation.step_indices
    ) and all(
        any(citation.number == number and i in citation.step_indices
            for citation in model.citations)
        for i, numbers in enumerate(model.step_citation_numbers)
        for number in numbers
    )
    return {
        "used_citation_numbers": sorted(used),
        "registered_citation_numbers": sorted(expected),
        "citation_numbers_match": used == expected,
        "bidirectional_links_valid": valid_links,
        "reference_bodies_complete": all(c.statement_bodies for c in model.citations),
        "premises_in_model": all(
            any(candidate is premise or candidate == premise for candidate in model.steps)
            for step in model.steps for premise in step.premises
        ),
        "number_of_reference_entries": len(model.citations),
        "number_of_steps": len(model.steps),
    }


def capture_public_cases() -> tuple[dict[str, object], object | None]:
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from phase168_r3_39f_frozen_comparison.audit import assess
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    report = {}
    sample = None
    for name, n, k, steps, references in CASES:
        text, model, view = capture(n, k)
        p = provenance(model, text)
        fixture = (BASELINES / f"{name}_current.md").read_text(encoding="utf-8-sig")
        same = fixture == text
        (OUT / f"{name}_current.md").write_text(text, encoding="utf-8")
        diff = "".join(difflib.unified_diff(
            fixture.splitlines(keepends=True), text.splitlines(keepends=True),
            fromfile=f"{name}_r341p6", tofile=f"{name}_r341p7",
        ))
        (OUT / f"{name}_fulltext.diff").write_text(diff, encoding="utf-8")
        _, proof = sections(text)
        checks = assess(name, proof)
        same_structure = p["number_of_steps"] == steps and p["number_of_reference_entries"] == references
        report[name] = {
            "steps": p["number_of_steps"], "references": p["number_of_reference_entries"],
            "expected_steps": steps, "expected_references": references,
            "expected_counts_match": same_structure,
            "fulltext_identical_to_p6": same,
            "frozen_requirements": checks,
            "frozen_requirements_pass": all(c["present"] for c in checks),
            "provenance": p,
        }
        for step in model.steps:
            if isinstance(step.conclusion, EHPImageEqualsKernelStatement) and sample is None:
                sample = step
    return report, sample


def probe_stable_eta() -> dict[str, object]:
    """Use the existing R3-AC tested r=2 construction; do not register it as a fact."""
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase166_r3ac_stable_notation import stable_eta_notation_rule
    from phase168_r3_27_typed_statement_projection import project_stable_eta_notation_transition
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, NarrativeCitation
    from proof import LiteratureReference, ProofRule, ProofStep, Relation
    from toda_rules import toda_eta_family_definition_statement

    r = 2
    source = toda_eta_family_definition_statement(3).element
    target = toda_eta_family_definition_statement(3 + r).element
    group = TodaPrimaryGroup(4 + r, 3 + r)
    goal = Relation(group, FiniteCyclicGroup(2, target))
    transported = Relation(group, FiniteCyclicGroup(2, IteratedSuspension(source, r)))
    source_step = ProofStep(transported, (), ProofRule.GIVEN)
    definition_step = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    target_step = ProofStep(goal, (source_step, definition_step), ProofRule.INFERENCE,
                            inference_rule=stable_eta_notation_rule(goal))
    citation = NarrativeCitation(1, LiteratureReference(label="synthetic eta definition"), (1,))
    model = ProofNarrativeModel((source_step, definition_step, target_step),
                                (citation,), ((), (1,), ()), 2)
    from proof import find_inference_matches_for_rule
    proof_rule_has_match = bool(find_inference_matches_for_rule(
        stable_eta_notation_rule(goal), (source_step, definition_step),
    ))
    valid_text = project_stable_eta_notation_transition(model, 2)

    invalid_goal = Relation(group, FiniteCyclicGroup(3, target))
    wrong_step = ProofStep(invalid_goal, (source_step, definition_step), ProofRule.INFERENCE)
    invalid_model = replace(model, steps=(source_step, definition_step, wrong_step))
    invalid_text = project_stable_eta_notation_transition(invalid_model, 2)

    no_citation = replace(model, citations=(), step_citation_numbers=((), (), ()))
    uncited_text = project_stable_eta_notation_transition(no_citation, 2)
    return {
        "source": "synthetic r=2, based on phase166_r3ac_stable_notation/tests/test_r3ac.py",
        "rule_guard_has_valid_match": proof_rule_has_match,
        "valid_projection": valid_text,
        "valid_projection_has_citation": valid_text is not None and "[R1]" in valid_text,
        "invalid_order_projection": invalid_text,
        "invalid_order_rejected": invalid_text is None,
        "uncited_projection": uncited_text,
        "uncited_rejected": uncited_text is None,
    }


def probe_ehp(sample_step: object) -> dict[str, object]:
    """Use a real ProofStep from the public search; modify a copy for rejection test."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from toda_rules import TodaProp42ExactnessStatement

    window = sample_step.conclusion.window
    source = window.source_term
    invalid_window = replace(window, source_term=TodaPrimaryGroup(
        source.group_dimension + 1, source.sphere_dimension,
    ))
    # If the source dimension is not mathematically essential in some future
    # formulation, this probe should be revised rather than declaring failure.
    valid_math_indices = prop42_exactness_indices(TodaProp42ExactnessStatement(window))
    invalid_math_indices = prop42_exactness_indices(TodaProp42ExactnessStatement(invalid_window))
    valid_text = typed_sentence(sample_step.conclusion, sample_step)
    invalid_text = typed_sentence(EHPImageEqualsKernelStatement(invalid_window), sample_step)
    return {
        "source": "observed EHPImageEqualsKernelStatement from public search",
        "valid_window": repr(window)[:600],
        "valid_math_indices": valid_math_indices,
        "valid_projection": valid_text,
        "invalid_math_indices": invalid_math_indices,
        "invalid_projection": invalid_text,
        "valid_projection_present": valid_text is not None,
        "invalid_window_rejected": invalid_text is None,
    }


def report_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Phase 168 R3-41P7 — 既存証明済み情報と表示再判定の責務境界監査",
        "",
        "## 監査範囲",
        "",
        "- audit-only。アプリケーションコード、既存テスト、DB を変更しない。",
        "- 対象: `_stable_eta_renaming_shape()`、`prop42_exactness_indices()`。",
        "- 検証済み ProofStep の出典を利用した表示と、不正入力に対する拒否を区別する。",
        "- 人工 Probe は表示境界の性質を調べるだけで、数学的証明として使用しない。",
        "",
        "## 既存コードの責務配置",
        "",
        "| 関数 | 証明側の使用 | 表示側の使用 |",
        "|---|---|---|",
        "| `_stable_eta_renaming_shape` | `stable_eta_notation_rule` の guard 等 | `project_stable_eta_notation_transition` |",
        "| `prop42_exactness_indices` | Proposition 4.2 の特殊化と EHP 像＝核規則 | `typed_sentence` |",
        "",
        "いずれも単なる LaTeX 整形ではなく、数学的形状・添字を検査する。",
        "表示側での再検査を削除するには、型付き ProofStep の妥当性を信頼する境界と不正入力時の挙動を明示する必要がある。",
        "",
        "## 3群の比較",
        "",
        "| 群 | ProofStep | Reference | R3-41P6全文 | Citation | 固定基準 |",
        "|---|---:|---:|---|---|---|",
    ]
    for name, item in report.get("cases", {}).items():
        p = item["provenance"]
        lines.append(
            f"| {name} | {item['steps']} | {item['references']} | "
            f"{'PASS' if item['fulltext_identical_to_p6'] else 'DIFF'} | "
            f"{'PASS' if p['citation_numbers_match'] and p['bidirectional_links_valid'] else 'REVIEW'} | "
            f"{'PASS' if item['frozen_requirements_pass'] else 'REVIEW'} |"
        )
    lines.extend(["", "## 動的な検査関数の呼び出し", ""])
    for category, counters in report.get("runtime_validation_calls", {}).items():
        lines.append(f"- `{category}`: `{counters}`")
    lines.extend(["", "## 明示的な形状 Probe", ""])
    for name, probe in report.get("probes", {}).items():
        lines.append(f"### {name}")
        lines.append("")
        for key, value in probe.items():
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
    lines.extend([
        "## 判定上の注意", "",
        "- 3群で動的再検証が0回でも、その関数が将来群の表示に不要とは断言できない。",
        "- 不正な人工 ProofStep が拒否された場合、検証関数の即時削除は不正表示を発生させる危険がある。",
        "- `ProofNarrativeModel` は引用 provenance を持つが、全 ProofStep を数学的に再検証したことを示す専用証明書ではない。",
        "- R3-41P7 では実装の移動・削除を行わず、結果を踏まえて最小修正を別工程で判断する。",
        "- 全体 pytest は Phase 168 の終了時まで実行しない。",
        "",
    ])
    if report.get("error"):
        lines.extend(["## エラー", "", "```text", report["error"], "```", ""])
    return "\n".join(lines)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"status": "ERROR", "sources": {}, "cases": {}, "probes": {}}
    status = 0
    try:
        report["sources"] = source_inventory()
        import phase168_r3_27_typed_statement_projection as projection
        import phase166_r3ac_stable_notation as notation
        original_exactness = projection.prop42_exactness_indices
        original_eta = notation._stable_eta_renaming_shape
        calls = []

        def log_call(kind, function):
            def wrapped(*args, **kwargs):
                caller = sys._getframe(1)
                value = function(*args, **kwargs)
                calls.append({
                    "validator": kind,
                    "caller_file": Path(caller.f_code.co_filename).name,
                    "caller_function": caller.f_code.co_name,
                    "from_projection": Path(caller.f_code.co_filename).name ==
                                       "phase168_r3_27_typed_statement_projection.py",
                    "accepted": value is not None if kind == "prop42_exactness_indices" else bool(value),
                })
                return value
            return wrapped

        with patch.object(projection, "prop42_exactness_indices", log_call("prop42_exactness_indices", original_exactness)), \
             patch.object(notation, "_stable_eta_renaming_shape", log_call("_stable_eta_renaming_shape", original_eta)):
            report["cases"], sample_step = capture_public_cases()
            public_call_count = len(calls)
            report["probes"]["stable_eta"] = probe_stable_eta()
            if sample_step is None:
                report["probes"]["ehp"] = {"status": "NO_EHP_STEP_IN_3_CASES"}
            else:
                report["probes"]["ehp"] = probe_ehp(sample_step)
        report["runtime_validation_calls"] = {
            "public_cases": dict(Counter(
                " / ".join((x["validator"], x["caller_file"], x["caller_function"]))
                for x in calls[:public_call_count]
            )),
            "probes": dict(Counter(
                " / ".join((x["validator"], x["caller_file"], x["caller_function"]))
                for x in calls[public_call_count:]
            )),
            "details": calls,
        }
        for name, entry in report["cases"].items():
            assert entry["fulltext_identical_to_p6"], f"{name}: fulltext differs"
            assert entry["expected_counts_match"], f"{name}: unexpected step/ref count"
            assert entry["frozen_requirements_pass"], f"{name}: benchmark reasoning missing"
            assert all(entry["provenance"][key] for key in (
                "citation_numbers_match", "bidirectional_links_valid",
                "reference_bodies_complete", "premises_in_model",
            )), f"{name}: citation provenance mismatch"
        eta = report["probes"]["stable_eta"]
        assert eta["rule_guard_has_valid_match"] and eta["valid_projection_has_citation"]
        assert eta["invalid_order_rejected"] and eta["uncited_rejected"]
        ehp = report["probes"]["ehp"]
        if "status" not in ehp:
            assert ehp["valid_math_indices"] is not None and ehp["invalid_math_indices"] is None
            assert ehp["valid_projection_present"] and ehp["invalid_window_rejected"]
        report["status"] = "PASS"
    except Exception:
        report["error"] = traceback.format_exc()
        print("AUDIT_ERROR", report["error"], file=sys.stderr)
        status = 1
    finally:
        (OUT / "audit.json").write_text(json.dumps(
            report, ensure_ascii=False, indent=2, default=str
        ) + "\n", encoding="utf-8")
        (OUT / "audit.md").write_text(report_markdown(report), encoding="utf-8")
        print("R3-41P7_STATUS", report["status"])
        if "cases" in report:
            for name, row in report["cases"].items():
                p = row["provenance"]
                print(name, f"steps={row['steps']}", f"refs={row['references']}",
                      f"P6_FULLTEXT_EQUAL={row['fulltext_identical_to_p6']}",
                      f"CITATIONS={p['citation_numbers_match'] and p['bidirectional_links_valid']}")
        if "probes" in report:
            for name, row in report["probes"].items():
                print("PROBE", name, "OK" if row.get("invalid_order_rejected", row.get("invalid_window_rejected", False)) else "REVIEW")
        print("REPORT", OUT / "audit.md")
        print("FULL_PYTEST_NOT_RUN")
        print("APPLICATION_SOURCE_UNCHANGED")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
