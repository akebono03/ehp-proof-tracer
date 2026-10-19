from functools import lru_cache

from repository_inference import (
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from test_phase84_producer_premise_availability import (
  build_phase84_3_data,
)


@lru_cache(maxsize=1)
def build_phase84_4_data():
  phase84_3 = build_phase84_3_data()

  result = (
    select_unique_depth_two_producer_chain(
      phase84_3[
        "repository"
      ],
      phase84_3[
        "catalog"
      ],
      phase84_3[
        "goal"
      ],
    )
  )

  assert result is not None

  bracket_sum_node = next(
    node
    for node in result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "bracket_sum_rule"
      ]
    )
  )

  composition_node = next(
    node
    for node in result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "composition_rule"
      ]
    )
  )

  return {
    "phase84_3": phase84_3,
    "result": result,
    "bracket_sum_node": (
      bracket_sum_node
    ),
    "composition_node": (
      composition_node
    ),
  }


def test_phase84_4_selects_actual_final_rule():
  data = build_phase84_4_data()

  assert (
    data[
      "result"
    ].final_rule
    is data[
      "phase84_3"
    ][
      "final_rule"
    ]
  )


def test_phase84_4_selects_two_unique_producer_nodes():
  data = build_phase84_4_data()

  assert len(
    data[
      "result"
    ].producer_nodes
  ) == 2

  assert tuple(
    node.producer_rule
    for node in data[
      "result"
    ].producer_nodes
  ) == (
    data[
      "phase84_3"
    ][
      "bracket_sum_rule"
    ],
    data[
      "phase84_3"
    ][
      "composition_rule"
    ],
  )


def test_phase84_4_bracket_sum_is_shared_across_depths():
  data = build_phase84_4_data()

  node = data[
    "bracket_sum_node"
  ]

  assert node.depths == (
    1,
    2,
  )

  assert node.minimum_depth == 1
  assert node.maximum_depth == 2
  assert node.is_shared


def test_phase84_4_composition_has_bracket_sum_dependency():
  data = build_phase84_4_data()

  assert (
    data[
      "composition_node"
    ].dependencies
    == (
      data[
        "bracket_sum_node"
      ],
    )
  )


def test_phase84_4_dependency_uses_same_shared_node_object():
  data = build_phase84_4_data()

  assert (
    data[
      "composition_node"
    ].dependencies[
      0
    ]
    is data[
      "bracket_sum_node"
    ]
  )


def test_phase84_4_nodes_are_dependency_first_ordered():
  data = build_phase84_4_data()

  assert (
    data[
      "result"
    ].producer_nodes[
      0
    ]
    is data[
      "bracket_sum_node"
    ]
  )

  assert (
    data[
      "result"
    ].producer_nodes[
      1
    ]
    is data[
      "composition_node"
    ]
  )


def test_phase84_4_preserves_producer_availability():
  data = build_phase84_4_data()

  bracket_sum_availability = data[
    "bracket_sum_node"
  ].producer_availability

  composition_availability = data[
    "composition_node"
  ].producer_availability

  assert bracket_sum_availability.is_complete

  assert (
    composition_availability
    .missing_indices
    == (
      0,
    )
  )


def test_phase84_4_selected_chain_is_within_depth_two():
  data = build_phase84_4_data()

  assert (
    data[
      "result"
    ].max_depth
    == 2
  )

  assert (
    data[
      "result"
    ].is_within_depth_limit
  )


def test_phase84_4_selection_does_not_execute_producers():
  data = build_phase84_4_data()
  phase84_3 = data[
    "phase84_3"
  ]

  bracket_sum_conclusion = phase84_3[
    "phase77"
  ][
    "bracket_sum_step"
  ].conclusion

  composition_conclusion = phase84_3[
    "phase77"
  ][
    "composition_step"
  ].conclusion

  assert all(
    step.conclusion
    not in (
      bracket_sum_conclusion,
      composition_conclusion,
    )
    for step in data[
      "result"
    ].final_availability.matched_steps
    if step is not None
  )


def test_phase84_4_selection_does_not_mutate_repository():
  data = build_phase84_4_data()
  phase84_3 = data[
    "phase84_3"
  ]

  assert (
    repository_available_steps(
      phase84_3[
        "repository"
      ]
    )
    == phase84_3[
      "initial_steps"
    ]
  )
