from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


PI4_3_CONCLUSION = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def _phase159_pi4_3_context():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    base,
    ordered_contributions,
  )


def test_phase159_pi4_3_conclusion_anchor_includes_standalone_connector():
  (
    _,
    _,
    blocks,
    arguments,
    base,
    ordered_contributions,
  ) = _phase159_pi4_3_context()

  indices = (
    _contribution_insertion_indices(
      base,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  connector_index = base.index(
    "以上より,"
  )
  before_conclusion_indices = tuple(
    indices[
      argument_index
    ][
      contribution_index
    ]
    for argument_index, contributions in enumerate(
      ordered_contributions
    )
    for contribution_index, contribution in enumerate(
      contributions
    )
    if (
      contribution.placement
      is TodaGroupProofNarrativeContributionPlacement
      .BEFORE_ARGUMENT_CONCLUSION
    )
  )

  assert before_conclusion_indices
  assert all(
    insertion_index == connector_index
    for insertion_index
    in before_conclusion_indices
  )


def test_phase159_pi4_3_contributions_keep_connector_with_root_conclusion():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    _,
    _,
  ) = _phase159_pi4_3_context()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert (
    "以上より, "
    + "$"
    + PI4_3_CONCLUSION
    + "$."
  ) in rendered


def test_phase159_pi4_3_public_proof_keeps_single_connected_final_conclusion():
  (
    presentation,
    _,
    _,
    _,
    _,
    _,
  ) = _phase159_pi4_3_context()

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_marker = "\n## 証明\n\n"

  assert proof_marker in rendered

  proof_body = rendered.split(
    proof_marker,
    1,
  )[1]

  assert proof_body.count(
    PI4_3_CONCLUSION
  ) == 1
  assert (
    "以上より, "
    + "$"
    + PI4_3_CONCLUSION
    + "$."
  ) in proof_body
  assert rendered.rstrip().endswith(
    "□"
  )
