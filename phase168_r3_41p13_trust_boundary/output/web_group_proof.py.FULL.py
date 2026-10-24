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

from toda_human_readable_renderer import (
  render_toda_public_group_relation_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)

from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import TodaGroupQueryDomainKind
from toda_group_query_semantics import classify_toda_group_query_domain


def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
  *,
  goal=None,
  citation_source: str = "model",
) -> WebGroupProofView:
  """Render shared search and screen positioned complete proof trees for Web.

  Unpositioned and partial/legacy contexts remain on their compatibility
  paths. They do not acquire a verified status merely by being projected.
  """
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for positive-dimensional group queries")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")
  if citation_source not in ("legacy", "model"):
    raise ValueError("citation_source must be legacy or model")

  from phase165_r55_nk_only_goal import search_group_from_registered_goal
  from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

  if citation_source == "legacy" or mode == "trace":
    result = search_group_from_registered_goal(n=n, k=k, goal=goal)
    return build_partial_web_group_proof_view(
      result,
      max_depth=max_depth,
      mode=mode,
    )

  from phase165_r52_r9_shared_math import build_shared_typed_bridge
  from phase168_r3_4_link_bridge import build_linked_proof_narrative_model

  bridge = build_shared_typed_bridge()
  search_contexts = []
  result = search_group_from_registered_goal(
    n=n, k=k, goal=goal, bridge=bridge,
    context_sink=search_contexts.append,
  )
  model_bridge = search_contexts[-1] if search_contexts else bridge

  # The public complete/positioned route crosses the proof trust boundary
  # before citation projection. The matcher and chronology are the SAME
  # rules used by search, not new presentation-layer mathematical rules.
  from phase165_r52_partial_proof import ProofSearchStatus
  from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
  from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
  from proof import ProofRule

  if result.status is ProofSearchStatus.COMPLETE and search_contexts:
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing_id is not None and all(
      step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
      for step in result.proven_steps
    ):
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=citing_id,
      )
  model = build_linked_proof_narrative_model(result, model_bridge)
  return build_partial_web_group_proof_view(
    result,
    max_depth=max_depth,
    mode=mode,
    narrative_model=model,
  )


# Phase 165 R52-R3 explicit partial-result Web entry
def build_web_partial_group_proof_view(
    result, *, max_depth: int = 2, mode: str = "narrative",
) -> WebGroupProofView:
    """Render incomplete proof progress with the shared proof-backed Model.

    Completed compatibility results and trace mode retain their former route.
    No new references, proof steps, or search results are inferred.
    """
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus

    narrative_model = None
    if mode != "trace" and result.status is not ProofSearchStatus.COMPLETE:
        from phase168_r3_3_proof_narrative_model import build_proof_narrative_model

        narrative_model = build_proof_narrative_model(result)
    return build_partial_web_group_proof_view(
        result, max_depth=max_depth, mode=mode,
        narrative_model=narrative_model,
    )
