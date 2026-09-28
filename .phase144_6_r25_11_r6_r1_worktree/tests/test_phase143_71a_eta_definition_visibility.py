from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
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


def test_phase143_71a_pi7_3_group_narrative_hides_raw_eta_definition():
  rendered = _render(
    3,
    4,
  )

  assert (
    "TodaEtaFamilyDefinitionStatement"
    not in rendered
  )


def test_phase143_71a_pi9_4_group_narrative_hides_raw_eta_definition():
  rendered = _render(
    4,
    5,
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
