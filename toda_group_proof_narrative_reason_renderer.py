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
        "次の定義を用いる."
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
      f"{reference_label} を適用できる.\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると、"
    )

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

  for reason in reason_sidecar.reasons:
    sentence = render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    if sentence is None:
      continue

    conclusion_line = _render_generic_narrative_step(
      reason.conclusion_step
    )
    if not conclusion_line:
      continue

    conclusion_index = rendered.find(conclusion_line)
    if conclusion_index < 0:
      continue

    prefix = sentence + "\n\n"
    if rendered[
      max(0, conclusion_index - len(prefix)):
      conclusion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:conclusion_index]
      + prefix
      + rendered[conclusion_index:]
    )

  return rendered
