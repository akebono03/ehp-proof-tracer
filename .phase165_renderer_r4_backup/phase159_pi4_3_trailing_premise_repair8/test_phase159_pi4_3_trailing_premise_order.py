from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  _provider_anchor_index,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


PI3_2_PREMISE = (
  r"$\pi_{3}^{2} = "
  r"\mathbb{Z}\{\eta_{2}\}$"
)
PI4_3_CONCLUSION = (
  r"$\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}$"
)


def _phase159_pi4_3_contribution_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )
  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )
  indices = (
    _contribution_insertion_indices(
      base,
      blocks,
      arguments,
      ordered,
    )
  )

  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    base,
    ordered,
    indices,
  )


def test_phase159_pi4_3_provider_anchor_contribution_does_not_cross_argument_conclusion():
  (
    _,
    blocks,
    _,
    _,
    base,
    ordered,
    indices,
  ) = _phase159_pi4_3_contribution_data()

  target = next(
    (
      argument_index,
      contribution_index,
      contribution,
    )
    for argument_index, contributions in enumerate(
      ordered
    )
    for contribution_index, contribution in enumerate(
      contributions
    )
    if PI3_2_PREMISE
    in _render_generic_narrative_step(
      contribution.proof_step
    )
  )
  (
    argument_index,
    contribution_index,
    contribution,
  ) = target

  assert (
    contribution.placement
    is TodaGroupProofNarrativeContributionPlacement
    .AT_PROVIDER_ANCHOR
  )

  provider_anchor_index = (
    _provider_anchor_index(
      base,
      blocks,
      contribution.provider_keys,
    )
  )
  conclusion_index = base.index(
    PI4_3_CONCLUSION
  )
  insertion_index = indices[
    argument_index
  ][
    contribution_index
  ]

  assert provider_anchor_index is not None
  assert provider_anchor_index > conclusion_index
  assert insertion_index <= conclusion_index


def test_phase159_pi4_3_contribution_renderer_places_pi3_2_before_final_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    _,
    _,
    _,
  ) = _phase159_pi4_3_contribution_data()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert PI3_2_PREMISE in rendered
  assert PI4_3_CONCLUSION in rendered
  assert rendered.index(
    PI3_2_PREMISE
  ) < rendered.index(
    PI4_3_CONCLUSION
  )


def test_phase159_pi4_3_public_narrative_has_no_trailing_pi3_2_premise_after_conclusion():
  (
    presentation,
    _,
    _,
    _,
    _,
    _,
    _,
  ) = _phase159_pi4_3_contribution_data()

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  premise = (
    "[R2]より, "
    + PI3_2_PREMISE
    + "."
  )
  final_conclusion = (
    "以上より, "
    + PI4_3_CONCLUSION
    + "."
  )

  assert premise in body
  assert final_conclusion in body
  assert body.index(
    premise
  ) < body.index(
    final_conclusion
  )
  assert body.rstrip().endswith(
    "□"
  )
