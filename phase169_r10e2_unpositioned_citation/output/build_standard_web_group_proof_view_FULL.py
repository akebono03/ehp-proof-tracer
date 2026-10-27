def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
  *,
  goal=None,
  citation_source: str = "model",
) -> WebGroupProofView:
  """Render canonical Web proofs; reject unverifiable complete proof trees.

  Complete model narratives must cross the searched/screened proof boundary.
  Partial and explicitly requested legacy/trace routes retain their old APIs
  without being marked as verified.
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
  from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
  )

  if result.status is ProofSearchStatus.COMPLETE:
    if not search_contexts:
      raise UnverifiedProofTree("complete proof has no screened search context")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    # A DB goal need not have a publication assertion. For this derived-only
    # route, require an actual typed group target before invoking the gate.
    # Synthetic/untyped completed results retain the previous fail-closed path.
    if citing_id is None:
      from homotopy_groups import TodaPrimaryGroupZeroStatement
      from proof import Relation, RelationType
      valid_derived_group = (
        isinstance(result.conclusion, Relation)
        and result.conclusion.relation_type is RelationType.EQUALITY
        and result.conclusion.lhs == result.target
      ) or (
        isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
        and result.conclusion.group == result.target
      )
      if not valid_derived_group:
        raise UnverifiedProofTree("complete unpositioned proof lacks a typed group target")
    # Keep the existing positioned-Goal call signature byte-for-byte.
    # The new keyword is passed only to genuinely unpositioned targets.
    if citing_id is None:
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=None,
        derived_target_without_citing_id=True,
      )
    else:
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
