from phase144_6_r25_27_proof_edge_ownership_boundary_audit.audit_phase144_6_r25_27 import (
  _closure_from_block,
)


def test_phase144_6_r25_27_r3_current_conclusion_cycle_is_not_reentered():
  dependencies = (
    (1, 3),
    (2,),
    (0,),
    (),
  )

  closure = _closure_from_block(
    dependencies,
    1,
    set(),
    excluded_indices=(
      0,
    ),
  )

  assert closure == frozenset(
    {
      1,
      2,
    }
  )
  assert 3 not in closure


def test_phase144_6_r25_27_r3_other_argument_boundary_still_stops():
  dependencies = (
    (),
    (0,),
    (1,),
  )

  closure = _closure_from_block(
    dependencies,
    2,
    {
      1,
    },
    excluded_indices=(),
  )

  assert closure == frozenset(
    {
      2,
    }
  )
