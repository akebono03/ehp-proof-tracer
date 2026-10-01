from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_statement_prose,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)


def _phase153_r2_pi10_6_toda45_case():
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=7,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  proof_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      Toda45IsomorphismStatement,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    proof_step,
  )


def test_phase153_r2_toda45_is_classified_as_map_property():
  (
    presentation,
    semantic_sidecar,
    proof_step,
  ) = _phase153_r2_pi10_6_toda45_case()

  role = recognize_toda_group_proof_narrative_step_role(
    presentation,
    proof_step,
    semantic_sidecar=semantic_sidecar,
  )

  assert (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
  )


def test_phase153_r2_toda45_uses_generic_isomorphism_rendering():
  (
    _presentation,
    _semantic_sidecar,
    proof_step,
  ) = _phase153_r2_pi10_6_toda45_case()

  rendered = (
    _render_generic_narrative_statement_prose(
      proof_step.conclusion
    )
  )

  assert rendered is not None
  assert rendered.startswith(
    "$E^{"
  )
  assert "は同型写像である." in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
