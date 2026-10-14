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
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import (
  TodaGroupQueryDomainKind,
  classify_toda_group_query_domain,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_outline_renderer import (
  render_toda_group_proof_outline_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
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
  """Render every group through the same presentation and narrative pipeline."""
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for repository-backed group results")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  report = build_standard_toda_report(n=n, k=k)
  if report.status is TodaCalculationStatus.NOT_FOUND:
    raise ValueError("no proof-backed group result found")
  if report.status is TodaCalculationStatus.MULTIPLE_RESULTS:
    raise ValueError("group proof requires exactly one result")
  group_result = report.candidates[0].source_candidate.group_result

  from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
  replay = build_phase164_r5_r2_common_replay(
    n=n, k=k, group_result=group_result, max_depth=max_depth, mode=mode,
  )

  conclusion_latex, conclusion_fallback = _group_proof_statement_latex(
    replay.root_step.conclusion
  )
  if conclusion_latex is None:
    raise ValueError(
      "group conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  steps = []
  for replay_step in replay.steps:
    statement_latex, fallback_type_name = _group_proof_statement_latex(
      replay_step.proof_step.conclusion
    )
    steps.append(WebGroupProofStepView(
      depth=replay_step.depth,
      statement_latex=statement_latex,
      fallback_type_name=fallback_type_name,
      rule_name=_group_proof_rule_name(replay_step.proof_step),
      role_name=replay_step.role.value,
    ))

  rendered_lines = ()
  if mode != "trace":
    presentation = build_toda_group_proof_presentation(replay)
    if mode == "outline":
      markdown = render_toda_group_proof_outline_markdown(presentation)
    else:
      markdown = render_toda_group_proof_narrative_markdown(presentation)
    rendered_lines = _build_group_proof_rendered_lines(markdown)

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(steps),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
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
