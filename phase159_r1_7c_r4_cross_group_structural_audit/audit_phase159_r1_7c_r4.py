from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from toda_calculation_facade import (
    build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)


@dataclass(frozen=True)
class AuditTarget:
    label: str
    n: int
    k: int
    purpose: str


TARGETS = (
    AuditTarget(
        label="pi3_2",
        n=2,
        k=1,
        purpose=(
            "short exact sequence / injective-surjective-isomorphism "
            "presentation control"
        ),
    ),
    AuditTarget(
        label="pi6_3",
        n=3,
        k=3,
        purpose=(
            "complex EHP proof control; R3 repair4 should remain a no-op"
        ),
    ),
    AuditTarget(
        label="pi8_5",
        n=5,
        k=3,
        purpose=(
            "cross-group public Narrative presentation control"
        ),
    ),
    AuditTarget(
        label="pi10_4",
        n=4,
        k=6,
        purpose=(
            "nontrivial reference/body linkage control"
        ),
    ),
    AuditTarget(
        label="pi11_4",
        n=4,
        k=7,
        purpose=(
            "R3 known-result ancestry suppression + direct-premise "
            "specialization + reference component pruning control"
        ),
    ),
)


FORBIDDEN_OR_SUSPICIOUS_FRAGMENTS = (
    "を示す.",
    "である.",
    "を得る.",
    "ProofStep",
    "Relation(",
    "ScalarGreaterEqualStatement",
)


def _build_data(target: AuditTarget):
    report = build_standard_toda_report(
        n=target.n,
        k=target.k,
    )

    if not report.candidates:
        raise RuntimeError(
            f"{target.label}: build_standard_toda_report returned no candidates"
        )

    group_result = (
        report
        .candidates[0]
        .source_candidate
        .group_result
    )

    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
    )

    raw = build_toda_group_proof_presentation(
        replay
    )

    semantic = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            raw
        )
    )

    rendered = render_toda_group_proof_narrative_markdown(
        raw
    )

    references = (
        build_toda_group_proof_narrative_reference_entries(
            semantic
        )
    )

    return (
        raw,
        semantic,
        rendered,
        references,
    )


def _root_direct_premises(presentation):
    return tuple(
        sorted(
            (
                edge
                for edge in presentation.edges
                if edge.parent_step is presentation.root_step
            ),
            key=lambda edge: edge.premise_index,
        )
    )


def _reference_summary(references):
    rows = []

    for index, entry in enumerate(
        references,
        start=1,
    ):
        reference = entry.reference
        rows.append(
            (
                index,
                reference.locator,
                reference.label,
                len(entry.proof_steps),
            )
        )

    return tuple(rows)


def _suspicious_fragments(rendered: str):
    return tuple(
        fragment
        for fragment in FORBIDDEN_OR_SUSPICIOUS_FRAGMENTS
        if fragment in rendered
    )


def _write_target_report(
    output_dir: Path,
    target: AuditTarget,
    raw,
    semantic,
    rendered: str,
    references,
):
    direct_premises = _root_direct_premises(
        semantic
    )

    report_lines = [
        f"# {target.label}",
        "",
        f"- n={target.n}",
        f"- k={target.k}",
        f"- purpose={target.purpose}",
        f"- raw_nodes={len(raw.nodes)}",
        f"- raw_edges={len(raw.edges)}",
        f"- semantic_nodes={len(semantic.nodes)}",
        f"- semantic_edges={len(semantic.edges)}",
        f"- root_direct_premises={len(direct_premises)}",
        f"- reference_entries={len(references)}",
        "",
        "## Root direct premises",
        "",
    ]

    for edge in direct_premises:
        step = edge.premise_step
        rule_name = (
            step.inference_rule.name
            if step.inference_rule is not None
            else "<none>"
        )
        report_lines.extend(
            (
                f"- premise_index={edge.premise_index}",
                f"  conclusion_type={type(step.conclusion).__name__}",
                f"  inference_rule={rule_name}",
            )
        )

    report_lines.extend(
        (
            "",
            "## References",
            "",
        )
    )

    reference_rows = _reference_summary(
        references
    )

    if not reference_rows:
        report_lines.append("- <none>")
    else:
        for (
            index,
            locator,
            label,
            step_count,
        ) in reference_rows:
            report_lines.append(
                f"- R{index}: locator={locator!r}; "
                f"label={label!r}; proof_steps={step_count}"
            )

    suspicious = _suspicious_fragments(
        rendered
    )

    report_lines.extend(
        (
            "",
            "## Suspicious fragments",
            "",
        )
    )

    if suspicious:
        for fragment in suspicious:
            report_lines.append(
                f"- {fragment!r}"
            )
    else:
        report_lines.append("- <none>")

    report_lines.extend(
        (
            "",
            "## Public Narrative",
            "",
            rendered,
            "",
        )
    )

    target_path = (
        output_dir
        / f"{target.label}.md"
    )
    target_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    return {
        "label": target.label,
        "n": target.n,
        "k": target.k,
        "raw_nodes": len(raw.nodes),
        "raw_edges": len(raw.edges),
        "semantic_nodes": len(semantic.nodes),
        "semantic_edges": len(semantic.edges),
        "root_direct_premises": len(direct_premises),
        "reference_entries": len(references),
        "suspicious_fragments": suspicious,
        "path": target_path,
    }


def main():
    output_dir = (
        Path(__file__).resolve().parent
        / "output"
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summaries = []

    for target in TARGETS:
        (
            raw,
            semantic,
            rendered,
            references,
        ) = _build_data(
            target
        )

        summary = _write_target_report(
            output_dir=output_dir,
            target=target,
            raw=raw,
            semantic=semantic,
            rendered=rendered,
            references=references,
        )
        summaries.append(
            summary
        )

    summary_lines = [
        "# Phase 159 R1-7c R4 cross-group structural audit",
        "",
        (
            "Purpose: identify the first remaining structural Narrative defect "
            "after R3 without changing production code."
        ),
        "",
        "## Targets",
        "",
    ]

    for summary in summaries:
        summary_lines.extend(
            (
                f"### {summary['label']}",
                "",
                f"- n={summary['n']}",
                f"- k={summary['k']}",
                f"- raw_nodes={summary['raw_nodes']}",
                f"- raw_edges={summary['raw_edges']}",
                f"- semantic_nodes={summary['semantic_nodes']}",
                f"- semantic_edges={summary['semantic_edges']}",
                (
                    "- root_direct_premises="
                    f"{summary['root_direct_premises']}"
                ),
                (
                    "- reference_entries="
                    f"{summary['reference_entries']}"
                ),
                (
                    "- suspicious_fragments="
                    + (
                        ", ".join(
                            repr(value)
                            for value in summary["suspicious_fragments"]
                        )
                        if summary["suspicious_fragments"]
                        else "<none>"
                    )
                ),
                f"- detail={summary['path'].name}",
                "",
            )
        )

    summary_path = (
        output_dir
        / "summary.md"
    )
    summary_path.write_text(
        "\n".join(summary_lines),
        encoding="utf-8",
    )

    print("=" * 62)
    print("Phase 159 R1-7c R4 - cross-group structural audit")
    print("=" * 62)
    print(f"Output: {output_dir}")
    print("")
    for summary in summaries:
        print(
            f"{summary['label']}: "
            f"direct={summary['root_direct_premises']}, "
            f"references={summary['reference_entries']}, "
            f"suspicious={len(summary['suspicious_fragments'])}"
        )
    print("")
    print("R4 is audit-only.")
    print("Production code changes: none")
    print("Existing test changes: none")
    print("Repository-wide pytest: not run")


if __name__ == "__main__":
    main()
