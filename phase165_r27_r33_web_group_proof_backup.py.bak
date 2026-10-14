from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofInlineSegmentView,
    WebGroupProofRenderedLineView,
    WebGroupProofView,
    _group_proof_rule_name,
    _group_proof_statement_latex,
    _split_group_proof_rendered_line,
    _build_group_proof_inline_segments,
    _build_group_proof_rendered_lines,
)

from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_human_readable_renderer import (
  render_toda_public_group_relation_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)



















def build_standard_web_group_proof_view(
    n: int,
    k: int,
    max_depth: int = 2,
    mode: str = "narrative",
) -> WebGroupProofView:
    """Compatibility entry: use only the registered shared backward search."""
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")

    from phase165_r52_r5_auto_search import search_group_structure_automatically
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    result = search_group_structure_automatically(n=n, k=k)
    return build_partial_web_group_proof_view(
        result, max_depth=max_depth, mode=mode,
    )


# Phase 165 R52-R3 explicit partial-result Web entry
def build_web_partial_group_proof_view(
    result, *, max_depth: int = 2, mode: str = "narrative",
) -> WebGroupProofView:
    """Render typed partial evidence through the shared WebGroupProofView."""
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    return build_partial_web_group_proof_view(
        result, max_depth=max_depth, mode=mode,
    )
