from audit_phase144_6_r5_43_11b import (
  build_boundary_inventory,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
)


def test_phase144_6_r5_43_11b_reproduces_190_selected_and_13_insertable():
  rows = build_boundary_inventory()

  assert sum(
    row[
      5
    ]
    for row in rows
  ) == 190
  assert sum(
    row[
      6
    ]
    for row in rows
  ) == 13


def test_phase144_6_r5_43_11b_classifies_every_non_insertable_populated_argument_by_discourse_role():
  rows = build_boundary_inventory()
  non_insertable = tuple(
    row
    for row in rows
    if row[
      6
    ] < row[
      5
    ]
  )

  assert non_insertable
  assert all(
    row[
      4
    ]
    in {
      role.value
      for role in TodaGroupProofNarrativeArgumentDiscourseRole
    }
    for row in non_insertable
  )
