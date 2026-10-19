from audit_phase144_6_r5_43_9 import (
  build_prose_design_inventory,
)


def test_phase144_6_r5_43_9_covers_all_sixteen_transport_chains():
  rows = build_prose_design_inventory()

  assert len(
    rows
  ) == 16


def test_phase144_6_r5_43_9_all_chains_observe_same_reference_identity():
  rows = build_prose_design_inventory()

  assert {
    row[
      "reference_identity"
    ]
    for row in rows
  } == {
    "Proposition 5.3",
  }


def test_phase144_6_r5_43_9_is_audit_only():
  import inspect
  import audit_phase144_6_r5_43_9 as module

  source = inspect.getsource(
    module
  )

  assert "write_text(" not in source
  assert "open(" not in source
