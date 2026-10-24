"""Read-only audit of proof dependencies versus Narrative display order.

This script does not replace project_narrative_order or derive propositions.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase168_r3_40b_dependency_audit.audit_core import (
    dependency_inversions,
    flattened_order,
    proof_dependency_edges,
    relative_order,
)

CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1),
         ("pi6_5", 5, 1))
OUTPUT = PACKAGE / "output"


def displayable(step) -> bool:
    """Match the two existing rendering routes; never fabricate new prose."""
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from web_group_proof_common import _group_proof_statement_latex
    latex, fallback = _group_proof_statement_latex(step.conclusion)
    if latex is not None and fallback is None:
        return True
    return typed_sentence(step.conclusion, step) is not None


def one_case(name: str, n: int, k: int) -> dict:
    from expression import IteratedSuspension
    from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaSuspensionMap
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_26_exactness_projection import project_exactness_chains
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from proof import Relation, RelationType
    from toda_rules import Toda45IsomorphismStatement

    rendered, model, view = capture(n, k)
    reference, proof = sections(rendered)
    (OUTPUT / (name + "_current.md")).write_text(rendered, encoding="utf-8")

    chains = project_exactness_chains(model)
    suppressed = {i for chain in chains for i in chain.step_indices}
    order_entries = project_narrative_order(model, suppressed)
    order = flattened_order(order_entries, len(model.steps), suppressed)
    edges, unresolved = proof_dependency_edges(model.steps)
    inversions_in_model = dependency_inversions(edges, tuple(range(len(model.steps))))
    inversions_in_projection = dependency_inversions(edges, order)
    positions = {step: idx for idx, step in enumerate(order)}
    rendered_indices = tuple(i for i in order if displayable(model.steps[i]))
    nonrendered_indices = tuple(i for i in order if i not in rendered_indices)

    table = []
    for index, step in enumerate(model.steps):
        table.append({
            "step_index": index,
            "type": type(step.conclusion).__name__,
            "rule": step.rule.value,
            "inference_name": (step.inference_rule.name if step.inference_rule else None),
            "premise_count": len(step.premises),
            "citation_numbers": list(model.step_citation_numbers[index]),
            "suppressed_exactness": index in suppressed,
            "renderable_as_statement": displayable(step),
            "projected_position": positions.get(index),
        })

    editorial = []
    for iso_index, iso_step in enumerate(model.steps):
        iso = iso_step.conclusion
        if not isinstance(iso, Toda45IsomorphismStatement):
            continue
        mapping = getattr(iso, "map", None)
        if not isinstance(mapping, TodaIteratedSuspensionMap):
            continue
        if type(mapping.exponent) is not int or mapping.exponent < 1:
            continue
        if any(type(v) is not int for v in (
                mapping.source_group.group_dimension,
                mapping.source_group.sphere_dimension,
                mapping.target_group.group_dimension,
                mapping.target_group.sphere_dimension)):
            continue
        if iso_index not in positions:
            continue

        source_options = [i for i, step in enumerate(model.steps)
                          if i in positions and isinstance(step.conclusion, Relation)
                          and step.conclusion.relation_type is RelationType.EQUALITY
                          and step.conclusion.lhs == mapping.source_group]
        transport_options = [i for i, step in enumerate(model.steps)
                             if i in positions and isinstance(step.conclusion, Relation)
                             and step.conclusion.relation_type is RelationType.EQUALITY
                             and step.conclusion.lhs == mapping.target_group
                             and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
                             and isinstance(step.conclusion.rhs.generator, IteratedSuspension)
                             and step.conclusion.rhs.generator.exponent == mapping.exponent]
        image_options = [i for i, step in enumerate(model.steps)
                         if i in positions
                         and isinstance(step.conclusion, (GeneratorImage, GeneratorSuspension))
                         and isinstance(step.conclusion.map, TodaSuspensionMap)
                         and step.conclusion.map.target_group == mapping.target_group]
        named_options = [i for i, step in enumerate(model.steps)
                         if i in positions and isinstance(step.conclusion, Relation)
                         and step.conclusion.relation_type is RelationType.EQUALITY
                         and step.conclusion.lhs == mapping.target_group
                         and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
                         and not isinstance(step.conclusion.rhs.generator, IteratedSuspension)]
        if not source_options and not transport_options:
            continue
        source_index = min(source_options, key=positions.get) if source_options else None
        transport_index = min(transport_options, key=positions.get) if transport_options else None
        def order_check(first, second):
            if first is None or second is None:
                return "NOT_EVALUABLE"
            return relative_order(first, second, order)
        editorial.append({
            "map_step": iso_index,
            "map_exponent": mapping.exponent,
            "source_group_index": source_index,
            "transported_group_index": transport_index,
            "generator_image_indices": image_options,
            "named_group_indices": named_options,
            "source_before_isomorphism": order_check(source_index, iso_index),
            "isomorphism_before_transport": order_check(iso_index, transport_index),
            "transport_before_generator_images": [
                {"step": i, "status": order_check(transport_index, i)}
                for i in image_options
            ],
            "transport_before_named_group": [
                {"step": i, "status": order_check(transport_index, i)}
                for i in named_options
            ],
        })

    from phase168_r3_27_typed_statement_projection import typed_sentence
    from web_group_proof_common import _group_proof_statement_latex
    abbreviated = []
    for i in order:
        latex, fallback = _group_proof_statement_latex(model.steps[i].conclusion)
        sentence = typed_sentence(model.steps[i].conclusion, model.steps[i]) if latex is None or fallback is not None else None
        abbreviated.append({
            "step_index": i,
            "type": type(model.steps[i].conclusion).__name__,
            "math_preview": latex[:150] if latex is not None and fallback is None else None,
            "prose_preview": sentence[:150] if sentence is not None else None,
        })

    observed = {
        "proof_contains_explicit_pi65_iterated_eta_identity":
            (r"E^{2}\eta_{3}=\eta_{5}" in proof if name == "pi6_5" else None),
        "has_references": bool(reference.strip()),
        "proof_ends_with_box": proof.rstrip().endswith("□"),
    }
    return {
        "name": name,
        "n": n,
        "k": k,
        "provenance_from_web_view": view.key,
        "proof_step_count": len(model.steps),
        "suppressed_exactness_indices": sorted(suppressed),
        "projected_order": list(order),
        "renderable_step_count": len(rendered_indices),
        "nonrendered_indices": list(nonrendered_indices),
        "premise_edges": [list(e) for e in edges],
        "unresolved_premises": list(unresolved),
        "original_dependency_inversions": [list(e) for e in inversions_in_model],
        "projected_dependency_inversions": [list(e) for e in inversions_in_projection],
        "editorial_order_checks": editorial,
        "proof_step_table": table,
        "projected_render_previews": abbreviated,
        "observed_text_checks": observed,
        "citation_integrity": {
            "number_count": len(model.citations),
            "numbers_are_contiguous": [c.number for c in model.citations]
                == list(range(1, len(model.citations) + 1)),
            "citation_numbers_resolve": all(
                number <= len(model.citations) and number >= 1
                for numbers in model.step_citation_numbers for number in numbers
            ),
        },
    }


def source_checksums():
    paths = (
        "phase168_r3_29_order_projection.py",
        "phase168_r3_27_typed_statement_projection.py",
        "phase168_r3_5_model_renderer.py",
        "phase168_r3_3_proof_narrative_model.py",
    )
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in paths}


def make_markdown(report: dict) -> str:
    lines = ["# Phase 168 R3-40B — 依存関係と表示順序の監査", "",
             "読み取り専用。新しい命題・引用・表示規則は導入しない。", "",
             "| 対象 | Steps | 論理依存の逆転 (Projection) | 未解決前提 | 編集上の順序不一致 |",
             "|---|---:|---:|---:|---:|"]
    for c in report["cases"]:
        bad = sum(v == "FAIL" for a in c["editorial_order_checks"] for v in (
            [a["source_before_isomorphism"], a["isomorphism_before_transport"]]
            + [b["status"] for b in a["transport_before_generator_images"]]
            + [b["status"] for b in a["transport_before_named_group"]]))
        lines.append(f'| {c["name"]} | {c["proof_step_count"]} | '
                     f'{len(c["projected_dependency_inversions"])} | '
                     f'{len(c["unresolved_premises"])} | {bad} |')
    lines.extend(("", "## 読み方", "",
                  "- 論理依存の逆転：既存の ProofStep.premises を表示順が逆転したもの。非表示ステップを含む場合は別途確認する。",
                  "- 編集上の順序不一致：出典群・Toda 同型・輸送結果・生成元の表示について、検証可能な箇所だけ比較したもの。数学的な誤りと同一視しない。",
                  "- Proof Tree の論理依存だけでは、独立な生成元恒等式の自然な文章位置までは決まらない。",
                  "- Reference はモデルの citation に従い、推論規則名だけから新たに付与しない。", ""))
    for c in report["cases"]:
        lines.extend((f'## {c["name"]}', "",
                      f'- 全ステップ数: {c["proof_step_count"]}',
                      f'- 表示可能なステップ数: {c["renderable_step_count"]}',
                      f'- 論理依存逆転: {c["projected_dependency_inversions"]}',
                      f'- 未解決の前提: {c["unresolved_premises"]}',
                      f'- 表示順: {c["projected_order"]}',
                      f'- Toda 輸送に関係する順序チェック: {json.dumps(c["editorial_order_checks"], ensure_ascii=False)}',
                      "", "### 表示可能ステップの概要", ""))
        for e in c["projected_render_previews"]:
            if e["math_preview"] or e["prose_preview"]:
                lines.append(f'- #{e["step_index"]}: {e["type"]} — '
                             f'{e["prose_preview"] or e["math_preview"]}')
        lines.append("")
    lines.extend(("## この監査から先の設計判断", "",
                  "1. ProofStep.premises の論理的な前後関係は壊さない。",
                  "2. 出典となる群構造・Toda (4.5) の特殊化・輸送先の群・生成元の同定という表示上の関係は、Proof Tree に実在するノードを参照して明示的に検証する。",
                  "3. 特定の群番号や指数に依存した分岐を一般的な順序付けに混入させない。",
                  "4. 次の Phase で共通表示順序へ置換するときは、既存の3群の固定基準テストと pi6_5 の検証を限定実行する。",
                  "", "全体 pytest は実行しない。"))
    return "\n".join(lines) + "\n"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [one_case(name, n, k) for name, n, k in CASES]
    report = {
        "mode": "READ_ONLY_DEPENDENCY_AUDIT",
        "source_sha256": source_checksums(),
        "cases": cases,
        "limitations": [
            "A topological order does not alone certify natural expository order.",
            "A ProofStep omitted from prose may be introduced in the reference section.",
            "This audit does not assert mathematical equivalence of raw or reordered prose.",
            "The previous R3-40A patch, if installed, is audited as-is; this audit does not install or revert it.",
        ],
    }
    (OUTPUT / "dependency_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTPUT / "dependency_audit.md").write_text(make_markdown(report), encoding="utf-8")
    bundle_path = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT.glob("*.md")) + sorted(OUTPUT.glob("*.json")):
            archive.write(path, path.name)
    for item in cases:
        checks = [v["status"] for c in item["editorial_order_checks"]
                  for v in c["transport_before_generator_images"]]
        print(item["name"], "steps", item["proof_step_count"],
              "logical_inversions", len(item["projected_dependency_inversions"]),
              "unresolved_premises", len(item["unresolved_premises"]),
              "generator_order", checks)
    print("AUDIT_ONLY: no implementation or registered source files modified")
    print("REPORT:", OUTPUT / "dependency_audit.md")
    print("UPLOAD_BUNDLE:", bundle_path)
    print("Full pytest NOT run.")


if __name__ == "__main__":
    main()
