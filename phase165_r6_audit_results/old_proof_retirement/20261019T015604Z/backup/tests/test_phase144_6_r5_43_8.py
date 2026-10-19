from collections import Counter

from audit_phase144_6_r5_43_8 import (
  build_transport_chain_inventory,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
)


def test_phase144_6_r5_43_8_every_hidden_step_uses_production_transport_role():
  rows = build_transport_chain_inventory()

  assert all(
    role
    is TodaGroupProofNarrativeHiddenBridgeSemanticRole.TRANSPORT
    for row in rows
    for role in row[
      "hidden_roles"
    ]
  )


def test_phase144_6_r5_43_8_is_audit_only():
  import inspect
  import audit_phase144_6_r5_43_8 as module

  source = inspect.getsource(
    module
  )

  assert "write_text(" not in source
  assert "open(" not in source
