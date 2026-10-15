from toda_rules import (
  TodaProp42ExactnessStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _normalized_exactness_rendering(
  step,
):
  rendered = (
    _render_generic_narrative_step(
      step
    )
  )
  suffix = r" \text{ is exact}$"

  if rendered.endswith(
    suffix
  ):
    return (
      rendered[
        :-len(
          suffix
        )
      ]
      + "$ は完全である."
    )

  return rendered


def test_phase148_rc2_4_repair_r1_audit_detects_visible_exactness_paths():
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      3,
      3,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  exactness_steps = tuple(
    (
      block,
      step,
    )
    for block in blocks
    for step in block.steps
    if isinstance(
      step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  assert exactness_steps

  visible = tuple(
    (
      block,
      step,
    )
    for block, step in exactness_steps
    if (
      _normalized_exactness_rendering(
        step
      )
      in rendered
    )
  )

  assert visible


def test_phase148_rc2_4_repair_r1_audit_records_exactness_role_distribution():
  _presentation, blocks, _sidecar, _arguments = (
    _method_evidence_data(
      3,
      3,
    )
  )

  exactness_roles = tuple(
    block.role
    for block in blocks
    for step in block.steps
    if isinstance(
      step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  assert exactness_roles
  assert all(
    isinstance(
      role,
      TodaGroupProofNarrativeMathematicalBlockRole,
    )
    for role in exactness_roles
  )
