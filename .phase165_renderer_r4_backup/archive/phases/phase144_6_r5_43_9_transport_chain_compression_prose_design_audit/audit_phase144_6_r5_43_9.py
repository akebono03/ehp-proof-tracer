from collections import Counter

from audit_phase144_6_r5_43_8 import (
  build_transport_chain_inventory,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)


_CANDIDATES = (
  (
    "A_role_only",
    "このtransportにより、",
    frozenset(
      {
        "semantic_role",
      }
    ),
  ),
  (
    "B_named_result",
    "Proposition 5.3 により、",
    frozenset(
      {
        "semantic_role",
        "reference_identity",
      }
    ),
  ),
  (
    "C_named_result_and_operation",
    (
      "Proposition 5.3 を順次適用し、"
      "suspension による安定化を用いると、"
    ),
    frozenset(
      {
        "semantic_role",
        "reference_identity",
        "operation_kind",
      }
    ),
  ),
)


def _rule_name(
  proof_step,
):
  rule = proof_step.inference_rule

  if rule is None:
    return None

  return rule.name


def _reference_identity(
  row,
):
  rule_names = tuple(
    _rule_name(
      proof_step
    )
    for proof_step in row[
      "hidden"
    ]
  )

  if all(
    rule_name is not None
    and "Proposition 5.3" in rule_name
    for rule_name in rule_names
  ):
    return "Proposition 5.3"

  return None


def _operation_kind(
  row,
):
  rendered = row[
    "hidden_rendered"
  ]

  if (
    len(
      rendered
    ) == 3
    and "E^{n - 4}" in rendered[
      2
    ]
  ):
    return "suspension_stabilization"

  return None


def build_prose_design_inventory():
  rows = []

  for chain_index, row in enumerate(
    build_transport_chain_inventory(),
    start=1,
  ):
    reference_identity = (
      _reference_identity(
        row
      )
    )
    operation_kind = (
      _operation_kind(
        row
      )
    )
    available_metadata = {
      "semantic_role",
    }

    if reference_identity is not None:
      available_metadata.add(
        "reference_identity"
      )

    if operation_kind is not None:
      available_metadata.add(
        "operation_kind"
      )

    rows.append(
      {
        "chain_index": chain_index,
        "n": row[
          "n"
        ],
        "k": row[
          "k"
        ],
        "argument_index": row[
          "argument_index"
        ],
        "source": row[
          "source"
        ],
        "target": row[
          "target"
        ],
        "hidden": row[
          "hidden"
        ],
        "reference_identity": reference_identity,
        "operation_kind": operation_kind,
        "available_metadata": frozenset(
          available_metadata
        ),
        "candidates": tuple(
          {
            "key": key,
            "prose": prose,
            "required_metadata": required_metadata,
            "supported": (
              required_metadata
              <= available_metadata
            ),
          }
          for (
            key,
            prose,
            required_metadata,
          ) in _CANDIDATES
        ),
      }
    )

  return tuple(
    rows
  )


def main():
  rows = build_prose_design_inventory()

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-9 transport chain "
    "compression prose design audit"
  )
  print("production changes: none")
  print("=" * 78)
  print()

  print("A. Population")
  print("-" * 78)
  print(
    f"transport chains={len(rows)}"
  )
  print()

  print("B. Metadata observed in the 16 chains")
  print("-" * 78)
  reference_counts = Counter(
    row[
      "reference_identity"
    ]
    for row in rows
  )
  operation_counts = Counter(
    row[
      "operation_kind"
    ]
    for row in rows
  )

  for value, count in sorted(
    reference_counts.items(),
    key=lambda item: str(
      item[
        0
      ]
    ),
  ):
    print(
      f"reference_identity={value!r}: {count}"
    )

  for value, count in sorted(
    operation_counts.items(),
    key=lambda item: str(
      item[
        0
      ]
    ),
  ):
    print(
      f"operation_kind={value!r}: {count}"
    )
  print()

  print("C. Candidate prose support")
  print("-" * 78)
  for (
    key,
    prose,
    required_metadata,
  ) in _CANDIDATES:
    supported_count = sum(
      1
      for row in rows
      if next(
        candidate
        for candidate in row[
          "candidates"
        ]
        if candidate[
          "key"
        ] == key
      )[
        "supported"
      ]
    )
    print(
      f"{key}: supported={supported_count}/{len(rows)}"
    )
    print(
      f"  prose: {prose}"
    )
    print(
      "  requires: "
      + ", ".join(
        sorted(
          required_metadata
        )
      )
    )
  print()

  print("D. Per-chain preview")
  print("-" * 78)
  for row in rows:
    source = _render_generic_narrative_step(
      row[
        "source"
      ]
    )
    target = _render_generic_narrative_step(
      row[
        "target"
      ]
    )
    detailed = next(
      candidate
      for candidate in row[
        "candidates"
      ]
      if candidate[
        "key"
      ] == "C_named_result_and_operation"
    )

    print(
      f"Chain {row['chain_index']}: "
      f"pi_{row['n'] + row['k']}^{row['n']} "
      f"arg={row['argument_index']}"
    )
    print(
      f"  {source}"
    )
    print(
      f"  {detailed['prose']}"
    )
    print(
      f"  {target}"
    )
  print()

  print("E. Production-design boundary")
  print("-" * 78)
  print(
    "semantic_role alone supports only a generic "
    "transport description."
  )
  print(
    "Reference naming requires explicit "
    "reference_identity metadata."
  )
  print(
    "Mentioning suspension stabilization requires "
    "explicit operation_kind metadata."
  )
  print(
    "R5-43-9 does not add either metadata field "
    "to production."
  )
  print(
    "No renderer prose is changed in R5-43-9."
  )


if __name__ == "__main__":
  main()
