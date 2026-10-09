"""Read-only stage provenance pinpoint for Phase 162 R7-B narrative defects."""
from collections import Counter
from functools import wraps
from pathlib import Path

import toda_group_proof_narrative_renderer as public_renderer
from audit_r7_b import collect_r7_b_snapshots, _paragraphs


SUSPECTS = {
    "stable_tail": "証明木に記録された群構造の移送について",
    "stable_general": r"\pi_{n + 1}^{n} =",
    "eta_square_issue": r"\eta_{3}\eta_{3} = \eta_{3}^{2}",
    "repeated_delta": r"\Delta\left(\iota_{5}\right) =",
    "bare_exactness_intro": "次の完全列を考える.",
}


STAGES = (
    "_wrap_phase150_rc4_generic_public_narrative",
    "_finalize_toda_group_proof_narrative_markdown",
    "_phase158_baseline_render_toda_group_proof_narrative_markdown",
    "_phase158_normalize_public_narrative_contract",
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    "_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions",
    "_phase159_r1_6d_finalize_reference_and_linkage",
    "_phase160_r7_render_stable_finite_cyclic_transport_narrative",
)


def capture_public_stages():
    originals = {}
    events = []
    for name in STAGES:
        original = getattr(public_renderer, name, None)
        if not callable(original):
            continue
        originals[name] = original

        def wrapper(*args, _name=name, _original=original, **kwargs):
            result = _original(*args, **kwargs)
            if isinstance(result, str):
                events.append((_name, result))
            return result

        setattr(public_renderer, name, wrapper)
    try:
        audit, snapshots = collect_r7_b_snapshots()
    finally:
        for name, original in originals.items():
            setattr(public_renderer, name, original)
    return audit, snapshots, events


def build_report(audit, snapshots, public_events):
    all_events = [("CONTRIBUTION:" + s.stage, s.text) for s in snapshots]
    all_events += [("PUBLIC:" + name, content) for name, content in public_events]
    all_events.append(("FINAL", audit.markdown))
    lines = [
        "# Phase 162 R7-B: exact paragraph origin pinpoint",
        "Read-only trace. No ProofStep or renderer changes.",
        f"Root preserved: {audit.presentation.root_step is audit.final_step}",
        f"Presentation: {len(audit.presentation.nodes)} nodes; {len(audit.presentation.edges)} edges",
        f"Contributions: {len(snapshots)}; public wrappers: {len(public_events)}",
        "",
    ]
    for title, needle in SUSPECTS.items():
        lines.append(f"## {title} ({needle})")
        first = None
        for idx, (stage, content) in enumerate(all_events, 1):
            count = content.count(needle)
            if count and first is None:
                first = (idx, stage)
            if count:
                lines.append(f"{idx:02d} {stage}: {count}")
        lines.append(f"FIRST: {first}")
        lines.append(f"FINAL COUNT: {audit.markdown.count(needle)}")
        lines.append("")
    paragraphs = _paragraphs(audit.markdown)
    lines.append("## Final body: exact duplicate paragraphs (no category filtering)")
    for para, count in Counter(paragraphs).items():
        if count > 1:
            lines.append(f"{count}x: {para[:280]}")
    lines.append("## Standalone exactness introduction and next paragraph")
    for index, para in enumerate(paragraphs):
        if para == "次の完全列を考える.":
            next_para = paragraphs[index + 1] if index + 1 < len(paragraphs) else "<END>"
            lines.append(f"paragraph {index+1}: next={next_para[:260]!r}")
    lines.append("## Final three paragraphs")
    for para in paragraphs[-3:]:
        lines.append(repr(para))
    return "\n".join(lines) + "\n"


def main():
    audit, snapshots, events = capture_public_stages()
    report = build_report(audit, snapshots, events)
    destination = Path(__file__).resolve().parent / "pi5_3_r7_b_origin_report.txt"
    destination.write_text(report, encoding="utf-8")
    print(report)
    print("Report:", destination)
    print("Read-only stage tracing completed. Full suite not run.")


if __name__ == "__main__":
    main()
