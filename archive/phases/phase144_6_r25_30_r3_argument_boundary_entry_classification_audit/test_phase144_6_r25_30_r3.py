import pytest

from phase144_6_r25_30_r3_argument_boundary_entry_classification_audit.audit_phase144_6_r25_30_r3 import (
  TARGETS,
  _audit_target,
)


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r3_boundary_entries_have_one_or_more_other_argument_owners(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _audit_target(
    n,
    k,
  )

  for row in rows:
    for entry in row[
      "entries"
    ]:
      if entry[
        "classification"
      ] != "argument_boundary":
        continue

      assert entry[
        "owner_arguments"
      ]
      assert all(
        owner
        != row[
          "argument_index"
        ]
        for owner in entry[
          "owner_arguments"
        ]
      )
      assert entry[
        "steps"
      ] == 0
      assert entry[
        "blocks"
      ] == 0


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r3_owned_entries_have_no_argument_owner(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _audit_target(
    n,
    k,
  )

  for row in rows:
    for entry in row[
      "entries"
    ]:
      if entry[
        "classification"
      ] != "owned":
        continue

      assert entry[
        "owner_arguments"
      ] == ()
      assert entry[
        "owner_roles"
      ] == ()
      assert entry[
        "steps"
      ] >= 1
      assert entry[
        "blocks"
      ] >= 1


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r3_step_boundary_pairs_match_declared_child_arguments(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _audit_target(
    n,
    k,
  )

  declared_pairs = {
    (
      row[
        "argument_index"
      ],
      child_argument_index,
    )
    for row in rows
    for child_argument_index in row[
      "declared_child_arguments"
    ]
  }
  classified_pairs = {
    (
      row[
        "argument_index"
      ],
      owner,
    )
    for row in rows
    for entry in row[
      "entries"
    ]
    if entry[
      "classification"
    ] == "argument_boundary"
    for owner in entry[
      "owner_arguments"
    ]
  }

  assert classified_pairs == declared_pairs


def test_phase144_6_r25_30_r3_reproduces_at_least_one_boundary_entry():
  boundary_count = 0

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      arguments,
      rows,
    ) = _audit_target(
      n,
      k,
    )

    boundary_count += sum(
      entry[
        "classification"
      ] == "argument_boundary"
      for row in rows
      for entry in row[
        "entries"
      ]
    )

  assert boundary_count > 0
