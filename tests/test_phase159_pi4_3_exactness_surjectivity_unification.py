import inspect

from homotopy_groups import (
  TodaPrimaryGroupZeroStatement,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
)


def _pi4_3_surjectivity_reason_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  )


def test_phase159_pi4_3_builds_exactness_to_surjectivity_reason():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_surjectivity_reason_data()

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and isinstance(
        reason.conclusion_step.conclusion,
        TodaSuspensionSurjectiveStatement,
      )
    )
  )

  assert len(reasons) == 1
  reason = reasons[0]

  assert len(reason.premise_steps) == 2
  assert isinstance(
    reason.premise_steps[0].conclusion,
    TodaPrimaryGroupZeroStatement,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaProp42ExactnessStatement,
  )

  zero_group = (
    reason.premise_steps[0].conclusion.group
  )
  window = (
    reason.premise_steps[1].conclusion.window
  )
  surjective_map = (
    reason.conclusion_step.conclusion.map
  )

  assert (
    window.source_term
    == surjective_map.source_group
  )
  assert (
    window.middle_term
    == surjective_map.target_group
  )
  assert zero_group == window.target_term
  assert window.first_map.name == "E"
  assert window.second_map.name == "H"


def test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_surjectivity_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and isinstance(
        reason.conclusion_step.conclusion,
        TodaSuspensionSurjectiveStatement,
      )
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence == (
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )
  assert rendered.count(
    sentence
  ) == 1
  assert rendered.count(
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  ) == 1
  assert (
    "この完全性と "
    not in rendered
  )
  assert (
    "これより, 完全性より,"
    not in rendered
  )


def test_phase159_exactness_to_map_property_builder_has_no_pi4_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._exactness_to_map_property_reason
  )

  forbidden_fragments = (
    "(4, 3)",
    "pi4",
    "eta_2",
    "η₂",
    "Proposition 5.1",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
