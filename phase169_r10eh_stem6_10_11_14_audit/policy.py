"""Pure classification for the R10EH audit; no theorem is inferred here."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    n: int
    k: int
    expected_status: str

    @property
    def identifier(self) -> str:
        return f"pi_{self.n + self.k}^{self.n}"


CASES = (
    Case(22, 6, "complete"),
    Case(22, 10, "complete"),
    Case(22, 11, "partial"),
    Case(22, 14, "partial"),
)


def expected_coverage(cases: tuple[Case, ...] = CASES) -> bool:
    """Test representative stem/status diversity, not mathematical validity."""
    if not isinstance(cases, tuple) or len(cases) != 4:
        return False
    if len({(case.n, case.k) for case in cases}) != len(cases):
        return False
    if {case.k for case in cases} != {6, 10, 11, 14}:
        return False
    return (sum(case.expected_status == "complete" for case in cases) == 2
            and sum(case.expected_status == "partial" for case in cases) == 2)


def classify_observation(expected: str, actual: str, trust: str) -> str:
    """Incomplete search is never a completed proof, regardless of UI labels."""
    if expected not in ("complete", "partial"):
        return "INVALID_EXPECTATION"
    if actual != expected:
        return "STATUS_CHANGED"
    if actual == "complete":
        return "PASS" if trust == "PASS" else "TRUST_NOT_VERIFIED"
    return "EXPECTED_INCOMPLETE"


def source_record_status(family_id: int, reviewed_ids: frozenset[int]) -> str:
    """HyoujiGen names cannot promote unchecked formulae to GIVEN."""
    if type(family_id) is not int:
        return "INVALID_FAMILY_ID"
    if family_id == 2:
        return "LEGACY_ETA_DEFINITION_PATH"
    if family_id in reviewed_ids:
        return "REVIEWED_GENERIC_FAMILY_SOURCE"
    return "NO_REVIEWED_GENERIC_FAMILY_SOURCE_IN_THIS_REGISTRY"
