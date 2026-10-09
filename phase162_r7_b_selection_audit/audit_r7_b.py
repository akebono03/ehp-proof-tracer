"""Phase 162 R7-B: read-only pi_5^3 narrative-selection tracing."""

from collections import Counter
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
import re

import toda_group_proof_narrative_contribution_renderer as contribution_renderer
from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import toda_eta_family_definition_statement


TRACKED_STAGES = (
    "render_toda_group_proof_narrative_multi_argument_markdown",
    "_insert_toda_group_proof_narrative_argument_contributions",
    "insert_toda_group_proof_narrative_reason_prose",
    "suppress_toda_group_proof_narrative_reference_internal_body",
    "suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry",
    "suppress_toda_group_proof_narrative_reference_body_duplicates",
    "link_toda_group_proof_narrative_reference_body_consumers",
    "normalize_toda_group_proof_narrative_connectors",
    "order_toda_group_proof_narrative_local_equation_derivations",
    "order_toda_group_proof_narrative_order_support",
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    "insert_toda_group_proof_narrative_map_property_dependencies",
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
    "merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows",
    "trim_toda_group_proof_narrative_redundant_left_ehp_terms",
    "normalize_toda_group_proof_narrative_repeated_numeric_equalities",
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
    "suppress_toda_group_proof_narrative_reflexive_equalities",
    "order_toda_group_proof_narrative_surjectivity_support",
    "order_toda_group_proof_narrative_short_exact_support",
    "suppress_toda_group_proof_narrative_repeated_reference_restatements",
    "suppress_toda_group_proof_narrative_dangling_connectors",
    "order_toda_group_proof_narrative_visible_relation_dependencies",
    "suppress_toda_group_proof_narrative_repeated_unique_step_statements",
    "order_toda_group_proof_narrative_visible_step_dependencies",
    "normalize_toda_group_proof_narrative_zero_map_exactness_reason",
    "order_toda_group_proof_narrative_injective_image_order_reason",
    "specialize_toda_group_proof_narrative_root_zero_direct_premises",
    "specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application",
    "suppress_toda_group_proof_narrative_literal_reflexive_equalities",
    "suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements",
)


@dataclass(frozen=True)
class Snapshot:
    stage: str
    text: str


def _paragraphs(markdown: str) -> tuple[str, ...]:
    return tuple(p.strip() for p in re.split(r"\n\s*\n", markdown) if p.strip())


def _category(paragraph: str) -> tuple[str, ...]:
    marks = []
    if r"\pi_{3}^{2}" in paragraph:
        marks.append("pi3_2")
    if r"\pi_{4}^{3}" in paragraph:
        marks.append("pi4_3")
    if r"E^{n - 3}" in paragraph or r"\pi_{n + 1}^{n}" in paragraph:
        marks.append("stable_generic")
    if r"\pi_{5}^{3}" in paragraph:
        marks.append("target_pi5_3")
    if r"\Delta" in paragraph or "Δ" in paragraph:
        marks.append("delta")
    if r"\xrightarrow" in paragraph:
        marks.append("exactness_or_maps")
    return tuple(marks)


def _stats(markdown: str) -> Counter:
    result = Counter()
    for paragraph in _paragraphs(markdown):
        for mark in _category(paragraph):
            result[mark] += 1
    return result


def _capture_renderer(func, stage: str, captured: list[Snapshot]):
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            captured.append(Snapshot(stage, result))
        return result
    return wrapped


def collect_r7_b_snapshots():
    """Instrument existing text stages without modifying or replacing proof steps."""
    originals = {}
    captured = []
    for stage in TRACKED_STAGES:
        func = getattr(contribution_renderer, stage, None)
        if not callable(func):
            continue
        originals[stage] = func
        setattr(contribution_renderer, stage, _capture_renderer(func, stage, captured))
    try:
        pi4 = build_phase59_2_data()["result_steps"][0]
        definitions = tuple(
            ProofStep(
                conclusion=toda_eta_family_definition_statement(index),
                premises=(),
                rule=ProofRule.GIVEN,
            )
            for index in (3, 4)
        )
        leaves = build_phase59_3_data()["premise_steps"]
        audit = render_phase162_pi5_3_reconstructed_proof(pi4, definitions, leaves)
    finally:
        for stage, func in originals.items():
            setattr(contribution_renderer, stage, func)
    return audit, tuple(captured)


def build_report(audit, snapshots: tuple[Snapshot, ...]) -> str:
    lines = [
        "# Phase 162 R7-B: narrative selection vs. ProofStep provenance",
        "", "## Scope",
        "Read-only diagnosis; no changes to ProofStep, references, or renderer.",
        f"Root: {audit.final_step.conclusion!r}",
        f"Presentation nodes: {len(audit.presentation.nodes)}",
        f"Presentation edges: {len(audit.presentation.edges)}",
        "", "## Direct root premises",
    ]
    for number, step in enumerate(audit.final_step.premises, 1):
        name = getattr(step.inference_rule, "name", "")
        lines.append(f"{number}. {name}: {step.conclusion!r}")
    lines += ["", "## Source narrative stages (ordered)"]
    previous = Counter()
    first = {}
    for index, shot in enumerate(snapshots, 1):
        counts = _stats(shot.text)
        # Functions may be called repeatedly: every invocation is recorded.
        lines.append(f"{index:02d} {shot.stage}: {dict(counts)}")
        for key in ("pi3_2", "pi4_3", "stable_generic", "target_pi5_3"):
            if key not in first and counts[key] > 0:
                first[key] = (index, shot.stage)
        deltas = {key: counts[key] - previous[key] for key in set(counts) | set(previous) if counts[key] != previous[key]}
        if deltas:
            lines.append(f"    changes from preceding snapshot: {deltas}")
        previous = counts
    lines += ["", "## First observed stage for each paragraph category"]
    for key in ("pi3_2", "pi4_3", "stable_generic", "target_pi5_3"):
        lines.append(f"{key}: {first.get(key, 'not seen in captured stages')}")
    lines += ["", "## Repeated exact paragraphs in final public narrative"]
    paragraphs = _paragraphs(audit.markdown)
    counts = Counter(paragraphs)
    for para, count in counts.most_common():
        if count < 2:
            continue
        if not _category(para):
            continue
        lines.append(f"x{count}: {para[:240]}")
    lines += ["", "## Stable-generic paragraphs in final narrative"]
    for index, para in enumerate(paragraphs, 1):
        if "stable_generic" in _category(para):
            lines.append(f"paragraph {index}: {para[:650]}")
    lines += ["", "## Generator-transport final conclusion context"]
    for index, para in enumerate(paragraphs):
        if "target_pi5_3" in _category(para):
            lines.append(f"paragraph {index + 1}: {para[:650]}")
    lines += ["", "## Provenance steps matching suspect rule labels"]
    terms = ("stable", "iterated suspension", "transport", "finite-cyclic", "eta-square")
    for node in audit.presentation.nodes:
        step = node.proof_step
        name = getattr(step.inference_rule, "name", "") or ""
        if any(term in name.lower() for term in terms):
            lines.append(f"depth={node.depth} {name}: {str(step.conclusion)[:350]}")
    lines += ["", "## Final public narrative", audit.markdown]
    return "\n".join(lines) + "\n"


def main() -> None:
    audit, snapshots = collect_r7_b_snapshots()
    report = build_report(audit, snapshots)
    output = Path(__file__).resolve().parent / "pi5_3_r7_b_selection_report.txt"
    output.write_text(report, encoding="utf-8")
    print("R7-B read-only audit completed")
    print("Root step preserved:", audit.presentation.root_step is audit.final_step)
    print("Nodes:", len(audit.presentation.nodes), "Edges:", len(audit.presentation.edges))
    print("Captured stage invocations:", len(snapshots))
    print("Final paragraph categories:", dict(_stats(audit.markdown)))
    print("Final duplicate categorized paragraphs:", sum(n - 1 for para, n in Counter(_paragraphs(audit.markdown)).items() if n > 1 and _category(para)))
    print("Report:", output)
    print("--- STAGE AND FIRST-APPEARANCE SUMMARY ---")
    for line in report.splitlines():
        if line.startswith("## Repeated exact paragraphs"):
            break
        if line.startswith("## ") or line.startswith("pi3_2:") or line.startswith("pi4_3:") or line.startswith("stable_generic:") or line.startswith("target_pi5_3:") or "changes from preceding" in line:
            print(line)
    print("No production source files modified; no full suite run.")


if __name__ == "__main__":
    main()
