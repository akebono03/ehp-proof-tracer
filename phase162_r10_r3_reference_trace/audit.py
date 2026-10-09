"""R10-R3 read-only classification of the actual Web proof tree and reference pipeline."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def classify(node: dict[str, Any]) -> str:
    """Assign exactly one structural bucket; retain nonexclusive tags separately."""
    if node.get("foundational_key", "") and str(node["foundational_key"]).startswith("literature:"):
        return "CITED_BOUNDARY"
    if node.get("classification") == "fixed_statement":
        return "FIXED_STATEMENT"
    if node.get("classification") == "proof_internal":
        return "PROOF_INTERNAL"
    if str(node.get("rule", "")).upper() == "GIVEN":
        return "OTHER_GIVEN"
    if str(node.get("rule", "")).upper() == "INFERENCE":
        return "UNCLASSIFIED_INFERENCE"
    return "OTHER_RULE"


def classify_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = graph["nodes"]
    if len(nodes) != 97:
        raise ValueError(f"Expected R10 97-node Web tree, got {len(nodes)}")
    ids = {node["node"] for node in nodes}
    if len(ids) != 97:
        raise ValueError("Repeated node identifiers")
    by_id = {node["node"]: node for node in nodes}
    root = graph["root_node"]
    if root not in by_id:
        raise ValueError("Root not in graph")
    if any(parent not in by_id for node in nodes for parent in node["premises"]):
        raise ValueError("Broken premise link")
    used = set()

    def walk(num: int) -> None:
        if num in used:
            return
        used.add(num)
        for child in by_id[num]["premises"]:
            walk(child)

    walk(root)
    if used != ids:
        raise ValueError("Not every audited node is reachable from root")
    results = []
    for node in nodes:
        category = classify(node)
        tags = []
        if node.get("is_hopf_conclusion"):
            tags.append("H_NU_PRIME")
        if node.get("is_internal_lemma52"):
            tags.append("LEMMA52")
        if node.get("reference"):
            tags.append("EXTRACTABLE_REFERENCE")
        if node.get("classification") == "fixed_statement":
            tags.append("FIXED_CLASSIFICATION")
        if node.get("map_fields"):
            tags.append("MAP_FIELDS")
        if node.get("type", "").endswith(("InjectiveStatement", "SurjectiveStatement", "IsomorphismStatement", "ZeroStatement")):
            tags.append("MAP_PROPERTY")
        if len(node["consumers"]) > 1:
            tags.append("SHARED_PREMISE")
        if node["node"] == root:
            tags.append("ROOT")
        results.append({
            "node": node["node"],
            "category": category,
            "tags": tags,
            "type": node["type"],
            "rule": node["rule"],
            "inference_rule": node.get("inference_rule"),
            "reference": node.get("reference"),
            "component": node.get("component"),
            "foundational_key": node.get("foundational_key"),
            "premises": node["premises"],
            "consumers": node["consumers"],
            "statement": node.get("statement", "")[:480],
        })
    grouped = {k: [x["node"] for x in results if x["category"] == k] for k in sorted({x["category"] for x in results})}
    duplicate_groups = graph["summary"].get("duplicated_conclusion_groups", [])
    return {
        "total": len(results),
        "categories": {name: len(values) for name, values in grouped.items()},
        "category_node_ids": grouped,
        "reference_extraction": dict(Counter(row.get("reference") for row in results if row.get("reference"))),
        "foundational_nodes": [x for x in results if x["foundational_key"]],
        "unextractable_citations": [x["node"] for x in results if x["foundational_key"] and not x["reference"]],
        "duplicate_groups": duplicate_groups,
        "map_property_nodes": [x["node"] for x in results if "MAP_PROPERTY" in x["tags"]],
        "rows": results,
    }


def _entry_summary(entries: tuple[object, ...]) -> list[dict[str, Any]]:
    return [{
        "number": e.number,
        "locator": e.reference.locator,
        "rule_names": [s.inference_rule.name if s.inference_rule else None for s in e.proof_steps],
        "step_count": len(e.proof_steps),
    } for e in entries]


def inspect_live_references() -> dict[str, Any]:
    """Read real Reference extraction and final Web Markdown without patching code."""
    from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
    from toda_group_proof_presentation import build_toda_group_proof_presentation
    from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
    from toda_group_proof_narrative_references import (
        build_toda_group_proof_narrative_reference_entries,
        filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
    )
    from toda_literature_statement_boundary import classify_toda_literature_statement_step
    from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference

    replay = build_phase162_pi5_3_web_replay(max_depth=40)
    presentation = build_toda_group_proof_presentation(replay)
    initial = build_toda_group_proof_narrative_reference_entries(presentation)
    fixed = filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(initial, presentation.root_step)
    markdown = render_toda_group_proof_narrative_markdown(presentation)
    section = markdown.split("## 使用する結果", 1)[1].split("## 証明", 1)[0] if "## 使用する結果" in markdown and "## 証明" in markdown else ""
    citations = []
    seen = set()
    for step in [n.proof_step for n in presentation.nodes]:
        ref_id = getattr(step, "foundational_reference", None)
        if ref_id is None or not str(ref_id.key).startswith("literature:"):
            continue
        if id(step) in seen:
            continue
        seen.add(id(step))
        boundary = classify_toda_literature_statement_step(step)
        extracted = extract_toda_group_proof_step_literature_reference(step)
        citations.append({
            "key": ref_id.key,
            "proof_rule": step.rule.value,
            "inference_rule": step.inference_rule.name if step.inference_rule else None,
            "fixed_classification": boundary.classification.value if boundary else None,
            "extractor_locator": extracted.locator if extracted else None,
            "premise_count": len(step.premises),
        })
    return {
        "raw_entries": _entry_summary(initial),
        "fixed_entries": _entry_summary(fixed),
        "foundational_citations": citations,
        "final_reference_section": section.strip(),
        "final_reference_labels": re.findall(r"\*\*\[R\d+\]\s+([^*]+)\*\*", section),
        "final_body_has_lemma52": "Lemma 5.2" in markdown.split("## 証明",1)[-1],
        "final_body_has_unrelated_h_map": r"\pi_{3}^{2} \to \pi_{3}^{3}" in markdown,
    }


def build_audit(graph_path: Path) -> dict[str, Any]:
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    if "web_replay" not in data.get("graphs", {}):
        raise ValueError("Expected R10-R2 web_replay graph")
    classification = classify_graph(data["graphs"]["web_replay"])
    return {"source": str(graph_path), "web": classification, "live_references": inspect_live_references()}


def _markdown(report: dict[str, Any]) -> str:
    web = report["web"]
    refs = report["live_references"]
    lines = ["# Phase 162 R10-R3 — 97ノード分類とReference欠落監査", "", "実 Web replay を対象にした読み取り専用結果。分類は排他的、tags は非排他的。", "", "## 排他的分類", ""]
    for category, count in web["categories"].items():
        ids = web["category_node_ids"][category]
        lines.append(f"- {category}: **{count}** — nodes {ids}")
    lines += ["", f"合計 **{web['total']}**", "", "## 出典抽出の監査", "", f"- 文献抽出結果: {web['reference_extraction']}", f"- foundational_reference のみで抽出不可: {web['unextractable_citations']}", "", "### Reference の段階別結果", "", f"- 生の抽出: {refs['raw_entries']}", f"- 固定命題の選別後: {refs['fixed_entries']}", f"- 実際の表示ラベル: {refs['final_reference_labels']}", "", "### 引用境界の各ノード", ""]
    for c in refs["foundational_citations"]:
        lines.append(f"- {c}")
    lines += ["", "### Web に表示された Reference", "", "```text", refs["final_reference_section"], "```", "", "## 重複・写像の候補", "", f"- 同じ結論のノード群: {web['duplicate_groups']}", f"- 写像の性質に関するノード: {web['map_property_nodes']}", "", "## 全97ノード", "", "| ID | 分類 | 型 | 推論規則 | 参照 | 前提 → 利用先 | tags |", "|---:|---|---|---|---|---|---|"]
    for row in web["rows"]:
        lines.append("| {node} | {category} | {type} | {inference_rule} | {reference} | {premises} → {consumers} | {tags} |".format(**{**row, "inference_rule": str(row["inference_rule"] or "-").replace("|", "/"), "reference": row["reference"] or "-", "tags": ", ".join(row["tags"])}))
    lines += ["", "## 判定上の注意", "", "- ROOT に到達可能なノードでも、文章化する必要があるとは限らない。", "- 出典の抽出失敗と文献の真偽は別問題。", "- 外見上不要な写像が実際にどの推論の前提かはJSONの premises / consumers で確認する。", ""]
    return "\n".join(lines)


def main() -> None:
    source = Path.cwd() / "phase162_r10_r2_tree_audit.json"
    if not source.exists():
        raise FileNotFoundError(f"First run R10-R2 tree audit: {source}")
    report = build_audit(source)
    output_json = Path.cwd() / "phase162_r10_r3_reference_trace.json"
    output_md = Path.cwd() / "phase162_r10_r3_reference_trace.md"
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(_markdown(report), encoding="utf-8")
    print("Web nodes:", report["web"]["total"])
    print("Categories:", report["web"]["categories"])
    print("Unextractable citation IDs:", report["web"]["unextractable_citations"])
    print("Raw references:", [e["locator"] for e in report["live_references"]["raw_entries"]])
    print("Fixed references:", [e["locator"] for e in report["live_references"]["fixed_entries"]])
    print("Displayed references:", report["live_references"]["final_reference_labels"])
    print("JSON:", output_json)
    print("Markdown:", output_md)


if __name__ == "__main__":
    main()
