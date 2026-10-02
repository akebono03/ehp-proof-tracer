from collections import Counter

from audit_phase144_6_r5_43_6 import (
  build_hidden_bridge_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_43_6_inventory_covers_only_representative_groups():
  rows = build_hidden_bridge_inventory()

  assert {
    (
      row[
        "n"
      ],
      row[
        "k"
      ],
    )
    for row in rows
  }.issubset(
    set(
      TARGETS
    )
  )


def test_phase144_6_r5_43_6_hidden_bridge_rows_have_classification_inputs():
  rows = build_hidden_bridge_inventory()

  assert rows
  assert all(
    row[
      "statement_type"
    ]
    for row in rows
  )
  assert all(
    row[
      "rule_name"
    ] is None
    or isinstance(
      row[
        "rule_name"
      ],
      str,
    )
    for row in rows
  )
  assert all(
    row[
      "classification"
    ] in {
      "transport_candidate",
      "mathematical_relation_candidate",
      "integration_provenance_candidate",
      "structured_mathematical_candidate",
    }
    for row in rows
  )


def test_phase144_6_r5_43_6_is_audit_only():
  import inspect
  import audit_phase144_6_r5_43_6 as module

  source = inspect.getsource(
    module
  )

  assert "write_text(" not in source
  assert "open(" not in source
