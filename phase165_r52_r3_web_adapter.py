"""Phase 165 R52-R3: common WebGroupProofView for partial proof states.

The adapter does not search for evidence, infer mathematical statements or
promote unproved goals into proven steps. Existing narrative rendering is
preserved for legacy complete proofs.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, render_partial_proof_markdown
from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofView,
    _build_group_proof_rendered_lines,
    _group_proof_rule_name,
    _group_proof_statement_latex,
)


def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
) -> WebGroupProofView:
    """Adapt an already observed proof state to the existing Web view contract.

    No range restriction is used and there is no per-group rendering branch.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    # A target expression is not a proof of its group structure.
    target_latex = rf"\pi_{{{dimension}}}^{{{n}}}"

    steps = []
    for step in result.proven_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(
            step.conclusion
        )
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    markdown = render_partial_proof_markdown(result)
    rendered_lines = _build_group_proof_rendered_lines(markdown)
    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key="generic-partial-proof",
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=True,
    )
