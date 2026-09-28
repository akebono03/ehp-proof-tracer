from collections import Counter

from audit_phase144_6_r5_43_6 import (
  build_hidden_bridge_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)


def main():
  audit_rows = (
    build_hidden_bridge_inventory()
  )
  signatures = {}

  for n, k in TARGETS:
    presentation = _context(
      n,
      k,
    )[0]

    for semantic in (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    ):
      rule = (
        semantic.proof_step.inference_rule
      )
      key = (
        type(
          semantic.proof_step.conclusion
        ).__name__,
        (
          None
          if rule is None
          else rule.name
        ),
      )
      signatures[
        key
      ] = semantic.role.value

  reproduced = Counter()

  for row in audit_rows:
    key = (
      row[
        "statement_type"
      ],
      row[
        "rule_name"
      ],
    )
    reproduced[
      signatures[
        key
      ]
    ] += 1

  print("=" * 78)
  print(
    "Phase 144-6-R5-43-7 hidden bridge semantic "
    "classification foundation audit"
  )
  print("=" * 78)
  print(
    f"R5-43-6 occurrences={len(audit_rows)}"
  )
  print(
    "production semantic roles:"
  )

  for role, count in sorted(
    reproduced.items()
  ):
    print(
      f"  {role}: {count}"
    )

  print(
    "renderer changes: none"
  )
  print(
    "public route changes: none"
  )


if __name__ == "__main__":
  main()
