from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = (
  r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
)


def _repair47_data():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  return (
    raw,
    presentation,
    reason_sidecar,
  )


def test_phase157_r20_repair47_eta_order_gets_generic_injective_image_reason():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  target_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      _render_generic_narrative_step(
        node.proof_step
      )
      == TARGET
    )
  )

  assert len(
    target_steps
  ) == 1

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.conclusion_step
      is target_steps[
        0
      ]
    )
  )

  matching = tuple(
    reason
    for reason in reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .INJECTIVE_IMAGE_ORDER
    )
  )

  assert len(
    matching
  ) == 1
  assert len(
    matching[
      0
    ].premise_steps
  ) == 2


def test_phase157_r20_repair47_reason_sentence_exposes_nonzero_suspension_image():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .INJECTIVE_IMAGE_ORDER
    )
  )

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )

  assert sentence is not None
  assert (
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$"
    in sentence
  )
  assert (
    "単射写像は元の位数を保つ."
    in sentence
  )


def test_phase157_r20_repair47_public_narrative_places_reason_before_eta_order():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  reason_tail = (
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
  order_text = (
    r"$\operatorname{ord}"
    r"\left(\eta_{3}^{3}\right) = 2$."
  )

  assert "この群構造と" not in body
  assert reason_tail in body
  assert order_text in body
  assert body.index(
    reason_tail
  ) < body.index(
    order_text
  )


def test_phase157_r20_repair47_existing_nu_prime_order_reason_remains():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  assert (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$ "
    r"かつ $2\nu'=\eta_{3}^{3}$ より, "
    r"$4\nu'=0$ かつ $2\nu'\neq0$."
    in body
  )
