"""Read-only gate for migrating citations without corrupting long-form proofs.

The comparison does not choose citations: ProofNarrativeModel is authoritative.
Legacy labels are inspected only to detect whether a safe cutover is possible.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from phase168_r3_3_proof_narrative_model import ProofNarrativeModel

_HEADING = re.compile(r"\*\*\[R(\d+)\]\s+(.+?)\.\*\*")
_MARKER = re.compile(r"\[R(\d+)\]")


@dataclass(frozen=True)
class NarrativeCutoverReport:
    model_references: tuple[tuple[int, str], ...]
    displayed_references: tuple[tuple[int, str], ...]
    body_numbers: tuple[int, ...]
    issues: tuple[str, ...]

    @property
    def safe_to_reuse_legacy_body(self) -> bool:
        return not self.issues


def inspect_narrative_cutover(model: ProofNarrativeModel, rendered_lines: tuple) -> NarrativeCutoverReport:
    """Reject body reuse unless old citation numbering agrees with the model.

    No source inference, numbering repair, or text modification occurs here.
    """
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if not isinstance(rendered_lines, tuple):
        raise TypeError("rendered_lines must be a tuple")
    wanted = tuple((item.number, item.reference.locator or item.reference.label) for item in model.citations)
    displayed: list[tuple[int, str]] = []
    body_numbers: set[int] = set()
    issues: list[str] = []
    for line in rendered_lines:
        prefix = line.prefix
        suffix = line.suffix
        heading = _HEADING.fullmatch(prefix.strip())
        if heading:
            displayed.append((int(heading.group(1)), heading.group(2)))
            continue
        for number in _MARKER.findall(prefix + suffix):
            body_numbers.add(int(number))
    seen_numbers: set[int] = set()
    for number, locator in displayed:
        if number in seen_numbers:
            issues.append(f"duplicate displayed reference R{number}")
        seen_numbers.add(number)
    if tuple(displayed) != wanted:
        issues.append("displayed citation identities/order differ from ProofNarrativeModel")
    unknown = tuple(sorted(body_numbers - {number for number, _ in wanted}))
    if unknown:
        issues.append(f"body references absent from model: {unknown}")
    return NarrativeCutoverReport(wanted, tuple(displayed), tuple(sorted(body_numbers)), tuple(issues))
