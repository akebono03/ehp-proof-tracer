from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
)


def render_toda_group_proof_narrative_reason_sentence(
  reason: TodaGroupProofNarrativeReason,
) -> str | None:
  if not isinstance(
    reason,
    TodaGroupProofNarrativeReason,
  ):
    raise TypeError(
      "reason must be a "
      "TodaGroupProofNarrativeReason"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  ):
    application = reason.reference_application

    if application is None or len(application.bindings) != 1:
      return (
        "この前提条件を満たすので、"
        "次の定義を用いる。"
      )

    binding = application.bindings[0]
    reference_label = application.reference.label
    formal_latex = render_toda_expression_latex(
      binding.formal_variable
    )
    instantiated_latex = render_toda_expression_latex(
      binding.instantiated_expression
    )

    return (
      "この前提条件を満たすので、"
      f"{reference_label} を適用できる。\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると、"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    if len(reason.premise_steps) != 2:
      return None

    exactness_statement = (
      reason.premise_steps[1].conclusion
    )
    window = exactness_statement.window
    first_map_name = window.first_map.name
    second_map_name = window.second_map.name

    return (
      "この完全性と "
      f"${first_map_name}=0$ より、"
      f"$\\ker {second_map_name}"
      f"=\\operatorname{{Im}}{first_map_name}=0$ "
      "である。\n"
      "したがって、"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .MULTIPLE_RELATION_TO_ORDER
  ):
    if len(reason.premise_steps) != 2:
      return None

    order_statement = reason.premise_steps[0].conclusion
    equality_statement = reason.premise_steps[1].conclusion
    ordered_latex = render_toda_expression_latex(order_statement.lhs)
    target_latex = render_toda_expression_latex(
      equality_statement.lhs.expression
    )

    return (
      f"$\\operatorname{{ord}}({ordered_latex})=2$ "
      f"かつ $2{target_latex}={ordered_latex}$ より、"
      f"$4{target_latex}=0$ かつ "
      f"$2{target_latex}\\neq0$ である。\n"
      "したがって、"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .FINAL_GROUP_STRUCTURE
  ):
    if len(reason.premise_steps) != 7:
      return None

    left_group_statement = reason.premise_steps[0].conclusion
    right_group_statement = reason.premise_steps[4].conclusion
    order_statement = reason.premise_steps[5].conclusion
    membership_statement = reason.premise_steps[6].conclusion

    left_order = left_group_statement.rhs.order
    right_order = right_group_statement.rhs.order
    middle_order = left_order * right_order
    generator_latex = render_toda_expression_latex(
      membership_statement.element
    )

    return (
      "この短完全列と両端の群の位数より、"
      f"中央の群の位数は ${left_order}\cdot"
      f"{right_order}={middle_order}$ である。\n"
      f"また、${generator_latex}$ は中央の群に属し、"
      f"$\operatorname{{ord}}({generator_latex})"
      f"={order_statement.rhs}={middle_order}$ であるから、"
      f"${generator_latex}$ は中央の群を生成する。\n"
      "したがって、"
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:
    return (
      "この完全性、既知の群構造、および写像の像に関する結果を合わせると、"
      "対象となる写像の像と核が決まる。\nしたがって、"
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:
    return (
      "この群構造と写像による移送の結果を合わせると、"
      "対象の群の位数と写像の単射性が決まる。\nしたがって、"
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return "以上で得た群構造、生成元、および写像に関する結果を合わせると、"

  return None


def _toda_group_proof_narrative_reason_insertion_index(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> int | None:
  conclusion_line = _render_generic_narrative_step(
    reason.conclusion_step
  )
  if conclusion_line:
    conclusion_index = markdown.find(conclusion_line)
    if conclusion_index >= 0:
      return conclusion_index

  children_by_step_id = {}
  for edge in reason_sidecar.presentation.edges:
    children_by_step_id.setdefault(
      id(edge.premise_step),
      [],
    ).append(edge.parent_step)

  queue = list(
    children_by_step_id.get(
      id(reason.conclusion_step),
      (),
    )
  )
  visited_step_ids = {
    id(reason.conclusion_step),
  }

  while queue:
    next_queue = []
    for proof_step in queue:
      proof_step_id = id(proof_step)
      if proof_step_id in visited_step_ids:
        continue
      visited_step_ids.add(proof_step_id)

      rendered_line = _render_generic_narrative_step(
        proof_step
      )
      if rendered_line:
        rendered_index = markdown.find(rendered_line)
        if rendered_index >= 0:
          return rendered_index

      next_queue.extend(
        children_by_step_id.get(
          proof_step_id,
          (),
        )
      )
    queue = next_queue

  return None


def insert_toda_group_proof_narrative_reason_prose(
  markdown: str,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")
  if not isinstance(
    reason_sidecar,
    TodaGroupProofNarrativeReasonSidecar,
  ):
    raise TypeError(
      "reason_sidecar must be a "
      "TodaGroupProofNarrativeReasonSidecar"
    )

  rendered = markdown
  emitted_final_result_sentences = set()

  for reason in reason_sidecar.reasons:
    sentence = render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    if sentence is None:
      continue

    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_RESULT_DERIVATION
    ):
      if sentence in emitted_final_result_sentences:
        continue

      emitted_final_result_sentences.add(
        sentence
      )

    insertion_index = (
      _toda_group_proof_narrative_reason_insertion_index(
        rendered,
        reason,
        reason_sidecar,
      )
    )
    if insertion_index is None:
      continue

    prefix = sentence + "\n\n"
    if rendered[
      max(0, insertion_index - len(prefix)):
      insertion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )

  return rendered

