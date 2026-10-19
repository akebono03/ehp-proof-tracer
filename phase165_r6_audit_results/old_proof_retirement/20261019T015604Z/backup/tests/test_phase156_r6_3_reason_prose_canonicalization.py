import inspect

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


def _pi6_reason_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .MULTIPLE_RELATION_TO_ORDER
    )
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason,
  )


def test_phase156_r6_3_reason_sentence_uses_canonical_eta_cube():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason,
  ) = _pi6_reason_data()

  sentence = render_toda_group_proof_narrative_reason_sentence(
    reason
  )

  assert sentence is not None
  assert (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$"
    in sentence
  )
  assert (
    r"$2\nu'=\eta_{3}^{3}$"
    in sentence
  )
  assert (
    r"\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})"
    not in sentence
  )
  assert (
    r"2\nu'=\eta_{3}\eta_{4}\eta_{5}"
    not in sentence
  )


def test_phase156_r6_3_public_reason_prose_matches_canonical_equation3():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason,
  ) = _pi6_reason_data()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  equation_three = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  canonical_reason = (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$ "
    r"かつ $2\nu'=\eta_{3}^{3}$ より, "
  )

  assert equation_three in rendered
  assert canonical_reason in rendered
  assert (
    rendered.index(
      equation_three
    )
    < rendered.index(
      canonical_reason
    )
  )


def test_phase156_r6_3_reason_renderer_has_no_pi6_specific_branch():
  import toda_group_proof_narrative_reason_renderer as module

  source = inspect.getsource(
    module
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
