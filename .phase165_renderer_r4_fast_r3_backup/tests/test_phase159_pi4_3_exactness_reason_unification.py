import inspect

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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
  TodaDeltaImageFreeCyclicStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


def _pi4_3_reason_data():
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


def test_phase159_pi4_3_builds_generic_exactness_to_kernel_reason():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
    )
  )

  assert len(reasons) == 1
  reason = reasons[0]

  assert isinstance(
    reason.conclusion_step.conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )
  assert len(reason.premise_steps) == 2
  assert isinstance(
    reason.premise_steps[0].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaProp42ExactnessStatement,
  )

  image_statement = (
    reason.premise_steps[0].conclusion
  )
  window = (
    reason.premise_steps[1]
    .conclusion
    .window
  )
  kernel_statement = (
    reason.conclusion_step.conclusion
  )

  assert (
    image_statement.map.source_group
    == window.source_term
  )
  assert (
    image_statement.map.target_group
    == window.middle_term
  )
  assert (
    window.middle_term
    == kernel_statement.map.source_group
  )
  assert (
    window.target_term
    == kernel_statement.map.target_group
  )
  assert (
    image_statement.image_group
    == kernel_statement.kernel_group
  )
  assert window.first_map.name == "Δ"
  assert window.second_map.name == "E"


def test_phase159_pi4_3_exactness_reason_is_visible_before_kernel_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  kernel_conclusion = (
    _render_generic_narrative_step(
      reason.conclusion_step
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

  assert sentence is not None
  assert sentence.startswith(
    "完全性より, "
  )
  assert (
    r"$\ker E=\operatorname{Im}Δ="
    in sentence
  )
  assert rendered.count(sentence) == 1

  assert kernel_conclusion
  assert kernel_conclusion not in rendered


def test_phase159_exactness_to_kernel_builder_has_no_pi4_or_rule_name_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._exactness_to_kernel_reason
  )

  forbidden_fragments = (
    "(4, 3)",
    "pi4",
    "eta_2",
    "η₂",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source

def test_phase159_pi4_3_exactness_reason_matches_existing_exactness_prose_style():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
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
  image_line = (
    _render_generic_narrative_step(
      reason.premise_steps[0]
    )
  )
  kernel_line = (
    _render_generic_narrative_step(
      reason.conclusion_step
    )
  )

  assert sentence is not None
  assert sentence.startswith(
    "完全性より, "
  )
  assert " である." not in sentence
  assert (
    "これより, 完全性より,"
    not in rendered
  )
  assert rendered.count(
    sentence
  ) == 1
  assert rendered.count(
    image_line
  ) == 1
  assert kernel_line not in rendered

