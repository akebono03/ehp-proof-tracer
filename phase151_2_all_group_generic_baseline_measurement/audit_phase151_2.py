from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_blocks import TodaGroupProofNarrativeMathematicalBlockRole, build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_contribution_renderer import render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
from toda_group_proof_narrative_reason_renderer import render_toda_group_proof_narrative_reason_sentence
from toda_group_proof_narrative_reasons import build_toda_group_proof_narrative_reason_sidecar
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation, build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112
OUTPUT_DIR = Path(__file__).resolve().parent / "audit_output"

def _label(n: int, k: int) -> str:
    return f"pi_{n + k}^{n}"

def _fallback_kind(step, rendered: str) -> str | None:
    rule = step.inference_rule
    if rule is not None and rendered == rule.name:
        return "rule_name"
    if rendered == "`" + type(step.conclusion).__name__ + "`":
        return "type_name"
    if rendered == repr(step.conclusion):
        return "raw_repr"
    if rendered == str(step.conclusion):
        return "raw_str"
    return None

def _context(n: int, k: int):
    report = build_standard_toda_report(n=n, k=k)
    if not report.candidates:
        raise AssertionError(f"no report candidate for n={n}, k={k}")
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(group_result, max_depth=MAX_DEPTH)
    presentation = build_toda_group_proof_presentation(replay)
    presentation = build_toda_group_proof_narrative_semantic_closure_presentation(presentation)
    semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=semantic_sidecar)
    arguments = build_toda_group_proof_narrative_arguments(presentation, blocks, semantic_sidecar=semantic_sidecar)
    reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(presentation, semantic_sidecar)
    markdown = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation, blocks, semantic_sidecar, arguments
    )
    return presentation, blocks, arguments, reason_sidecar, markdown

def _write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    group_rows = []
    fallback_rows = []
    reason_rows = []
    exception_rows = []
    total_role_counts = Counter()
    total_reason_counts = Counter()
    total_fallback_counts = Counter()

    for n in N_RANGE:
        for k in K_RANGE:
            label = _label(n, k)
            try:
                presentation, blocks, arguments, reason_sidecar, markdown = _context(n, k)
            except Exception as exc:
                exception_rows.append({
                    "n": n, "k": k, "group": label,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                })
                group_rows.append({
                    "n": n, "k": k, "group": label, "success": False,
                    "presentation_nodes": 0, "blocks": 0, "arguments": 0,
                    "typed_reasons": 0, "rendered_typed_reasons": 0,
                    "other_blocks": 0, "raw_fallbacks": 0,
                    "rule_name_fallbacks": 0, "type_fallbacks": 0,
                    "markdown_chars": 0, "exception_type": type(exc).__name__,
                })
                continue

            role_counts = Counter(block.role.value for block in blocks)
            total_role_counts.update(role_counts)
            reason_counts = Counter(reason.kind.value for reason in reason_sidecar.reasons)
            total_reason_counts.update(reason_counts)

            rendered_reason_count = 0
            for index, reason in enumerate(reason_sidecar.reasons):
                sentence = render_toda_group_proof_narrative_reason_sentence(reason)
                if sentence is not None:
                    rendered_reason_count += 1
                reason_rows.append({
                    "n": n, "k": k, "group": label, "reason_index": index,
                    "reason_kind": reason.kind.value,
                    "premise_count": len(reason.premise_steps),
                    "conclusion_type": type(reason.conclusion_step.conclusion).__name__,
                    "sentence_rendered": sentence is not None,
                    "sentence_visible": bool(sentence and sentence in markdown),
                })

            group_fallback_counts = Counter()
            for node_index, node in enumerate(presentation.nodes):
                step = node.proof_step
                rendered = _render_generic_narrative_step(step)
                fallback_kind = _fallback_kind(step, rendered)
                if fallback_kind is None:
                    continue
                group_fallback_counts[fallback_kind] += 1
                total_fallback_counts[fallback_kind] += 1
                fallback_rows.append({
                    "n": n, "k": k, "group": label, "node_index": node_index,
                    "statement_type": type(step.conclusion).__name__,
                    "fallback_kind": fallback_kind,
                    "inference_rule_name": step.inference_rule.name if step.inference_rule is not None else "",
                    "rendered": rendered,
                    "statement_repr": repr(step.conclusion),
                })

            group_rows.append({
                "n": n, "k": k, "group": label, "success": bool(markdown.strip()),
                "presentation_nodes": len(presentation.nodes), "blocks": len(blocks),
                "arguments": len(arguments), "typed_reasons": len(reason_sidecar.reasons),
                "rendered_typed_reasons": rendered_reason_count,
                "other_blocks": role_counts[TodaGroupProofNarrativeMathematicalBlockRole.OTHER.value],
                "raw_fallbacks": group_fallback_counts["raw_repr"] + group_fallback_counts["raw_str"],
                "rule_name_fallbacks": group_fallback_counts["rule_name"],
                "type_fallbacks": group_fallback_counts["type_name"],
                "markdown_chars": len(markdown), "exception_type": "",
            })

    group_fields = ("n","k","group","success","presentation_nodes","blocks","arguments","typed_reasons","rendered_typed_reasons","other_blocks","raw_fallbacks","rule_name_fallbacks","type_fallbacks","markdown_chars","exception_type")
    fallback_fields = ("n","k","group","node_index","statement_type","fallback_kind","inference_rule_name","rendered","statement_repr")
    reason_fields = ("n","k","group","reason_index","reason_kind","premise_count","conclusion_type","sentence_rendered","sentence_visible")
    exception_fields = ("n","k","group","exception_type","exception_message")
    _write_csv(OUTPUT_DIR / "all_group_baseline.csv", group_fields, group_rows)
    _write_csv(OUTPUT_DIR / "fallback_inventory.csv", fallback_fields, fallback_rows)
    _write_csv(OUTPUT_DIR / "typed_reason_inventory.csv", reason_fields, reason_rows)
    _write_csv(OUTPUT_DIR / "exception_inventory.csv", exception_fields, exception_rows)

    success_count = sum(bool(row["success"]) for row in group_rows)
    summary_lines = [
        "=" * 78,
        "Phase 151-2 — All-Group Generic Baseline Measurement",
        "=" * 78,
        f"groups: {len(group_rows)}",
        f"successes: {success_count}",
        f"exceptions: {len(exception_rows)}",
        f"presentation nodes: {sum(int(row['presentation_nodes']) for row in group_rows)}",
        f"blocks: {sum(int(row['blocks']) for row in group_rows)}",
        f"arguments: {sum(int(row['arguments']) for row in group_rows)}",
        f"typed reasons: {sum(int(row['typed_reasons']) for row in group_rows)}",
        f"OTHER blocks: {sum(int(row['other_blocks']) for row in group_rows)}",
        f"raw fallbacks: {total_fallback_counts['raw_repr'] + total_fallback_counts['raw_str']}",
        f"rule-name fallbacks: {total_fallback_counts['rule_name']}",
        f"type fallbacks: {total_fallback_counts['type_name']}",
        "", "Block roles:",
    ]
    for role, count in sorted(total_role_counts.items()):
        summary_lines.append(f"  {role}: {count}")
    summary_lines.extend(("", "Typed reason kinds:"))
    for kind, count in sorted(total_reason_counts.items()):
        summary_lines.append(f"  {kind}: {count}")
    summary_lines.extend(("", "Fallback kinds:"))
    for kind, count in sorted(total_fallback_counts.items()):
        summary_lines.append(f"  {kind}: {count}")
    summary_lines.extend(("", "Output files:",
        "  all_group_baseline.csv",
        "  fallback_inventory.csv",
        "  typed_reason_inventory.csv",
        "  exception_inventory.csv",
        "  baseline_summary.txt",
        "=" * 78))
    summary = "\n".join(summary_lines) + "\n"
    (OUTPUT_DIR / "baseline_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)

    if len(group_rows) != EXPECTED_GROUP_COUNT or success_count != EXPECTED_GROUP_COUNT or exception_rows:
        print("MEASUREMENT COMPLETE WITH FAILURES: preserve the CSV files as the baseline.")
        return 1
    print("PASS: the 112-group generic baseline was measured without changing production behavior.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
