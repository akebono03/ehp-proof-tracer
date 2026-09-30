import pytest

from phase148_rc2_4_repair_r5_two_group_exposure_path_audit.audit_phase148_rc2_4_repair_r5 import (
  CASES,
  _build_case,
  _normalized_exactness_rendering,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_repair_r5_r2_raw_exactness_proof_steps_are_hidden(
  label,
  n,
  k,
):
  (
    _presentation,
    closure,
    _sidecar,
    _blocks,
    _arguments,
    rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  exactness_steps = tuple(
    node.proof_step
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  assert exactness_steps

  for proof_step in exactness_steps:
    assert (
      _normalized_exactness_rendering(
        proof_step
      )
      not in rendered
    )


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_repair_r5_r2_generic_narrative_has_no_literal_exactness_phrase(
  label,
  n,
  k,
):
  (
    _presentation,
    closure,
    _sidecar,
    _blocks,
    _arguments,
    rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  normalized_windows = tuple(
    _normalized_exactness_rendering(
      node.proof_step
    )
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  phrase_lines = tuple(
    line
    for line in rendered.splitlines()
    if (
      "は完全である" in line
      or r"\text{ is exact}" in line
    )
  )

  assert normalized_windows
  assert phrase_lines == ()
