from toda_end_to_end_presentation import (
  TodaEndToEndCandidatePresentation,
)
from toda_human_readable_renderer import (
  render_toda_end_to_end_markdown,
)
from toda_proof_narrative_renderer import (
  render_toda_readable_proof_narrative_markdown,
)


def render_toda_full_proof_report_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaEndToEndCandidatePresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    )

  base_report = (
    render_toda_end_to_end_markdown(
      presentation
    )
  ).rstrip()

  narrative = (
    render_toda_readable_proof_narrative_markdown(
      presentation
    )
  ).rstrip()

  return (
    base_report
    + "\n\n"
    + narrative
    + "\n"
  )
