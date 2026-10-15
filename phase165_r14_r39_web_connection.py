"""Compatibility entry for the retired R39 fixed-text Web narrative.

The historical API is retained temporarily for import compatibility; it does
not create or render a proof and never selects a per-group narrative.
"""

from web_group_proof import build_standard_web_group_proof_view


def build_phase165_pi32_web_view(max_depth: int = 2, mode: str = "narrative"):
    """Delegate the legacy call to the unified Web proof entry."""
    return build_standard_web_group_proof_view(
        n=2,
        k=1,
        max_depth=max_depth,
        mode=mode,
    )
