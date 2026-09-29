from proof import (
  ProofStep,
)
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_catalog import (
  DEFINITION_STATEMENT_TYPES,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
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

  return render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def test_phase143_71a_eta_definition_catalog_is_unchanged():
  assert (
    TodaEtaFamilyDefinitionStatement
    not in DEFINITION_STATEMENT_TYPES
  )


def test_phase143_71a_cross_validation_group_narratives_hide_raw_eta_definition():
  for n, k in (
    (3, 4),
    (4, 5),
  ):
    rendered = _render(
      n,
      k,
    )

    assert (
      "TodaEtaFamilyDefinitionStatement"
      not in rendered
    )


def test_phase143_71a_existing_definition_arguments_remain_available():
  (
    _,
    _,
    _,
    arguments,
  ) = _method_evidence_data(
    5,
    3,
  )

  assert any(
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
    for argument in arguments
  )


def test_phase143_71a_body_renderer_can_hide_only_selected_steps():
  (
    presentation,
    blocks,
    _,
    _,
  ) = _method_evidence_data(
    3,
    4,
  )

  eta_step = next(
    proof_step
    for block in blocks
    for proof_step in block.steps
    if isinstance(
      proof_step.conclusion,
      TodaEtaFamilyDefinitionStatement,
    )
  )
  eta_block = next(
    block
    for block in blocks
    if eta_step in block.steps
  )

  rendered = render_toda_group_proof_narrative_argument_body_markdown(
    presentation,
    blocks,
    (
      eta_block,
    ),
    None,
    context_hidden_step_ids=frozenset(
      (
        id(
          eta_step
        ),
      )
    ),
  )

  assert rendered == ""
