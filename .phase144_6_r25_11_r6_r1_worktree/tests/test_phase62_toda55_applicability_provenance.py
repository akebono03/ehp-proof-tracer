from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)


def collect_ancestor_steps(
  step,
):
  stack = list(
    step.premises
  )

  seen_ids = set()
  ancestors = []

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if current_id in seen_ids:
      continue

    seen_ids.add(
      current_id
    )

    ancestors.append(
      current
    )

    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
  )


def ancestor_ids(
  step,
):
  return {
    id(
      ancestor
    )
    for ancestor in collect_ancestor_steps(
      step
    )
  }


@lru_cache(maxsize=1)
def build_phase62_7_data():
  phase62_6 = (
    build_phase62_6_data()
  )

  phase62_4 = (
    phase62_6[
      "phase62_4"
    ]
  )

  phase62_3 = (
    phase62_6[
      "phase62_3"
    ]
  )

  phase60_3 = (
    phase62_4[
      "phase60_3"
    ]
  )

  phase58 = (
    phase60_3[
      "phase58"
    ]
  )

  integration_step = (
    phase62_6[
      "integration_step"
    ]
  )

  lemma54_step = (
    phase62_6[
      "lemma54_step"
    ]
  )

  definition_step = (
    phase62_6[
      "definition_step"
    ]
  )

  n_range_step = (
    phase62_6[
      "n_range_step"
    ]
  )

  double_nu_step = (
    phase62_6[
      "double_nu_step"
    ]
  )

  quadruple_nu_step = (
    phase62_6[
      "quadruple_nu_step"
    ]
  )

  triple_eta_step = (
    phase62_4[
      "triple_eta_step"
    ]
  )

  four_to_double_suspended_step = (
    phase62_4[
      "four_to_double_suspended_step"
    ]
  )

  nu_prime_double_step = (
    phase60_3[
      "nu_prime_double_step"
    ]
  )

  phase58_final_double_step = (
    phase58[
      "final_double_step"
    ]
  )

  integration_ancestors = (
    collect_ancestor_steps(
      integration_step
    )
  )

  integration_ancestor_ids = {
    id(
      step
    )
    for step in integration_ancestors
  }

  double_nu_ancestor_ids = (
    ancestor_ids(
      double_nu_step
    )
  )

  quadruple_nu_ancestor_ids = (
    ancestor_ids(
      quadruple_nu_step
    )
  )

  triple_eta_ancestor_ids = (
    ancestor_ids(
      triple_eta_step
    )
  )

  return {
    "phase62_6": phase62_6,
    "phase62_4": phase62_4,
    "phase62_3": phase62_3,
    "phase60_3": phase60_3,
    "phase58": phase58,
    "integration_step": (
      integration_step
    ),
    "lemma54_step": lemma54_step,
    "definition_step": (
      definition_step
    ),
    "n_range_step": n_range_step,
    "double_nu_step": (
      double_nu_step
    ),
    "quadruple_nu_step": (
      quadruple_nu_step
    ),
    "triple_eta_step": (
      triple_eta_step
    ),
    "four_to_double_suspended_step": (
      four_to_double_suspended_step
    ),
    "nu_prime_double_step": (
      nu_prime_double_step
    ),
    "phase58_final_double_step": (
      phase58_final_double_step
    ),
    "integration_ancestors": (
      integration_ancestors
    ),
    "integration_ancestor_ids": (
      integration_ancestor_ids
    ),
    "double_nu_ancestor_ids": (
      double_nu_ancestor_ids
    ),
    "quadruple_nu_ancestor_ids": (
      quadruple_nu_ancestor_ids
    ),
    "triple_eta_ancestor_ids": (
      triple_eta_ancestor_ids
    ),
  }


def test_phase62_7_definition_remains_explicit_given():
  data = build_phase62_7_data()

  assert (
    data[
      "definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase62_7_n_ge_5_remains_explicit_given():
  data = build_phase62_7_data()

  assert (
    data[
      "n_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "n_range_step"
    ].conclusion.right
    == 5
  )


def test_phase62_7_theorem_spine_is_derived():
  data = build_phase62_7_data()

  derived_steps = (
    data[
      "lemma54_step"
    ],
    data[
      "double_nu_step"
    ],
    data[
      "four_to_double_suspended_step"
    ],
    data[
      "triple_eta_step"
    ],
    data[
      "quadruple_nu_step"
    ],
    data[
      "integration_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in derived_steps
  )


def test_phase62_7_final_aggregate_uses_exactly_five_premises():
  data = build_phase62_7_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "double_nu_step"
      ],
      data[
        "quadruple_nu_step"
      ],
    )
  )


def test_phase62_7_final_aggregate_reaches_lemma54():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "lemma54_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase62_7_final_aggregate_reaches_phase62_3():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "double_nu_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase62_7_final_aggregate_reaches_phase62_4():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "quadruple_nu_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase62_7_quadruple_branch_reaches_phase62_3():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "double_nu_step"
      ]
    )
    in data[
      "quadruple_nu_ancestor_ids"
    ]
  )


def test_phase62_7_quadruple_branch_reaches_four_to_double_bridge():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "four_to_double_suspended_step"
      ]
    )
    in data[
      "quadruple_nu_ancestor_ids"
    ]
  )


def test_phase62_7_quadruple_branch_reaches_phase60_triple_eta():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "triple_eta_step"
      ]
    )
    in data[
      "quadruple_nu_ancestor_ids"
    ]
  )


def test_phase62_7_triple_eta_branch_reaches_phase58_double_relation():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "nu_prime_double_step"
      ]
    )
    in data[
      "triple_eta_ancestor_ids"
    ]
  )


def test_phase62_7_phase60_reuses_exact_phase58_final_double_step():
  data = build_phase62_7_data()

  assert (
    data[
      "nu_prime_double_step"
    ]
    is data[
      "phase58_final_double_step"
    ]
  )

  assert (
    data[
      "nu_prime_double_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_7_phase58_double_relation_is_not_given():
  data = build_phase62_7_data()

  assert (
    data[
      "phase58_final_double_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase62_7_double_nu_branch_reaches_lemma54():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "lemma54_step"
      ]
    )
    in data[
      "double_nu_ancestor_ids"
    ]
  )


def test_phase62_7_final_aggregate_graph_is_acyclic():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "integration_step"
      ]
    )
    not in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase62_7_double_nu_branch_does_not_depend_on_final_aggregate():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "integration_step"
      ]
    )
    not in data[
      "double_nu_ancestor_ids"
    ]
  )


def test_phase62_7_quadruple_nu_branch_does_not_depend_on_final_aggregate():
  data = build_phase62_7_data()

  assert (
    id(
      data[
        "integration_step"
      ]
    )
    not in data[
      "quadruple_nu_ancestor_ids"
    ]
  )


def test_phase62_7_final_conclusion_does_not_appear_in_ancestors():
  data = build_phase62_7_data()

  final_conclusion = (
    data[
      "integration_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "integration_ancestors"
    ]
  )


def test_phase62_7_final_aggregate_is_not_given():
  data = build_phase62_7_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


