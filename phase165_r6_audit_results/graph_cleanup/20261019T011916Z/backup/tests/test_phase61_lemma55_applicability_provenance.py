from dataclasses import replace

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  Zero,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase61_lemma55_integration import (
  build_phase61_6_data,
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


def build_phase61_7_data():
  phase61_6 = (
    build_phase61_6_data()
  )

  phase61_5 = (
    phase61_6[
      "phase61_5"
    ]
  )

  phase61_3 = (
    phase61_6[
      "phase61_3"
    ]
  )

  phase61_4 = (
    phase61_5[
      "phase61_4"
    ]
  )

  integration_step = (
    phase61_6[
      "integration_step"
    ]
  )

  lemma54_step = (
    phase61_6[
      "lemma54_step"
    ]
  )

  alpha_star_inclusion_step = (
    phase61_5[
      "alpha_star_inclusion_step"
    ]
  )

  suspension_step = (
    phase61_5[
      "suspension_step"
    ]
  )

  final_inclusion_step = (
    phase61_6[
      "final_inclusion_step"
    ]
  )

  theorem36_step = (
    phase61_3[
      "theorem36_step"
    ]
  )

  construction_step = (
    phase61_4[
      "construction_step"
    ]
  )

  ancestor_steps = (
    collect_ancestor_steps(
      integration_step
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestor_steps
  }

  return {
    "phase61_6": phase61_6,
    "phase61_5": phase61_5,
    "phase61_4": phase61_4,
    "phase61_3": phase61_3,
    "integration_step": (
      integration_step
    ),
    "lemma54_step": lemma54_step,
    "alpha_star_inclusion_step": (
      alpha_star_inclusion_step
    ),
    "suspension_step": (
      suspension_step
    ),
    "final_inclusion_step": (
      final_inclusion_step
    ),
    "theorem36_step": (
      theorem36_step
    ),
    "construction_step": (
      construction_step
    ),
    "ancestor_steps": (
      ancestor_steps
    ),
    "ancestor_ids": ancestor_ids,
    "rule": phase61_6[
      "rule"
    ],
  }


def test_phase61_7_hypotheses_remain_explicit_inputs():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  assert (
    phase61_6[
      "beta_membership_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    phase61_6[
      "beta_eta_zero_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    phase61_6[
      "t_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase61_7_derived_spine_is_all_inference():
  data = build_phase61_7_data()

  derived_steps = (
    data[
      "theorem36_step"
    ],
    data[
      "construction_step"
    ],
    data[
      "lemma54_step"
    ],
    data[
      "alpha_star_inclusion_step"
    ],
    data[
      "suspension_step"
    ],
    data[
      "final_inclusion_step"
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


def test_phase61_7_final_aggregate_uses_exactly_phase61_6_premises():
  data = build_phase61_7_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "phase61_6"
    ][
      "premise_steps"
    ]
  )


def test_phase61_7_final_inclusion_reaches_phase61_3_and_phase61_4():
  data = build_phase61_7_data()

  final_ancestors = (
    collect_ancestor_steps(
      data[
        "final_inclusion_step"
      ]
    )
  )

  final_ancestor_ids = {
    id(
      step
    )
    for step in final_ancestors
  }

  assert (
    id(
      data[
        "alpha_star_inclusion_step"
      ]
    )
    in final_ancestor_ids
  )

  assert (
    id(
      data[
        "suspension_step"
      ]
    )
    in final_ancestor_ids
  )


def test_phase61_7_alpha_star_branch_reaches_phase60_theorem36():
  data = build_phase61_7_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "alpha_star_inclusion_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "theorem36_step"
      ]
    )
    in ancestor_ids
  )


def test_phase61_7_nu4_branch_reaches_phase60_construction():
  data = build_phase61_7_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "suspension_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "construction_step"
      ]
    )
    in ancestor_ids
  )


def test_phase61_7_final_aggregate_directly_reuses_lemma54_aggregate():
  data = build_phase61_7_data()

  assert (
    data[
      "lemma54_step"
    ]
    in data[
      "integration_step"
    ].premises
  )

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_7_provenance_graph_is_acyclic():
  data = build_phase61_7_data()

  assert (
    id(
      data[
        "integration_step"
      ]
    )
    not in data[
      "ancestor_ids"
    ]
  )


def test_phase61_7_final_conclusion_does_not_appear_in_ancestors():
  data = build_phase61_7_data()

  final_conclusion = (
    data[
      "integration_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "ancestor_steps"
    ]
  )


def test_phase61_7_rejects_wrong_beta_group():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  phase61_3 = data[
    "phase61_3"
  ]

  wrong_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=phase61_3[
          "beta"
        ],
        group_dimension=ScalarSum(
          left=phase61_3[
            "t"
          ],
          right=3,
        ),
        sphere_dimension=phase61_3[
          "m"
        ],
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      wrong_membership_step,
      phase61_6[
        "beta_eta_zero_step"
      ],
      phase61_6[
        "t_range_step"
      ],
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_7_rejects_wrong_beta_eta_zero_relation():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  phase61_3 = data[
    "phase61_3"
  ]

  t = phase61_3[
    "t"
  ]

  t_plus_three = ScalarSum(
    left=t,
    right=3,
  )

  t_plus_four = ScalarSum(
    left=t,
    right=4,
  )

  wrong_eta = HomotopyElement(
    name="η_(t+3)",
    dimension=t_plus_three,
    source=t_plus_four,
    target=t_plus_three,
    generator=GeneratorSymbol(
      family="η",
      index=t_plus_three,
    ),
  )

  wrong_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=phase61_3[
          "beta"
        ],
        right=wrong_eta,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      phase61_6[
        "beta_membership_step"
      ],
      wrong_zero_step,
      phase61_6[
        "t_range_step"
      ],
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_7_rejects_t_at_least_zero():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "phase61_3"
      ][
        "t"
      ],
      right=0,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      phase61_6[
        "beta_membership_step"
      ],
      phase61_6[
        "beta_eta_zero_step"
      ],
      wrong_range_step,
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_7_rejects_final_inclusion_with_alpha_star_instead_of_nu4():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  phase61_3 = data[
    "phase61_3"
  ]

  final_statement = (
    data[
      "final_inclusion_step"
    ].conclusion
  )

  wrong_positive_value = Composition(
    left=(
      final_statement
      .positive_value
      .left
    ),
    right=IteratedSuspension(
      expression=phase61_3[
        "alpha_star"
      ],
      exponent=phase61_3[
        "t"
      ],
    ),
  )

  wrong_inclusion = replace(
    final_statement,
    positive_value=(
      wrong_positive_value
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_inclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      phase61_6[
        "beta_membership_step"
      ],
      phase61_6[
        "beta_eta_zero_step"
      ],
      phase61_6[
        "t_range_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase61_7_rejects_given_lemma54_aggregate():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

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
      "rule"
    ],
    (
      given_lemma54_step,
      phase61_6[
        "beta_membership_step"
      ],
      phase61_6[
        "beta_eta_zero_step"
      ],
      phase61_6[
        "t_range_step"
      ],
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_7_rejects_given_final_inclusion():
  data = build_phase61_7_data()

  phase61_6 = data[
    "phase61_6"
  ]

  given_final_step = ProofStep(
    conclusion=(
      data[
        "final_inclusion_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      phase61_6[
        "beta_membership_step"
      ],
      phase61_6[
        "beta_eta_zero_step"
      ],
      phase61_6[
        "t_range_step"
      ],
      given_final_step,
    ),
  ) is None


