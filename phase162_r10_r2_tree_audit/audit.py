"""Read-only Phase 162 R10-R2 proof ancestry audit for the actual Web replay.

Never changes ProofStep, production code, references or rendered text.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from phase162_web_narrative_integration import _build_phase162_existing_group_connection
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_literature_statement_boundary import (
    TodaLiteratureStatementClassification,
    classify_toda_literature_statement_step,
)
from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference


def ordered_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Enumerate the graph by identity, in post-order, with cycle detection."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be ProofStep")
    active: set[int] = set()
    visited: set[int] = set()
    result: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise ValueError("Non-ProofStep premise")
        identifier = id(step)
        if identifier in active:
            raise ValueError("Cyclic ProofStep ancestry")
        if identifier in visited:
            return
        active.add(identifier)
        for premise in step.premises:
            visit(premise)
        active.remove(identifier)
        visited.add(identifier)
        result.append(step)

    visit(root)
    return tuple(result)


def parent_chains(root: ProofStep, target: ProofStep, limit: int = 12) -> list[list[ProofStep]]:
    """Find exact identity paths from root to target without inventing edges."""
    paths: list[list[ProofStep]] = []

    def visit(step: ProofStep, path: tuple[ProofStep, ...], active: frozenset[int]) -> None:
        if len(paths) >= limit:
            return
        if id(step) in active:
            raise ValueError("Cyclic ProofStep ancestry")
        next_path = path + (step,)
        if step is target:
            paths.append(list(next_path))
            return
        for premise in step.premises:
            visit(premise, next_path, active | {id(step)})

    visit(root, (), frozenset())
    return paths


def _reference(step: ProofStep) -> tuple[str | None, str | None, str | None]:
    boundary = classify_toda_literature_statement_step(step)
    ref = extract_toda_group_proof_step_literature_reference(step)
    return (
        boundary.classification.value if boundary is not None else None,
        boundary.component_key if boundary is not None else None,
        ref.locator if ref is not None else None,
    )


def _field(value: object) -> dict[str, str]:
    output = {}
    for name in ("map", "source_group", "target_group"):
        attribute = getattr(value, name, None)
        if attribute is not None:
            output[name] = repr(attribute)[:450]
    return output


def graph_report(root: ProofStep, hopf_conclusion: object) -> dict[str, Any]:
    steps = ordered_ancestry(root)
    numbers = {id(step): index for index, step in enumerate(steps, 1)}
    consumers: dict[int, list[int]] = defaultdict(list)
    for step in steps:
        for premise in step.premises:
            consumers[id(premise)].append(numbers[id(step)])
    rows = []
    for step in steps:
        classification, component, reference = _reference(step)
        source = getattr(step.conclusion, "source", None)
        cited_identity = step.foundational_reference
        rows.append({
            "node": numbers[id(step)],
            "type": type(step.conclusion).__name__,
            "statement": repr(step.conclusion)[:1800],
            "statement_complete_repr": repr(step.conclusion),
            "rule": step.rule.value,
            "inference_rule": step.inference_rule.name if step.inference_rule else None,
            "premises": [numbers[id(p)] for p in step.premises],
            "consumers": consumers[id(step)],
            "classification": classification,
            "component": component,
            "reference": reference,
            "foundational_key": cited_identity.key if cited_identity is not None else None,
            "foundational_label": cited_identity.label if cited_identity is not None else None,
            "relation_source": getattr(source, "locator", source if isinstance(source, str) else None),
            "map_fields": _field(step.conclusion),
            "is_hopf_conclusion": step.conclusion == hopf_conclusion,
            "is_internal_lemma52": "lemma52" in (step.inference_rule.name.lower() if step.inference_rule else ""),
        })
    duplicates: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        duplicates[row["statement_complete_repr"]].append(row["node"])
    repeated = [ids for ids in duplicates.values() if len(ids) > 1]
    summary = {
        "node_count": len(steps),
        "edges": sum(len(s.premises) for s in steps),
        "given": sum(s.rule is ProofRule.GIVEN for s in steps),
        "inference": sum(s.rule is ProofRule.INFERENCE for s in steps),
        "literature_categories": dict(Counter(row["classification"] or "unclassified" for row in rows)),
        "reference_locators": dict(Counter(row["reference"] for row in rows if row["reference"])),
        "duplicated_conclusion_groups": repeated,
        "hopf_nodes": [row["node"] for row in rows if row["is_hopf_conclusion"]],
        "lemma52_nodes": [row["node"] for row in rows if row["is_internal_lemma52"]],
        "citation_nodes": [row["node"] for row in rows if (row["foundational_key"] or "").startswith("literature:")],
        "map_property_nodes": [row["node"] for row in rows if row["type"].endswith(("InjectiveStatement", "SurjectiveStatement", "IsomorphismStatement", "ZeroStatement"))],
    }
    targets = [row for row in rows if row["is_hopf_conclusion"] or row["is_internal_lemma52"] or row["foundational_key"]]
    traces = {}
    for row in targets:
        step = steps[row["node"] - 1]
        traces[str(row["node"])] = [[numbers[id(node)] for node in chain] for chain in parent_chains(root, step)]
    return {"root": repr(root.conclusion), "root_node": numbers[id(root)], "summary": summary, "node_paths": traces, "nodes": rows}


def _markdown(report: dict[str, Any]) -> str:
    lines = ["# Phase 162 R10-R2 証明木監査", "", "監査対象は実際の Web replay の ProofStep 証明木と旧 R10 再構築経路。読み取り専用。", ""]
    for name, graph in report["graphs"].items():
        s = graph["summary"]
        lines += [f"## {name}", "", f"- nodes: {s['node_count']}, edges: {s['edges']}, GIVEN: {s['given']}, INFERENCE: {s['inference']}", f"- H(nu_prime)=eta5 nodes: {s['hopf_nodes']}", f"- Lemma 5.2 inference nodes: {s['lemma52_nodes']}", f"- cited boundary nodes: {s['citation_nodes']}", f"- repeated conclusions (identity-distinct): {s['duplicated_conclusion_groups']}", "", "### 引用・Lemma 5.2・Hopf の使用経路", ""]
        relevant = set(s["hopf_nodes"] + s["lemma52_nodes"] + s["citation_nodes"])
        for row in graph["nodes"]:
            if row["node"] in relevant:
                lines += [f"- node {row['node']} {row['rule']}, {row['inference_rule'] or '-'}, {row['reference'] or '-'} / {row['component'] or '-'}", f"  - premises={row['premises']}, consumers={row['consumers']}", f"  - root paths={graph['node_paths'].get(str(row['node']), [])}"]
        lines += ["", "### 参考文献の帰属", ""]
        for locator, count in sorted(s["reference_locators"].items()):
            lines.append(f"- {locator}: {count} nodes")
        lines += [""]
    lines += ["## 解釈上の注意", "", "- `root paths` は実在する ProofStep オブジェクトの identity で追跡した依存経路。", "- 結論が同じノードでも、別の引用適用と GIVEN がある場合は2ノードになる。", "- 証明木にない文章が Web に現れる場合は Renderer 側の生成過程を別途調べる。", "- 文献分類があることと外部文献の数学的真偽検証は同義ではない。", ""]
    return "\n".join(lines)


def build_audit() -> dict[str, Any]:
    hopf = build_phase58_representative_result()["expected_final_hopf"]
    actual_replay = build_phase162_pi5_3_web_replay(max_depth=40)
    secondary = _build_phase162_existing_group_connection()
    return {
        "purpose": "Read-only proof tree audit; no production code modifications",
        "graphs": {
            "web_replay": graph_report(actual_replay.root_step, hopf),
            "r10_auxiliary_connection": graph_report(secondary.reconstruction.final_step, hopf),
        },
        "web_replay_depth": actual_replay.max_depth,
    }


def main() -> None:
    report = build_audit()
    output = Path.cwd() / "phase162_r10_r2_tree_audit.json"
    summary = Path.cwd() / "phase162_r10_r2_tree_audit.md"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    summary.write_text(_markdown(report), encoding="utf-8")
    for name, graph in report["graphs"].items():
        s = graph["summary"]
        print(f"{name}: nodes={s['node_count']}, edges={s['edges']}, hopf={s['hopf_nodes']}, lemma52={s['lemma52_nodes']}, citations={s['citation_nodes']}")
    print(f"JSON: {output}")
    print(f"Markdown: {summary}")


if __name__ == "__main__":
    main()
