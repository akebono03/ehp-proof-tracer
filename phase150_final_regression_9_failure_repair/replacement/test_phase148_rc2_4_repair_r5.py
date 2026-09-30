import pytest

from phase148_rc2_4_repair_r5_two_group_exposure_path_audit.audit_phase148_rc2_4_repair_r5 import (
  CASES,
  _build_case,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_repair_r5_audit_has_exactness_steps_to_trace(
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
    _rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  assert any(
    isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
    for node in closure.nodes
  )


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_repair_r5_generic_narrative_does_not_require_literal_exactness_phrase(
  label,
  n,
  k,
):
  (
    _presentation,
    _closure,
    _sidecar,
    _blocks,
    _arguments,
    rendered,
  ) = _build_case(
    label,
    n,
    k,
  )

  assert (
    rendered.count(
      "は完全である"
    )
    + rendered.count(
      r"\text{ is exact}"
    )
    == 0
  )
