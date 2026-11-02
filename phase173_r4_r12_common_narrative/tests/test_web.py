"""Public Web trust-boundary regressions, run after installation only."""
from __future__ import annotations

import pytest

from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11))
def test_completed_public_web_toda56_narratives(dimension: int) -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=dimension - 4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert view.rendered_lines
    math = [segment.value for line in view.rendered_lines for segment in line.segments
            if segment.kind in ("inline_math", "display_math")]
    assert any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in formula for formula in math)
    if dimension != 7:
        assert any(rf"\Phi_{{{dimension}}}:" in formula for formula in math)
