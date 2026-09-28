import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_qualified_execution_family import (
  RepositoryGeneratorQualifiedExecutionFamilyGroup,
  RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  group_qualified_repository_generator_execution_families,
)
from repository_generator_qualified_execution_family_selection import (
  RepositoryGeneratorQualifiedExecutionFamilySelection,
  select_qualified_repository_generator_execution_family_by_root_and_source,
)
from repository_generator_qualified_execution_selection import (
  select_qualified_repository_generator_applicability_candidates,
)
from test_phase105_14_qualified_execution_family_grouping import (
  _build_phase105_14_fixture,
)


def test_phase105_16_selects_one_group_by_explicit_root_and_source_identity():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  expected_group = grouping.groups[
    1
  ]

  selection = (
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      expected_group.root_entry,
      expected_group.source_step,
    )
  )

  assert isinstance(
    selection,
    RepositoryGeneratorQualifiedExecutionFamilySelection,
  )
  assert selection.groups == (
    expected_group,
  )
  assert (
    selection.selected_group
    is expected_group
  )


def test_phase105_16_preserves_group_and_representative_identity():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  expected_group = grouping.groups[
    0
  ]

  selection = (
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      expected_group.root_entry,
      expected_group.source_step,
    )
  )

  assert (
    selection.selected_group
    is expected_group
  )
  assert (
    selection.representative
    is expected_group.representative
  )
  assert (
    selection.representative
    is data[
      "first_family_candidates"
    ][0]
  )


def test_phase105_16_does_not_use_shortest_depth_or_group_order_for_selection():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  expected_group = grouping.groups[
    1
  ]

  assert (
    expected_group
    is not grouping.groups[
      0
    ]
  )

  selection = (
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      expected_group.root_entry,
      expected_group.source_step,
    )
  )

  assert (
    selection.selected_group
    is expected_group
  )


def test_phase105_16_actual_standard_group_is_uniquely_selected_by_root_and_source():
  applicability_result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  qualified_selection = (
    select_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  grouping = (
    group_qualified_repository_generator_execution_families(
      qualified_selection
    )
  )

  expected_group = next(
    group
    for group
    in grouping.groups
    if (
      group.root_entry.key
      == "standard.toda.prop58"
    )
  )

  selection = (
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      expected_group.root_entry,
      expected_group.source_step,
    )
  )

  assert len(
    grouping.groups
  ) == 248
  assert selection.groups == (
    expected_group,
  )
  assert (
    selection.selected_group
    is expected_group
  )
  assert (
    selection.representative
    is expected_group.representative
  )


def test_phase105_16_all_actual_standard_root_source_pairs_are_unique():
  applicability_result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  qualified_selection = (
    select_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  grouping = (
    group_qualified_repository_generator_execution_families(
      qualified_selection
    )
  )

  for expected_group in grouping.groups:
    selection = (
      select_qualified_repository_generator_execution_family_by_root_and_source(
        grouping,
        expected_group.root_entry,
        expected_group.source_step,
      )
    )

    assert selection.groups == (
      expected_group,
    )
    assert (
      selection.selected_group
      is expected_group
    )


def test_phase105_16_rejects_foreign_root_entry_identity():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  foreign_root = ProofRepositoryEntry(
    key="phase105.16.foreign.root",
    step=ProofStep(
      conclusion="foreign root",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  with pytest.raises(
    ValueError,
    match=(
      "root_entry must be an original root entry "
      "from grouping"
    ),
  ):
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      foreign_root,
      grouping.groups[
        0
      ].source_step,
    )


def test_phase105_16_rejects_foreign_source_step_identity():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  foreign_source = ProofStep(
    conclusion="foreign source",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "source_step must be an original source step "
      "from grouping"
    ),
  ):
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      grouping.groups[
        0
      ].root_entry,
      foreign_source,
    )


def test_phase105_16_rejects_non_grouping():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "grouping must be a "
      "RepositoryGeneratorQualifiedExecutionFamilyGrouping"
    ),
  ):
    select_qualified_repository_generator_execution_family_by_root_and_source(
      object(),
      grouping.groups[
        0
      ].root_entry,
      grouping.groups[
        0
      ].source_step,
    )


def test_phase105_16_rejects_non_root_entry():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  with pytest.raises(
    TypeError,
    match="root_entry must be a ProofRepositoryEntry",
  ):
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      object(),
      grouping.groups[
        0
      ].source_step,
    )


def test_phase105_16_rejects_non_source_step():
  data = _build_phase105_14_fixture()

  grouping = (
    group_qualified_repository_generator_execution_families(
      data[
        "selection"
      ]
    )
  )

  with pytest.raises(
    TypeError,
    match="source_step must be a ProofStep",
  ):
    select_qualified_repository_generator_execution_family_by_root_and_source(
      grouping,
      grouping.groups[
        0
      ].root_entry,
      object(),
    )
