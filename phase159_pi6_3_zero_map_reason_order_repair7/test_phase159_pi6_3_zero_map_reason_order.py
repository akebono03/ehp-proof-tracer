from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


CONTRIBUTION_ZERO_MAP = (
  r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ "
  "は零写像である."
)
PUBLIC_ZERO_MAP = (
  r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ "
  "は零写像."
)
CONCISE_INJECTIVITY_REASON = (
  "完全性より, "
  r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ "
  "は単射."
)


def _phase159_pi6_3_context():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )


def test_phase159_pi6_3_zero_map_precedes_concise_injectivity_reason_in_contribution_renderer():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _phase159_pi6_3_context()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert CONTRIBUTION_ZERO_MAP in rendered
  assert CONCISE_INJECTIVITY_REASON in rendered
  assert rendered.index(
    CONTRIBUTION_ZERO_MAP
  ) < rendered.index(
    CONCISE_INJECTIVITY_REASON
  )


def test_phase159_pi6_3_zero_map_precedes_concise_injectivity_reason_in_public_renderer():
  (
    presentation,
    _,
    _,
    _,
  ) = _phase159_pi6_3_context()

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  assert PUBLIC_ZERO_MAP in body
  assert CONCISE_INJECTIVITY_REASON in body
  assert body.index(
    PUBLIC_ZERO_MAP
  ) < body.index(
    CONCISE_INJECTIVITY_REASON
  )
