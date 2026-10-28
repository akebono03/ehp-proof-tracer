"""Pure diagnostic helpers; they do not establish any proof relation."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re


IMAGE_PATTERN = re.compile(r"\$E\(([^$\n]+)\)=([^$\n]+)\$")


@dataclass(frozen=True)
class AuditCase:
    n: int
    k: int
    expected_r10a: bool
    expected_duplicates: int

    @property
    def label(self) -> str:
        return f"pi_{self.n + self.k}^{self.n}"


CASES = (
    AuditCase(22, 6, True, 0),
    AuditCase(22, 10, False, 10),
)


def image_formula_occurrences(markdown: str) -> tuple[dict, ...]:
    """Inventory exactly displayed one-step equations; no inference from text."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")
    found = Counter(
        (match.group(1), match.group(2))
        for match in IMAGE_PATTERN.finditer(markdown)
    )
    return tuple(
        {"source_tex": source, "target_tex": target, "copies": count}
        for (source, target), count in sorted(found.items())
    )


def extra_duplicate_occurrences(rows: tuple[dict, ...]) -> int:
    """Count repeated displayed equations, not repeated proof obligations."""
    return sum(max(0, row["copies"] - 1) for row in rows)


def validate_coverage() -> bool:
    """Keep exactly the independently audited 6- and 10-stem cases."""
    return (
        len(CASES) == 2
        and {(case.n, case.k) for case in CASES} == {(22, 6), (22, 10)}
        and all(case.n >= case.k + 2 for case in CASES)
    )


def assess_case(status: str, trust: str, r10a: bool,
                duplicates: int, case: AuditCase) -> str:
    if status != "complete" or trust != "PASS":
        return "PROOF_VERIFICATION_FAILED"
    if r10a != case.expected_r10a:
        return "PROJECTION_BEHAVIOR_CHANGED"
    if duplicates != case.expected_duplicates:
        return "NARRATIVE_DUPLICATES_CHANGED"
    return "PASS"
