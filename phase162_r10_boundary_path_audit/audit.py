"""Phase 162 R10: read-only audit of the (5.3) citation boundary.

Run from a checked-out EHP Proof Tracer repository. This program does not
modify the proof tree or its renderer.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from proof import ProofStep
from probes.probe_phase58_capabilities import build_phase58_representative_result
from phase162_web_narrative_integration import _build_phase162_existing_group_connection


def ancestors(root: ProofStep) -> tuple[ProofStep, ...]:
    seen: set[int] = set()
    active: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("A proof premise is not a ProofStep")
        identity = id(step)
        if identity in active:
            raise ValueError("Cyclic ProofStep ancestry")
        if identity in seen:
            return
        active.add(identity)
        for premise in step.premises:
            visit(premise)
        active.remove(identity)
        seen.add(identity)
        ordered.append(step)

    visit(root)
    return tuple(ordered)


def snapshot(root: ProofStep) -> list[dict[str, Any]]:
    ordered = ancestors(root)
    ids = {id(step): index for index, step in enumerate(ordered, 1)}
    rows: list[dict[str, Any]] = []
    for step in ordered:
        reference = getattr(step.inference_rule, "literature_reference", None)
        source = getattr(step.conclusion, "source", None)
        rows.append({
            "index": ids[id(step)],
            "statement_type": type(step.conclusion).__name__,
            "conclusion_repr": repr(step.conclusion)[:1200],
            "rule": step.rule.value,
            "inference_rule": step.inference_rule.name if step.inference_rule else None,
            "rule_reference": getattr(reference, "locator", None),
            "relation_source": getattr(source, "locator", source if isinstance(source, str) else None),
            "premise_indices": [ids[id(p)] for p in step.premises],
            "foundational_reference": repr(step.foundational_reference) if step.foundational_reference else None,
        })
    return rows


def _find_r9_files(root: Path) -> list[str]:
    names = []
    for folder in (root, root / "tests"):
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if "phase162_r9" in path.name.lower():
                names.append(str(path.relative_to(root)))
    return sorted(names)


def main() -> None:
    root = Path.cwd()
    source = build_phase58_representative_result()
    connection = _build_phase162_existing_group_connection()
    graph_root = connection.reconstruction.final_step
    graph = snapshot(graph_root)
    candidate = source["final_hopf_step"]
    candidate_graph = snapshot(candidate)
    lemma_nodes = [r for r in candidate_graph if "lemma52" in (r["inference_rule"] or "").lower() or "lemma 5.2" in (r["inference_rule"] or "").lower()]
    same_conclusion = [r for r in graph if r["conclusion_repr"] == repr(candidate.conclusion)[:1200]]
    result = {
        "purpose": "Read-only reference boundary ancestry audit, not a proof or patch",
        "r9_files_on_disk": _find_r9_files(root),
        "final_group_statement": repr(graph_root.conclusion),
        "graph_node_count": len(graph),
        "hopf_witness_conclusion": repr(candidate.conclusion),
        "hopf_witness_ancestry_count": len(candidate_graph),
        "hopf_witness_lemma52_nodes": lemma_nodes,
        "same_conclusion_in_final_tree": same_conclusion,
        "graph": graph,
        "hopf_witness_graph": candidate_graph,
    }
    output = root / "phase162_r10_boundary_path_audit.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("R10 read-only audit")
    print("R9 paths:", result["r9_files_on_disk"])
    print("Final group proof nodes:", len(graph))
    print("H(nu-prime) source ancestry nodes:", len(candidate_graph))
    print("Lemma 5.2 inference nodes:", len(lemma_nodes))
    print("Matching H(nu-prime) conclusion nodes in final proof:", len(same_conclusion))
    print("Report:", output)
    if not same_conclusion:
        print("NOTE: equality of displayed conclusions does not establish ProofStep identity; inspect JSON graph.")


if __name__ == "__main__":
    main()
