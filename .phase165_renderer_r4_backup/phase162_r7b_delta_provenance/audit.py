"""Read-only Phase 162 R7-B audit of repeated Delta(iota_5) statements."""
from collections import Counter
from pathlib import Path

from audit_r7_b import collect_r7_b_snapshots, _paragraphs
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_contribution_renderer import (
    _phase157_r11_reference_statement_match_key,
)

DELTA_MARKERS = (r"\Delta\left(\iota_{5}\right)", r"\Delta(\iota_{5})")


def delta_paragraphs(markdown):
    """Retain statements containing Delta(iota_5), with punctuation intact."""
    return tuple(
        paragraph for paragraph in _paragraphs(markdown)
        if any(marker in paragraph for marker in DELTA_MARKERS)
    )


def exact_key(paragraph):
    return _phase157_r11_reference_statement_match_key(paragraph.strip())


def build_report(audit, snapshots):
    lines = [
        "# Phase 162 R7-B Delta premise provenance",
        "Read-only: no replacement of renderer output and no ProofStep mutation.",
        f"Root preserved: {audit.final_step is audit.presentation.root_step}",
        f"Nodes: {len(audit.presentation.nodes)}; edges: {len(audit.presentation.edges)}",
        "",
        "## Step identities with matching rendered mathematical statement",
    ]
    selected = []
    for node in audit.presentation.nodes:
        step = node.proof_step
        rendered = _render_generic_narrative_step(step)
        if not isinstance(rendered, str):
            continue
        if any(marker in rendered for marker in DELTA_MARKERS):
            selected.append((node.depth, step, rendered))
    for n, (depth, step, rendered) in enumerate(selected, 1):
        rule = getattr(getattr(step, "inference_rule", None), "name", None)
        lines.extend((
            f"{n}. depth={depth} step_id={id(step)} rule={step.rule.value} inference={rule}",
            f"   conclusion={step.conclusion!r}",
            f"   rendered={rendered}",
            f"   premises={len(step.premises)}",
            f"   equivalence_key={exact_key(rendered)!r}",
        ))
    by_conclusion = {}
    for _, step, _ in selected:
        by_conclusion.setdefault(repr(step.conclusion), []).append(id(step))
    lines += [
        "",
        f"Matching ProofStep identities: {len({id(s) for _, s, _ in selected})}",
        f"Distinct structural conclusions: {len(by_conclusion)}",
        "## Conclusion equivalence groups (by repr, diagnostic only)",
    ]
    for ids in by_conclusion.values():
        lines.append(f"step_count={len(ids)} identities={ids}")
    lines += ["", "## Paragraph counts after selected renderer stages"]
    previous_count = None
    for number, snapshot in enumerate(snapshots, 1):
        paragraphs = delta_paragraphs(snapshot.text)
        count = len(paragraphs)
        if previous_count is None or count != previous_count:
            lines.append(f"{number:02d} {snapshot.stage}: {count} delta paragraphs (change={None if previous_count is None else count-previous_count})")
        previous_count = count
    final_paragraphs = delta_paragraphs(audit.markdown)
    lines += ["", "## Final public narrative Delta paragraphs"]
    for n, paragraph in enumerate(final_paragraphs, 1):
        key = exact_key(paragraph)
        matching = [id(step) for _, step, rendered in selected if exact_key(rendered) == key]
        lines.append(f"{n}. text={paragraph!r}")
        lines.append(f"   matching_step_ids={matching} (diagnostic, not ownership proof)")
        lines.append(f"   normalized_key={key!r}")
    counts = Counter(exact_key(text) for text in final_paragraphs)
    lines += [
        "",
        f"Final matching paragraphs: {len(final_paragraphs)}",
        f"Distinct normalized text keys: {len(counts)}",
        "## Interpretation warning",
        "Same normalized text does not imply the same ProofStep identity or redundant mathematical support.",
        "No deduplication was attempted.",
    ]
    return "\n".join(lines) + "\n"


def main():
    audit, snapshots = collect_r7_b_snapshots()
    report = build_report(audit, snapshots)
    destination = Path(__file__).resolve().parent / "pi5_3_r7b_delta_provenance.txt"
    destination.write_text(report, encoding="utf-8")
    print(report)
    print("Report:", destination)
    print("Read-only audit complete. Full suite not run.")


if __name__ == "__main__":
    main()
