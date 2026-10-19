import pytest

from phase149_rc3_4_cross_group_ordering_audit.audit_phase149_rc3_4 import (
  CASES,
  _argument_record,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


@pytest.mark.parametrize(
  "_label,n,k",
  CASES,
)
def test_phase149_rc3_4_owned_primary_exactness_precedes_owner_conclusion(
  _label,
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

  records = tuple(
    _argument_record(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    for argument_index in range(
      len(
        arguments
      )
    )
  )

  assert all(
    record[
      "ordering_ok"
    ]
    for record in records
  )


def test_phase149_rc3_4_pi6_3_has_owned_primary_exactness_before_conclusion():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  records = tuple(
    _argument_record(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    for argument_index in range(
      len(
        arguments
      )
    )
  )
  owned_records = tuple(
    record
    for record in records
    if record[
      "owned_primary_latex"
    ]
  )

  assert owned_records
  assert all(
    record[
      "ordering_ok"
    ]
    for record in owned_records
  )
