def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  """The single public Narrative entry for complete and incomplete searches."""
  from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
  if isinstance(presentation, PartialProofResult):
    if presentation.status is ProofSearchStatus.COMPLETE:
      from phase165_r56_presentation_adapter import render_completed_shared_narrative
      return render_completed_shared_narrative(presentation)
    from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative
    return render_incomplete_public_narrative(presentation)

  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )
  if stable_transport_narrative is not None:
    return stable_transport_narrative

  rendered = (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
  from phase164_r9_narrative_contract import normalize_public_narrative_contract
  rendered = normalize_public_narrative_contract(
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )
  # Phase 165 R2 order repair: consume existing typed ancestry, not new facts.
  from phase165_r12_r2_quotient_rules import (
    KernelMultipleStatement,
    QuotientIsomorphismStatement,
  )
  from phase165_r57_r10_step_narrative import ordered_proof_ancestry
  replay = getattr(presentation, "source_replay", None)
  group_result = getattr(replay, "group_result", None)
  proof_root = getattr(group_result, "proof_step", None)
  if proof_root is not None:
    ancestry = ordered_proof_ancestry(proof_root)
    kernel_steps = tuple(
      step for step in ancestry
      if isinstance(step.conclusion, KernelMultipleStatement)
    )
    quotient_steps = tuple(
      step for step in ancestry
      if isinstance(step.conclusion, QuotientIsomorphismStatement)
    )
    if kernel_steps and quotient_steps:
      from phase165_r12_r34_r2_semantic_narrative import _element, _group
      paragraphs = rendered.split("\n\n")

      def unique_index(fragment):
        indices = [
          index for index, paragraph in enumerate(paragraphs)
          if fragment in paragraph
        ]
        if len(indices) != 1:
          raise ValueError(
            "R2: cannot uniquely locate existing narrative anchor: " + fragment
          )
        return indices[0]

      for step in kernel_steps:
        item = step.conclusion
        expression = str(item.multiple) + _element(item.source_generator)
        formula = r"\ker E=\mathbb{Z}\{" + expression + r"\}"
        if formula not in rendered and r"\ker E" not in rendered:
          delta_index = unique_index(r"\operatorname{Im}\Delta")
          paragraphs.insert(
            delta_index + 1,
            "完全性より, $" + formula + "$."
          )
      for step in quotient_steps:
        item = step.conclusion
        formula = (
          _group(item.codomain) + r"\cong "
          + _group(item.domain) + r"/\mathbb{Z}\{"
          + str(item.multiple) + _element(item.source_generator) + r"\}"
        )
        if "準同型定理" not in "\n\n".join(paragraphs):
          surjective_index = unique_index("は全射")
          prior_group = _group(item.domain) + " = "
          group_indices = [
            i for i, paragraph in enumerate(paragraphs)
            if prior_group in paragraph and i > surjective_index
          ]
          if len(group_indices) != 1:
            raise ValueError("R2: cannot locate earlier group after surjectivity")
          paragraphs.insert(
            group_indices[0] + 1,
            "全射性と核の決定から, 準同型定理より $" + formula + "$."
          )
      rendered = "\n\n".join(paragraphs)
  # Hide only labels of typed finite-cyclic quotient deductions.
  # This occurs after the existing mathematical narrative is assembled,
  # so existing quotient paragraph/anchor calculations remain unchanged.
  if proof_root is not None:
    from phase165_r12_r2_quotient_rules import (
      CyclicStructureStatement,
      QuotientIsomorphismStatement,
    )
    from proof import ProofRule
    suppressed_inference_labels = {
      step.inference_rule.name
      for step in ancestry
      if step.rule is ProofRule.INFERENCE
      and step.inference_rule is not None
      and isinstance(step.conclusion, CyclicStructureStatement)
      and step.conclusion.order is not None
      and any(
        isinstance(premise.conclusion, QuotientIsomorphismStatement)
        for premise in step.premises
      )
    }
    if suppressed_inference_labels:
      rendered = "".join(
        line for line in rendered.splitlines(keepends=True)
        if line.strip() not in suppressed_inference_labels
      )
  return rendered
