from expression import (
  Expression,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
  render_toda_target_latex,
)
from toda_presentation import (
  build_toda_target_presentation,
)


def _render_toda_group_proof_narrative_argument_purpose_subject_latex(
  subject,
) -> str:
  if isinstance(
    subject,
    Expression,
  ):
    return render_toda_expression_latex(
      subject
    )

  if isinstance(
    subject,
    TodaPrimaryGroup,
  ):
    return render_toda_target_latex(
      build_toda_target_presentation(
        subject
      )
    )

  raise TypeError(
    "unsupported NarrativeArgument purpose subject"
  )


def render_toda_group_proof_narrative_argument_purpose_sentence(
  argument: TodaGroupProofNarrativeArgument,
) -> str | None:
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )

  if subject is None:
    return None

  subject_latex = (
    _render_toda_group_proof_narrative_argument_purpose_subject_latex(
      subject
    )
  )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    return (
      f"${subject_latex}$ を定める."
    )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  ):
    return (
      f"${subject_latex}$ の位数を決定する."
    )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE
  ):
    return (
      f"${subject_latex}$ の群構造を決定する."
    )

  return None
