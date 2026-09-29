import re

from phase144_6_r25_23_evidence_selection_dependency_order_audit.audit_phase144_6_r25_23 import (
  _data,
  _forward_references,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)


def test_phase144_6_r25_23_pi6_complete_replay_exposes_exactness_evidence_population():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
    _,
  ) = _data(
    3,
    3,
  )

  group_argument_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    )
  )

  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      group_argument_index,
    )
  )
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      group_argument_index,
    )
  )

  assert local_body
  assert evidence
  assert all(
    block in local_body
    for block in evidence
  )


def test_phase144_6_r25_23_pi6_reports_actual_forward_reference_population():
  (
    _,
    _,
    _,
    _,
    markdown,
  ) = _data(
    3,
    3,
  )

  forward = (
    _forward_references(
      markdown
    )
  )

  assert isinstance(
    forward,
    tuple,
  )
  assert all(
    isinstance(
      reference,
      int,
    )
    and reference > 0
    for _, reference, _ in forward
  )


def test_phase144_6_r25_23_pi6_generic_narrative_contains_numbered_equations():
  (
    _,
    _,
    _,
    _,
    markdown,
  ) = _data(
    3,
    3,
  )

  assert re.search(
    r"\\tag\{1\}",
    markdown,
  )
  assert "(1) と (2) より、" in markdown
