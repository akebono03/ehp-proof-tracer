"""Assertions for reference-attributed proof prose.

Only the mechanically attached [R#] preface may differ from flat prose.
The complete underlying step text and its multiplicity must be preserved.
"""

from collections import Counter
import re


_REFERENCE_LEAD = re.compile(
    r"^(?:\[R[0-9]+\](?:, )?)+(?:より|を用いて)、"
)


def strip_reference_lead(line: str) -> str:
    return _REFERENCE_LEAD.sub("", line)


def assert_composed_steps_preserved(composed_lines, flat_lines) -> None:
    assert len(composed_lines) == len(flat_lines)
    assert Counter(strip_reference_lead(line) for line in composed_lines) == Counter(
        strip_reference_lead(line) for line in flat_lines
    )
