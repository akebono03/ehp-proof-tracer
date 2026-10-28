"""Read-only case coverage policy; no search or mathematical rules."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditCase:
    n: int
    k: int
    expected_suspensions: int
    expected_summands: int


CASES = (
    AuditCase(13, 9, 2, 3),
    AuditCase(15, 8, 5, 2),
    AuditCase(15, 9, 4, 3),
    AuditCase(24, 9, 13, 3),
    AuditCase(30, 9, 19, 3),
)


def validate_coverage(cases: tuple[AuditCase, ...]) -> None:
    """Refuse to call a one-stem or one-length sample a generality audit."""
    if not cases or len(set((c.n, c.k) for c in cases)) != len(cases):
        raise ValueError("R10ED audit cases must be nonempty and distinct")
    if any(type(c.n) is not int or type(c.k) is not int
           or type(c.expected_suspensions) is not int
           or type(c.expected_summands) is not int
           or c.n < 2 or c.k < 0 or c.expected_suspensions < 2
           or c.expected_summands < 2 for c in cases):
        raise ValueError("R10ED audit case has invalid dimensions or coverage")
    if len({c.k for c in cases}) < 2:
        raise ValueError("R10ED must cover at least two different stems")
    if len({c.expected_summands for c in cases}) < 2:
        raise ValueError("R10ED must cover different direct-sum ranks")
    if len({c.expected_suspensions for c in cases}) < 3:
        raise ValueError("R10ED must cover multiple suspension lengths")
