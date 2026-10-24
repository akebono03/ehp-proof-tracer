"""Phase 168 R3-41P4: audit remaining display-time validation without modifying app sources."""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUT = PACKAGE / "output"
FILES = (
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_27_typed_statement_projection.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_12_body_binding.py",
    "phase168_r3_29_order_projection.py",
    "phase166_r3ac_stable_notation.py",
    "phase165_r12_r11_prop42_unified.py",
)
CASES = (("pi3_2", 2, 1, 18, 4), ("pi4_3", 3, 1, 25, 4), ("pi5_4", 4, 1, 10, 3))
LITERAL_TRANSPORT_NAME = "proved generator suspension normalizes transported cyclic group"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_info() -> dict[str, str | None]:
    info = {}
    for key, args in (
        ("head", ["rev-parse", "HEAD"]),
        ("branch", ["branch", "--show-current"]),
        ("status", ["status", "--short"]),
    ):
        try:
            completed = subprocess.run(
                ["git", *args], cwd=PROJECT, capture_output=True,
                text=True, encoding="utf-8", errors="replace", check=False,
            )
            info[key] = completed.stdout.strip() if completed.returncode == 0 else None
        except OSError:
            info[key] = None
    return info


def scan_static() -> dict[str, object]:
    results = []
    absent = []
    for name in FILES:
        path = PROJECT / name
        if not path.is_file():
            absent.append(name)
            continue
        data = path.read_bytes()
        source = data.decode("utf-8-sig")
        tree = ast.parse(source, filename=name)
        nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                target = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else ""
                )
                if target in ("_stable_eta_renaming_shape", "prop42_exactness_indices"):
                    nodes.append({
                        "line": node.lineno, "name": target,
                        "kind": "math_rule_recheck",
                        "source": source.splitlines()[node.lineno - 1].strip(),
                    })
                if target == "getattr" and len(node.args) >= 2 and (
                    isinstance(node.args[1], ast.Constant) and node.args[1].value == "name"
                ) and any(
                    isinstance(child, ast.Attribute) and child.attr == "inference_rule"
                    for child in ast.walk(node.args[0])
                ):
                    nodes.append({
                        "line": node.lineno, "name": "inference_rule.name",
                        "kind": "string_name_dependency",
                        "source": source.splitlines()[node.lineno - 1].strip(),
                    })
        results.append({"file": name, "sha256": sha256_bytes(data), "bytes": len(data),
                        "findings": sorted(nodes, key=lambda x: x["line"])})
    return {"files": results, "missing": absent}


def index_of_step(model, step):
    by_identity = [i for i, candidate in enumerate(model.steps) if candidate is step]
    if len(by_identity) == 1:
        return by_identity[0]
    by_value = [i for i, candidate in enumerate(model.steps) if candidate == step]
    return by_value[0] if len(by_value) == 1 else None


def name_sensitive_steps(model):
    """Find suppression-shaped proof nodes. Never execute a proof validator."""
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from proof import ProofRule, Relation

    findings = []
    for index, consumer in enumerate(model.steps):
        statement = consumer.conclusion
        if not (consumer.rule is ProofRule.INFERENCE
                and isinstance(statement, Relation)
                and len(consumer.premises) == 2
                and isinstance(statement.rhs, FiniteCyclicGroup)):
            continue
        transported_step, witness_step = consumer.premises
        transported = transported_step.conclusion
        witness = witness_step.conclusion
        if not (transported_step.rule is ProofRule.INFERENCE
                and isinstance(transported, Relation)
                and isinstance(transported.rhs, FiniteCyclicGroup)
                and isinstance(witness, GeneratorSuspension)
                and transported.lhs == statement.lhs
                and transported.rhs.order == statement.rhs.order
                and transported.lhs == witness.map.target_group):
            continue
        name = getattr(consumer.inference_rule, "name", None)
        earlier_index = index_of_step(model, transported_step)
        consumers = sum(
            any(parent is transported_step or parent == transported_step
                for parent in other.premises)
            for other in model.steps
        )
        findings.append({
            "step_index": index,
            "rule_name": name,
            "literal_matches": name == LITERAL_TRANSPORT_NAME,
            "transported_step_index": earlier_index,
            "transported_citations": list(model.step_citation_numbers[earlier_index])
                if earlier_index is not None else None,
            "transported_consumer_count": consumers,
            "is_root": index == model.root_index,
        })
    return findings


def eta_candidates(model):
    """Inventory of candidates; deliberately do not re-run the eta rule."""
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup
    from proof import Relation
    found = []
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if (isinstance(statement, Relation)
                and isinstance(statement.rhs, FiniteCyclicGroup)
                and isinstance(statement.rhs.generator, IteratedSuspension)):
            found.append({
                "step_index": index,
                "exponent": statement.rhs.generator.exponent,
                "premise_indices": [index_of_step(model, p) for p in step.premises],
            })
    return found


def exactness_wording_candidates(model):
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from toda_rules import TodaProp42ExactnessStatement
    from proof import ProofRule

    rows = []
    def has_exactness(node, seen):
        if id(node) in seen:
            return False
        seen.add(id(node))
        if isinstance(node.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement)):
            return True
        return any(has_exactness(parent, seen) for parent in node.premises)

    for index, step in enumerate(model.steps):
        if step.rule is not ProofRule.INFERENCE or not isinstance(step.conclusion, (MapInjective, MapSurjective)):
            continue
        rows.append({
            "step_index": index,
            "conclusion_type": type(step.conclusion).__name__,
            "direct_premise_names": [getattr(p.inference_rule, "name", None) for p in step.premises],
            "direct_name_contains_exact": any("exact" in str(getattr(p.inference_rule, "name", "")).lower()
                                              for p in step.premises),
            "typed_exactness_in_ancestors": any(has_exactness(p, set()) for p in step.premises),
        })
    return rows


def check_three_groups() -> dict[str, object]:
    import phase168_r3_5_model_renderer as renderer
    import phase168_r3_27_typed_statement_projection as projection
    import phase166_r3ac_stable_notation as eta_math
    from web_group_proof import build_standard_web_group_proof_view
    from phase168_r3_38_frozen_fulltext_audit.audit import sections
    from phase168_r3_39f_frozen_comparison.audit import assess

    original_renderer = renderer.render_model_backed_narrative_markdown
    original_sentence = projection.typed_sentence
    original_transition = projection.project_stable_eta_notation_transition
    original_eta = eta_math._stable_eta_renaming_shape
    original_exactness = projection.prop42_exactness_indices
    records = {}

    for name, n, k, expected_steps, expected_refs in CASES:
        events = []
        captures = []
        state = {"in_render": False, "step": None}

        def record(label, original, args, kwargs):
            outcome = original(*args, **kwargs)
            if state["in_render"]:
                caller = sys._getframe(1).f_back
                events.append({
                    "validator": label,
                    "caller_file": Path(caller.f_code.co_filename).name,
                    "caller_function": caller.f_code.co_name,
                    "step_index": state["step"],
                    "result_is_none": outcome is None,
                    "result_truthy": bool(outcome),
                    "arg_types": [type(arg).__name__ for arg in args],
                })
            return outcome

        def eta_spy(*args, **kwargs):
            return record("_stable_eta_renaming_shape", original_eta, args, kwargs)

        def exactness_spy(*args, **kwargs):
            return record("prop42_exactness_indices", original_exactness, args, kwargs)

        def sentence_spy(statement, step):
            old = state["step"]
            # Model is set before rendering, so locate via identity when possible.
            model = state.get("model")
            state["step"] = index_of_step(model, step) if model is not None else None
            try:
                return original_sentence(statement, step)
            finally:
                state["step"] = old

        def transition_spy(model, step_index):
            old = state["step"]
            state["step"] = step_index
            try:
                return original_transition(model, step_index)
            finally:
                state["step"] = old

        def capture_renderer(result, model):
            original_fingerprint = sha256_bytes(repr((model.steps, model.citations,
                                                      model.step_citation_numbers)).encode("utf-8"))
            state.update({"in_render": True, "model": model})
            try:
                text = original_renderer(result, model)
            finally:
                state["in_render"] = False
            rendered_fingerprint = sha256_bytes(repr((model.steps, model.citations,
                                                      model.step_citation_numbers)).encode("utf-8"))
            captures.append((text, model, original_fingerprint == rendered_fingerprint))
            return text

        with patch.object(eta_math, "_stable_eta_renaming_shape", side_effect=eta_spy), \
             patch.object(projection, "prop42_exactness_indices", side_effect=exactness_spy), \
             patch.object(projection, "typed_sentence", side_effect=sentence_spy), \
             patch.object(projection, "project_stable_eta_notation_transition", side_effect=transition_spy), \
             patch.object(renderer, "render_model_backed_narrative_markdown", side_effect=capture_renderer):
            build_standard_web_group_proof_view(n=n, k=k)

        if len(captures) != 1:
            raise AssertionError(f"Expected one shared Renderer call for {name}, got {len(captures)}")
        rendered, model, no_mutation = captures[0]
        reference, proof = sections(rendered)
        benchmark = assess(name, proof)
        previous_path = PACKAGE / "fixtures" / f"{name}_current.md"
        baseline = previous_path.read_text(encoding="utf-8-sig")
        changes = "".join(difflib.unified_diff(
            baseline.splitlines(keepends=True), rendered.splitlines(keepends=True),
            fromfile="R3-41P3_" + name,
            tofile="R3-41P4_" + name,
        ))
        (OUT / f"{name}_current.md").write_text(rendered, encoding="utf-8")
        (OUT / f"{name}_fulltext.diff").write_text(changes, encoding="utf-8")
        used = sorted({int(number) for number in re.findall(r"\[R(\d+)\]", proof)})
        cited = sorted(citation.number for citation in model.citations)
        rows = [{
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "step_indices": list(citation.step_indices),
            "body_count": len(citation.statement_bodies),
        } for citation in model.citations]
        corresponding = all(
            number in model.step_citation_numbers[index]
            for citation in model.citations
            for number in (citation.number,)
            for index in citation.step_indices
        ) and all(
            index in next(c.step_indices for c in model.citations if c.number == number)
            for index, nums in enumerate(model.step_citation_numbers)
            for number in nums
        )
        records[name] = {
            "status": str(model.status),
            "steps": len(model.steps), "expected_steps": expected_steps,
            "references": len(model.citations), "expected_references": expected_refs,
            "reference_provenance": rows,
            "citation_numbers_used": used, "citation_numbers_in_model": cited,
            "citation_consistent": corresponding and used == cited,
            "reference_bodies_complete": all(c.statement_bodies for c in model.citations),
            "model_unmodified": no_mutation,
            "p3_fulltext_exact": changes == "",
            "fulltext_diff_lines": len(changes.splitlines()),
            "benchmark_checks": benchmark,
            "benchmark_complete": all(x["present"] for x in benchmark),
            "validator_calls": events,
            "eta_candidates": eta_candidates(model),
            "exactness_wording_candidates": exactness_wording_candidates(model),
            "rule_name_suppression_candidates": name_sensitive_steps(model),
        }
    return records


def write_report(payload):
    lines = [
        "# Phase 168 R3-41P4 — 残存する表示時判定の監査", "",
        "## 方針", "", "- 監査専用。プロジェクト本体のコードとテストは変更しない。",
        "- 確認対象：安定 η 表記、EHP 完全性、推論規則名への依存。",
        "- 検証関数を呼び出す際は元の実装に委譲し、呼び出しの有無と由来のみ記録する。",
        "- 証明本文・Reference は R3-41P3 の保存全文と比較する。", "",
        "## Git 情報", "",
        f"- branch: `{payload['git']['branch']}`",
        f"- HEAD: `{payload['git']['head']}`", "",
        "## 静的監査で見つかった箇所", "",
        "| ファイル | 行 | 呼び出し・条件 | 分類 |", "|---|---:|---|---|",
    ]
    for file in payload["static"]["files"]:
        for finding in file["findings"]:
            lines.append(f"| `{file['file']}` | {finding['line']} | `{finding['name']}` | {finding['kind']} |")
    lines.extend(["", "## 公開 Web の3群", "",
                  "| 群 | ProofStep | Ref. | P3全文一致 | Citation | 数学的関数の表示時呼び出し |",
                  "|---|---:|---:|---|---|---:|"])
    for name, row in payload.get("runtime", {}).items():
        lines.append(f"| {name} | {row['steps']} | {row['references']} | {row['p3_fulltext_exact']} | {row['citation_consistent']} | {len(row['validator_calls'])} |")
    lines.extend(["", "## 判定の内訳", ""])
    for name, row in payload.get("runtime", {}).items():
        lines.append(f"### {name}")
        lines.append(f"- η 表記の候補数：{len(row['eta_candidates'])}")
        lines.append(f"- 単射・全射の説明候補数：{len(row['exactness_wording_candidates'])}")
        lines.append(f"- 規則名依存の表示省略候補数：{len(row['rule_name_suppression_candidates'])}")
        if not row["validator_calls"]:
            lines.append("- 対象の数学的判定関数呼び出し：なし（未使用箇所の安全性は未証明）")
        for call in row["validator_calls"]:
            lines.append(f"- `{call['validator']}`：step={call['step_index']}, caller=`{call['caller_function']}`")
        lines.append("")
    lines.extend([
        "## 解釈上の注意", "",
        "- 表示時の数学的再判定と、表示の整合性確認は区別する。",
        "- 動的呼び出し0回は検証関数が不要と証明されたことを意味しない。",
        "- 規則名を削除する際は、同一結果の別推論規則を誤って表示省略しない保証が必要。",
        "- 本監査は新しい推論や証明を実施しない。", "- 全体 pytest は Phase 168 終了時のみ実行する。", "",
    ])
    if payload.get("error"):
        lines.extend(["## エラー", "", "```text", payload["error"], "```", ""])
    (OUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {"git": git_info()}
    status = 0
    try:
        payload["static"] = scan_static()
        if payload["static"]["missing"]:
            raise FileNotFoundError("Required project modules are missing: " + ", ".join(payload["static"]["missing"]))
        renderer_source = (PROJECT / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
        projection_source = (PROJECT / "phase168_r3_27_typed_statement_projection.py").read_text(encoding="utf-8-sig")
        if "direct_given_premise_citation_numbers" not in renderer_source:
            raise RuntimeError("R3-41P3 Renderer change is not applied")
        if "specialize_typed_statement" in renderer_source or "specialize_typed_statement" in projection_source:
            raise RuntimeError("R3-41P3 removed-specialization invariant is not satisfied")
        payload["runtime"] = check_three_groups()
        for name, entry in payload["runtime"].items():
            if (entry["steps"] != entry["expected_steps"] or
                entry["references"] != entry["expected_references"] or
                not entry["citation_consistent"] or
                not entry["reference_bodies_complete"] or
                not entry["model_unmodified"] or
                not entry["p3_fulltext_exact"] or
                not entry["benchmark_complete"]):
                status = 1
    except Exception:
        payload["error"] = traceback.format_exc()
        status = 1
    finally:
        (OUT / "audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        write_report(payload)
    for name, row in payload.get("runtime", {}).items():
        print(f"{name} steps={row['steps']} refs={row['references']} "
              f"P3_FULLTEXT_EQUAL={row['p3_fulltext_exact']} "
              f"CITATIONS={row['citation_consistent']} "
              f"ETA_RECHECKS={sum(c['validator'] == '_stable_eta_renaming_shape' for c in row['validator_calls'])} "
              f"EXACTNESS_RECHECKS={sum(c['validator'] == 'prop42_exactness_indices' for c in row['validator_calls'])} "
              f"NAME_CANDIDATES={len(row['rule_name_suppression_candidates'])}")
    if payload.get("error"):
        print(payload["error"], file=sys.stderr)
    print("REPORT", OUT / "audit.md")
    print("AUDIT_STATUS", "PASS" if status == 0 else "REVIEW_REQUIRED")
    print("APPLICATION_SOURCE_UNCHANGED")
    print("FULL_PYTEST_NOT_RUN")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
