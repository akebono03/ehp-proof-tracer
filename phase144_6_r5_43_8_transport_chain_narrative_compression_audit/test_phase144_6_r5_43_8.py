from collections import Counter

from audit_phase144_6_r5_43_8 import (
  build_transport_chain_inventory,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
)


def test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains():
  rows = build_transport_chain_inventory()

  assert len(
    rows
  ) == 16
  assert all(
    len(
      row[
        "hidden"
      ]
    ) == 3
    for row in rows
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


def test_phase144_6_r5_43_8_has_one_hidden_signature_sequence():
  rows = build_transport_chain_inventory()
  counts = Counter(
    row[
      "hidden_signatures"
    ]
    for row in rows
  )

  assert len(
    counts
  ) == 1
  assert next(
    iter(
      counts.values()
    )
  ) == 16


def test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences():
  rows = build_transport_chain_inventory()

  assert sum(
    len(
      row[
        "hidden"
      ]
    )
    for row in rows
  ) == 48


def test_phase144_6_r5_43_8_is_audit_only():
  import inspect
  import audit_phase144_6_r5_43_8 as module

  source = inspect.getsource(
    module
  )

  assert "write_text(" not in source
  assert "open(" not in source
