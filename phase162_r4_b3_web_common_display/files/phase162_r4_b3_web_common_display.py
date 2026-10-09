"""Use the R4-B2 derived proof tree with the existing common narrative renderer.

Only pi_5^4 and pi_6^5 narrative views are affected. The Markdown is passed
unchanged to the existing WebGroupProof line parser and HTML template.
"""

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
)
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay


def build_phase162_r4_b3_web_common_display_view(n: int, k: int, max_depth: int):
    """Build a WebGroupProofView from the same derived common path as the audit."""
    from web_group_proof import (
        WebGroupProofStepView,
        WebGroupProofView,
        _build_group_proof_rendered_lines,
        _group_proof_rule_name,
        _group_proof_statement_latex,
        build_standard_web_group_proof_view,
    )

    # The existing public view supplies source metadata without invoking
    # its dedicated narrative renderer. Its trace steps are not reused.
    original_view = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=max_depth, mode="trace"
    )
    target_report = build_standard_toda_report(n=n, k=k)
    base_report = build_standard_toda_report(n=3, k=1)
    target_result = target_report.candidates[0].source_candidate.group_result
    base_result = base_report.candidates[0].source_candidate.group_result
    derived = build_toda_stable_eta_proof_replay(
        target_result, base_result, max_depth=max(3, max_depth)
    )
    replay = derived.replay
    markdown = _phase158_baseline_render_toda_group_proof_narrative_markdown(
        derived.presentation
    )
    conclusion_latex, fallback = _group_proof_statement_latex(
        replay.root_step.conclusion
    )
    if conclusion_latex is None:
        raise ValueError(f"group conclusion is not renderable as LaTeX: {fallback}")
    steps = []
    for node in replay.steps:
        latex, fallback_name = _group_proof_statement_latex(node.proof_step.conclusion)
        steps.append(
            WebGroupProofStepView(
                depth=node.depth,
                statement_latex=latex,
                fallback_type_name=fallback_name,
                rule_name=_group_proof_rule_name(node.proof_step),
                role_name=node.role.value,
            )
        )
    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=conclusion_latex,
        theorem=original_view.theorem,
        phase=original_view.phase,
        key=original_view.key,
        steps=tuple(steps),
        max_depth=replay.max_depth,
        mode="narrative",
        rendered_lines=_build_group_proof_rendered_lines(markdown),
    )
