from phase144_6_r25_27_proof_edge_ownership_boundary_audit.audit_phase144_6_r25_27 import (
  _closure_from_block,
)


def test_phase144_6_r25_27_r2_starting_boundary_is_not_owned():
  dependencies = (
    (),
    (0,),
    (1,),
  )

  assert _closure_from_block(
    dependencies,
    1,
    {1},
  ) == frozenset()


def test_phase144_6_r25_27_r2_descendant_boundary_is_not_owned():
  dependencies = (
    (),
    (0,),
    (1,),
  )

  assert _closure_from_block(
    dependencies,
    2,
    {1},
  ) == frozenset(
    {
      2,
    }
  )
