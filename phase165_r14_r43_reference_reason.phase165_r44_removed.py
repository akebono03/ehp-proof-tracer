"""Shared narrative completion based only on actual proof steps, not group IDs."""
from __future__ import annotations

from proof import ProofStep
from toda_group_proof_narrative_references import (
    extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_shared_components import _render_generic_narrative_step


def _reference_rows(presentation):
    groups = {}
    for node in presentation.nodes:
        step = node.proof_step
        if step.premises:
            continue
        reference = extract_toda_group_proof_step_literature_reference(step)
        if reference is None or reference.locator is None:
            continue
        locator = reference.locator
        if locator not in groups:
            groups[locator] = []
        formula = _render_generic_narrative_step(step)
        if formula.startswith("`") or formula.startswith("Toda "):
            continue
        if formula not in groups[locator]:
            groups[locator].append(formula)
    return tuple(
        "Toda " + key + ": " + " ".join(values)
        for key, values in groups.items()
        if values
    )


def _exactness_reason_rows(presentation):
    found = set()
    result = []
    for node in presentation.nodes:
        step = node.proof_step
        if not isinstance(step, ProofStep) or not step.premises:
            continue
        kind = type(step.conclusion).__name__
        family = tuple(type(p.conclusion).__name__ for p in step.premises)
        if "TodaProp42ExactnessStatement" not in family:
            continue
        if kind == "MapInjective" and "TodaPrimaryGroupZeroStatement" in family:
            entry = r"完全性と始域が零群であることから, $\ker H=\operatorname{Im}E=0$."
        elif kind == "MapSurjective" and "TodaDeltaZeroStatement" in family:
            entry = r"完全性と $\Delta=0$ より, $\operatorname{Im}H=\ker\Delta$ であり, $H$ は全射である."
        elif kind == "TodaDeltaZeroStatement" and any("Isomorphism" in name for name in family):
            entry = r"完全性と $E$ の同型性より, $\operatorname{Im}\Delta=\ker E=0$."
        else:
            continue
        if entry not in found:
            found.add(entry)
            result.append(entry)
    return tuple(result)


def enrich_common_narrative(presentation, markdown: str) -> str:
    """Supply filtered-out references and proof-grounded exactness reasons.

    Existing reference content is left untouched.  Never synthesize a source
    from the goal, a proof rule name, or an absent premise.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    lines = markdown.splitlines()
    reference_rows = _reference_rows(presentation)
    # A reference section may be empty because the older boundary classifier
    # rejects the new registered, typed GIVEN facts.
    heading = next((i for i, line in enumerate(lines)
                    if line.strip() in ("使用する結果", "## 使用する結果")), None)
    if heading is not None:
        next_heading = next((i for i in range(heading+1, len(lines))
                             if lines[i].strip() in ("証明", "## 証明")), None)
        if next_heading is not None:
            body = tuple(
                x.strip() for x in lines[heading+1:next_heading]
                if x.strip() and x.strip() != "---"
                and not x.lstrip().startswith("#")
            )
            if not body and reference_rows:
                lines[next_heading:next_heading] = list(reference_rows) + [""]
    rendered = "\n".join(lines)
    reason_rows = _exactness_reason_rows(presentation)
    if reason_rows and "証明" in rendered:
        heading = next((i for i, line in enumerate(lines)
                        if line.strip() in ("証明", "## 証明")), None)
        if heading is not None:
            # Reasons are derived from matched exactness premises, not canned
            # group-specific narratives.  Keep them in proof, not Reference.
            lines[heading+1:heading+1] = list(reason_rows) + [""]
    result = "\n".join(lines)
    if markdown.endswith("\n"):
        result += "\n"
    return result
