import pytest

from repository_generator_applicability_selection import (
  RepositoryGeneratorApplicabilitySelection,
  select_repository_generator_applicability_by_source_nodes,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def test_phase104_3b_selects_all_candidates_for_one_source_node():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        data[
          "first_node"
        ],
      ),
    )
  )

  assert isinstance(
    selection,
    RepositoryGeneratorApplicabilitySelection,
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
    data[
      "candidates"
    ][2],
  )


def test_phase104_3b_multiple_source_nodes_preserve_discovery_order():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        data[
          "second_node"
        ],
        data[
          "first_node"
        ],
      ),
    )
  )

  assert selection.candidates == data[
    "candidates"
  ]


def test_phase104_3b_preserves_original_candidate_identity():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        data[
          "second_node"
        ],
      ),
    )
  )

  assert len(
    selection.candidates
  ) == 1

  assert (
    selection.candidates[
      0
    ]
    is data[
      "candidates"
    ][3]
  )


def test_phase104_3b_empty_source_tuple_returns_empty_selection():
  data = build_grouped_fixture()

  selection = (
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (),
    )
  )

  assert selection.candidates == ()


def test_phase104_3b_duplicate_source_nodes_do_not_duplicate_candidates():
  data = build_grouped_fixture()

  first_node = data[
    "first_node"
  ]

  selection = (
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        first_node,
        first_node,
      ),
    )
  )

  assert selection.candidates == (
    data[
      "candidates"
    ][0],
    data[
      "candidates"
    ][1],
    data[
      "candidates"
    ][2],
  )


def test_phase104_3b_rejects_foreign_source_node_identity():
  data = build_grouped_fixture()
  foreign_data = build_grouped_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "each scope_node must be an original source "
      "node from applicability_result"
    ),
  ):
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        foreign_data[
          "first_node"
        ],
      ),
    )


def test_phase104_3b_rejects_non_applicability_result():
  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    select_repository_generator_applicability_by_source_nodes(
      object(),
      (),
    )


def test_phase104_3b_requires_scope_node_tuple():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match="scope_nodes must be a tuple",
  ):
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      [],
    )


def test_phase104_3b_rejects_non_scope_node_member():
  data = build_grouped_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "scope_nodes must contain only "
      "RepositoryProofScopeNode objects"
    ),
  ):
    select_repository_generator_applicability_by_source_nodes(
      data[
        "result"
      ],
      (
        object(),
      ),
    )
