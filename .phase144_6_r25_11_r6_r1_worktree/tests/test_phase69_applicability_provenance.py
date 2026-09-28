from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase69_delta_iota11 import (
  build_phase69_3_data,
)


def collect_ancestor_steps(
  step,
):
  ancestors = []
  seen_ids = set()

  def visit(
    current,
  ):
    for premise in current.premises:
      premise_id = id(
        premise
      )

      if (
        premise_id
        in seen_ids
      ):
        continue

      seen_ids.add(
        premise_id
      )

      ancestors.append(
        premise
      )

      visit(
        premise
      )

  visit(
    step
  )

  return tuple(
    ancestors
  )


@lru_cache(maxsize=1)
def build_phase69_4_data():
  phase69_3 = (
    build_phase69_3_data()
  )

  phase68_11 = (
    build_phase68_11_data()
  )

  final_step = (
    phase69_3[
      "final_step"
    ]
  )

  delta_surjective_step = (
    phase69_3[
      "delta_surjective_step"
    ]
  )

  pi11_11_step = (
    phase69_3[
      "pi11_11_step"
    ]
  )

  pi9_5_step = (
    phase69_3[
      "pi9_5_step"
    ]
  )

  phase69_2 = (
    phase69_3[
      "phase69_2"
    ]
  )

  pi10_6_zero_step = (
    phase69_2[
      "pi10_6_zero_step"
    ]
  )

  exactness_step = (
    phase69_2[
      "exactness_step"
    ]
  )

  exactness_window_step = (
    phase69_2[
      "exactness_window_step"
    ]
  )

  phase68_aggregate_step = (
    phase68_11[
      "integration_step"
    ]
  )

  final_ancestors = (
    collect_ancestor_steps(
      final_step
    )
  )

  final_ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in final_ancestors
  }

  delta_surjective_ancestors = (
    collect_ancestor_steps(
      delta_surjective_step
    )
  )

  delta_surjective_ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in delta_surjective_ancestors
  }

  pi9_5_ancestors = (
    collect_ancestor_steps(
      pi9_5_step
    )
  )

  pi9_5_ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in pi9_5_ancestors
  }

  return {
    "phase69_3": phase69_3,
    "phase69_2": phase69_2,
    "phase68_11": phase68_11,
    "final_step": final_step,
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "pi11_11_step": pi11_11_step,
    "pi9_5_step": pi9_5_step,
    "pi10_6_zero_step": (
      pi10_6_zero_step
    ),
    "exactness_step": exactness_step,
    "exactness_window_step": (
      exactness_window_step
    ),
    "phase68_aggregate_step": (
      phase68_aggregate_step
    ),
    "final_ancestors": (
      final_ancestors
    ),
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "delta_surjective_ancestors": (
      delta_surjective_ancestors
    ),
    "delta_surjective_ancestor_ids": (
      delta_surjective_ancestor_ids
    ),
    "pi9_5_ancestors": (
      pi9_5_ancestors
    ),
    "pi9_5_ancestor_ids": (
      pi9_5_ancestor_ids
    ),
  }


def test_phase69_4_final_is_inference():
  data = build_phase69_4_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_4_final_is_not_given():
  data = build_phase69_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase69_4_final_direct_premises_are_exact():
  data = build_phase69_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi11_11_step"
      ],
      data[
        "pi9_5_step"
      ],
    )
  )


def test_phase69_4_delta_surjective_is_derived():
  data = build_phase69_4_data()

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_4_pi9_5_is_derived():
  data = build_phase69_4_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_4_pi11_11_remains_foundational_given():
  data = build_phase69_4_data()

  assert (
    data[
      "pi11_11_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase69_4_pi10_6_zero_is_derived():
  data = build_phase69_4_data()

  assert (
    data[
      "pi10_6_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_4_exactness_is_derived():
  data = build_phase69_4_data()

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_4_exactness_window_remains_given():
  data = build_phase69_4_data()

  assert (
    data[
      "exactness_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase69_4_final_reaches_delta_surjective():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "delta_surjective_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_reaches_pi9_5():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "pi9_5_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_reaches_pi11_11_foundation():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "pi11_11_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_reaches_pi10_6_zero():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "pi10_6_zero_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_reaches_phase69_exactness():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "exactness_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_reaches_structural_exactness_window():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "exactness_window_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_delta_surjective_reaches_pi10_6_zero():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "pi10_6_zero_step"
      ]
    )
    in data[
      "delta_surjective_ancestor_ids"
    ]
  )


def test_phase69_4_delta_surjective_reaches_exactness():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "exactness_step"
      ]
    )
    in data[
      "delta_surjective_ancestor_ids"
    ]
  )


def test_phase69_4_final_graph_is_acyclic():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_final_conclusion_not_in_ancestors():
  data = build_phase69_4_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase69_4_delta_surjective_does_not_depend_on_final():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in data[
      "delta_surjective_ancestor_ids"
    ]
  )


def test_phase69_4_pi9_5_does_not_depend_on_final():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in data[
      "pi9_5_ancestor_ids"
    ]
  )


def test_phase69_4_phase68_aggregate_is_not_final_ancestor():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "phase68_aggregate_step"
      ]
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase69_4_phase68_aggregate_is_not_direct_premise():
  data = build_phase69_4_data()

  assert (
    data[
      "phase68_aggregate_step"
    ]
    not in data[
      "final_step"
    ].premises
  )


def test_phase69_4_final_uses_phase68_pi9_5_branch_directly():
  data = build_phase69_4_data()

  assert (
    data[
      "pi9_5_step"
    ]
    in data[
      "final_step"
    ].premises
  )


def test_phase69_4_phase69_2_does_not_use_phase68_aggregate():
  data = build_phase69_4_data()

  assert (
    id(
      data[
        "phase68_aggregate_step"
      ]
    )
    not in data[
      "delta_surjective_ancestor_ids"
    ]
  )


