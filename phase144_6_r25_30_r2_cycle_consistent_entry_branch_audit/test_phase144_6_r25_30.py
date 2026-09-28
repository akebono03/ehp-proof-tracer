import pytest

from phase144_6_r25_30_r2_cycle_consistent_entry_branch_audit.audit_phase144_6_r25_30 import (
  LARGE_BRANCH_BLOCK_THRESHOLD,
  TARGETS,
  _argument_rows,
)


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r2_audits_only_group_structure_and_definition(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _argument_rows(
    n,
    k,
  )

  assert rows
  assert all(
    row[
      "role"
    ]
    in (
      "establish_group_structure",
      "establish_definition",
    )
    for row in rows
  )


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r2_child_step_closure_is_subset_of_entry_step_closure(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _argument_rows(
    n,
    k,
  )

  for row in rows:
    for entry in row[
      "entries"
    ]:
      for child in entry[
        "children"
      ]:
        assert (
          child[
            "step_indices"
          ]
          <= entry[
            "step_indices"
          ]
        )


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_30_r2_child_block_projection_is_subset_of_entry_projection(
  n,
  k,
):
  (
    presentation,
    blocks,
    arguments,
    rows,
  ) = _argument_rows(
    n,
    k,
  )

  for row in rows:
    for entry in row[
      "entries"
    ]:
      for child in entry[
        "children"
      ]:
        assert (
          child[
            "block_indices"
          ]
          <= entry[
            "block_indices"
          ]
        )


def test_phase144_6_r25_30_r2_reproduces_remaining_giant_entry_branches():
  for n, k in (
    (8, 7),
    (9, 7),
  ):
    (
      presentation,
      blocks,
      arguments,
      rows,
    ) = _argument_rows(
      n,
      k,
    )

    assert any(
      entry[
        "blocks"
      ]
      >= LARGE_BRANCH_BLOCK_THRESHOLD
      for row in rows
      for entry in row[
        "entries"
      ]
    )
