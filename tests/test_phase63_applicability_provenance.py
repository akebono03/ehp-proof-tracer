from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase63_toda56_semantics import (
  build_phase63_4_data,
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


def build_phase63_5_data():
  phase63_4 = (
    build_phase63_4_data()
  )

  phase63_3 = (
    phase63_4[
      "phase63_3"
    ]
  )

  phase63_2 = (
    phase63_3[
      "phase63_2"
    ]
  )

  phase60_9 = (
    phase63_2[
      "phase60_9"
    ]
  )

  toda56_step = (
    phase63_4[
      "toda56_step"
    ]
  )

  prop44_isomorphism_step = (
    phase63_4[
      "prop44_isomorphism_step"
    ]
  )

  specialization_step = (
    phase63_3[
      "specialization_step"
    ]
  )

  decomposition_map_step = (
    phase63_3[
      "decomposition_map_step"
    ]
  )

  lemma54_step = (
    phase63_2[
      "lemma54_step"
    ]
  )

  membership_step = (
    phase60_9[
      "membership_step"
    ]
  )

  hopf_step = (
    phase60_9[
      "hopf_step"
    ]
  )

  double_step = (
    phase60_9[
      "double_step"
    ]
  )

  final_ancestors = (
    collect_ancestor_steps(
      toda56_step
    )
  )

  final_ancestor_ids = {
    id(
      step
    )
    for step in final_ancestors
  }

  prop44_ancestor_ids = (
    ancestor_ids(
      prop44_isomorphism_step
    )
  )

  specialization_ancestor_ids = (
    ancestor_ids(
      specialization_step
    )
  )

  lemma54_ancestor_ids = (
    ancestor_ids(
      lemma54_step
    )
  )

  return {
    "phase63_4": phase63_4,
    "phase63_3": phase63_3,
    "phase63_2": phase63_2,
    "phase60_9": phase60_9,
    "toda56_step": toda56_step,
    "prop44_isomorphism_step": (
      prop44_isomorphism_step
    ),
    "specialization_step": (
      specialization_step
    ),
    "decomposition_map_step": (
      decomposition_map_step
    ),
    "lemma54_step": lemma54_step,
    "membership_step": membership_step,
    "hopf_step": hopf_step,
    "double_step": double_step,
    "final_ancestors": final_ancestors,
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "prop44_ancestor_ids": (
      prop44_ancestor_ids
    ),
    "specialization_ancestor_ids": (
      specialization_ancestor_ids
    ),
    "lemma54_ancestor_ids": (
      lemma54_ancestor_ids
    ),
  }


def test_phase63_5_decomposition_map_remains_explicit_given():
  data = build_phase63_5_data()

  assert (
    data[
      "decomposition_map_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase63_5_theorem_spine_is_derived():
  data = build_phase63_5_data()

  theorem_steps = (
    data[
      "membership_step"
    ],
    data[
      "hopf_step"
    ],
    data[
      "double_step"
    ],
    data[
      "lemma54_step"
    ],
    data[
      "specialization_step"
    ],
    data[
      "prop44_isomorphism_step"
    ],
    data[
      "toda56_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in theorem_steps
  )


def test_phase63_5_toda56_uses_exactly_prop44_isomorphism():
  data = build_phase63_5_data()

  assert (
    data[
      "toda56_step"
    ].premises
    == (
      data[
        "prop44_isomorphism_step"
      ],
    )
  )


def test_phase63_5_prop44_uses_specialization_and_map():
  data = build_phase63_5_data()

  assert (
    data[
      "prop44_isomorphism_step"
    ].premises
    == (
      data[
        "specialization_step"
      ],
      data[
        "decomposition_map_step"
      ],
    )
  )


def test_phase63_5_specialization_uses_exactly_lemma54():
  data = build_phase63_5_data()

  assert (
    data[
      "specialization_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
    )
  )


def test_phase63_5_reuses_exact_phase60_lemma54_step():
  data = build_phase63_5_data()

  assert (
    data[
      "lemma54_step"
    ]
    is data[
      "phase60_9"
    ][
      "integration_step"
    ]
  )


def test_phase63_5_final_reaches_prop44_isomorphism():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "prop44_isomorphism_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_phase63_2_specialization():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "specialization_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_lemma54():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "lemma54_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_phase60_membership():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "membership_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_phase60_hopf_relation():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "hopf_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_phase60_double_relation():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "double_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_reaches_explicit_decomposition_map():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "decomposition_map_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_rejects_given_lemma54():
  data = build_phase63_5_data()

  given_lemma54_step = ProofStep(
    conclusion=(
      data[
        "lemma54_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "phase63_2"
    ][
      "rule"
    ],
    (
      given_lemma54_step,
    ),
  ) is None


def test_phase63_5_rejects_given_specialization():
  data = build_phase63_5_data()

  given_specialization_step = ProofStep(
    conclusion=(
      data[
        "specialization_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "phase63_3"
    ][
      "rule"
    ],
    (
      given_specialization_step,
      data[
        "decomposition_map_step"
      ],
    ),
  ) is None


def test_phase63_5_rejects_given_prop44_isomorphism():
  data = build_phase63_5_data()

  given_prop44_step = ProofStep(
    conclusion=(
      data[
        "prop44_isomorphism_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "phase63_4"
    ][
      "rule"
    ],
    (
      given_prop44_step,
    ),
  ) is None


def test_phase63_5_final_graph_is_acyclic():
  data = build_phase63_5_data()

  assert (
    id(
      data[
        "toda56_step"
      ]
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase63_5_final_conclusion_does_not_appear_in_ancestors():
  data = build_phase63_5_data()

  final_conclusion = (
    data[
      "toda56_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "final_ancestors"
    ]
  )


def test_phase63_5_upstream_steps_do_not_depend_on_final_result():
  data = build_phase63_5_data()

  final_id = id(
    data[
      "toda56_step"
    ]
  )

  assert (
    final_id
    not in data[
      "prop44_ancestor_ids"
    ]
  )

  assert (
    final_id
    not in data[
      "specialization_ancestor_ids"
    ]
  )

  assert (
    final_id
    not in data[
      "lemma54_ancestor_ids"
    ]
  )


def test_phase63_5_final_result_is_not_given():
  data = build_phase63_5_data()

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "toda56_step"
    ].rule
    != ProofRule.GIVEN
  )


