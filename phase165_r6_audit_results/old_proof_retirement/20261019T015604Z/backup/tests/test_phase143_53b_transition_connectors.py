from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase143_53b_pi6_3_support_definition_has_no_connector():
  rendered = _render(
    3,
    3,
  )

  assert (
    "以上より、\n\n"
    r"$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
    not in rendered
  )


