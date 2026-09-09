from functools import lru_cache

from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase66_delta_iota9_nu_expression import (
  build_phase66_3_data,
)
from test_phase66_whitehead_square_nu_expression import (
  build_phase66_4_data,
)
from test_phase66_delta_iota9_whitehead_square import (
  build_phase66_5_data,
)
from toda_rules import (
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageUpToSignStatement,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
  toda_58_whitehead_square_nu_expression_inference_rule,
  toda_58_delta_iota9_whitehead_square_inference_rule,
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
def build_phase66_6_data():
  phase66_3 = (
    build_phase66_3_data()
  )

  phase66_4 = (
    build_phase66_4_data()
  )

  phase66_5 = (
    build_phase66_5_data()
  )

  delta_nu_step = (
    phase66_3[
      "final_step"
    ]
  )

  whitehead_nu_step = (
    phase66_4[
      "final_step"
    ]
  )

  final_step = (
    phase66_5[
      "final_step"
    ]
  )

  pi7_4_step = (
    phase66_3[
      "pi7_4_step"
    ]
  )

  whitehead_data_step = (
    phase66_4[
      "whitehead_data_step"
    ]
  )

  final_ancestors = (
    collect_ancestor_steps(
      final_step
    )
  )

  final_ancestor_ids = {
    id(
      step
    )
    for step in final_ancestors
  }

  delta_nu_ancestors = (
    collect_ancestor_steps(
      delta_nu_step
    )
  )

  whitehead_nu_ancestors = (
    collect_ancestor_steps(
      whitehead_nu_step
    )
  )

  return {
    "phase66_3": phase66_3,
    "phase66_4": phase66_4,
    "phase66_5": phase66_5,
    "delta_nu_step": delta_nu_step,
    "whitehead_nu_step": (
      whitehead_nu_step
    ),
    "final_step": final_step,
    "pi7_4_step": pi7_4_step,
    "whitehead_data_step": (
      whitehead_data_step
    ),
    "final_ancestors": (
      final_ancestors
    ),
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "delta_nu_ancestors": (
      delta_nu_ancestors
    ),
    "whitehead_nu_ancestors": (
      whitehead_nu_ancestors
    ),
  }


def test_phase66_6_derived_spine_is_all_inference():
  data = build_phase66_6_data()

  derived_spine = (
    data[
      "delta_nu_step"
    ],
    data[
      "whitehead_nu_step"
    ],
    data[
      "final_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in derived_spine
  )


def test_phase66_6_final_reaches_phase66_3():
  data = build_phase66_6_data()

  assert (
    id(
      data[
        "delta_nu_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase66_6_final_reaches_phase66_4():
  data = build_phase66_6_data()

  assert (
    id(
      data[
        "whitehead_nu_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase66_6_delta_branch_reaches_phase65_pi7_4():
  data = build_phase66_6_data()

  ancestor_ids = {
    id(
      step
    )
    for step in data[
      "delta_nu_ancestors"
    ]
  }

  assert (
    id(
      data[
        "pi7_4_step"
      ]
    )
    in ancestor_ids
  )


def test_phase66_6_whitehead_branch_reaches_phase60_data():
  data = build_phase66_6_data()

  ancestor_ids = {
    id(
      step
    )
    for step in data[
      "whitehead_nu_ancestors"
    ]
  }

  assert (
    id(
      data[
        "whitehead_data_step"
      ]
    )
    in ancestor_ids
  )


def test_phase66_6_final_reaches_phase65_and_phase60():
  data = build_phase66_6_data()

  ancestor_ids = (
    data[
      "final_ancestor_ids"
    ]
  )

  assert (
    id(
      data[
        "pi7_4_step"
      ]
    )
    in ancestor_ids
  )

  assert (
    id(
      data[
        "whitehead_data_step"
      ]
    )
    in ancestor_ids
  )


def test_phase66_6_final_graph_is_acyclic():
  data = build_phase66_6_data()

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


def test_phase66_6_final_conclusion_not_in_ancestors():
  data = build_phase66_6_data()

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


def test_phase66_6_phase66_3_does_not_depend_on_final():
  data = build_phase66_6_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor
    in data[
      "delta_nu_ancestors"
    ]
  )


def test_phase66_6_phase66_4_does_not_depend_on_final():
  data = build_phase66_6_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor
    in data[
      "whitehead_nu_ancestors"
    ]
  )


def test_phase66_6_rejects_given_pi7_4_at_phase66_3():
  data = build_phase66_6_data()

  rule = (
    toda_58_delta_iota9_nu4_nu_prime_inference_rule()
  )

  given_pi7_4 = ProofStep(
    conclusion=(
      data[
        "pi7_4_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    rule,
    (
      given_pi7_4,
    ),
  ) is None


def test_phase66_6_rejects_given_delta_at_phase66_4():
  data = build_phase66_6_data()

  rule = (
    toda_58_whitehead_square_nu_expression_inference_rule()
  )

  given_delta = ProofStep(
    conclusion=(
      data[
        "delta_nu_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    rule,
    (
      given_delta,
      data[
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_6_rejects_given_whitehead_data_at_phase66_4():
  data = build_phase66_6_data()

  rule = (
    toda_58_whitehead_square_nu_expression_inference_rule()
  )

  given_whitehead_data = ProofStep(
    conclusion=(
      data[
        "whitehead_data_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    rule,
    (
      data[
        "delta_nu_step"
      ],
      given_whitehead_data,
    ),
  ) is None


def test_phase66_6_rejects_given_delta_at_phase66_5():
  data = build_phase66_6_data()

  rule = (
    toda_58_delta_iota9_whitehead_square_inference_rule()
  )

  given_delta = ProofStep(
    conclusion=(
      data[
        "delta_nu_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    rule,
    (
      given_delta,
      data[
        "whitehead_nu_step"
      ],
    ),
  ) is None


def test_phase66_6_rejects_given_whitehead_at_phase66_5():
  data = build_phase66_6_data()

  rule = (
    toda_58_delta_iota9_whitehead_square_inference_rule()
  )

  given_whitehead = ProofStep(
    conclusion=(
      data[
        "whitehead_nu_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    rule,
    (
      data[
        "delta_nu_step"
      ],
      given_whitehead,
    ),
  ) is None


def test_phase66_6_phase66_4_rejects_phase66_5_delta_result():
  data = build_phase66_6_data()

  rule = (
    toda_58_whitehead_square_nu_expression_inference_rule()
  )

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert find_inference_match(
    rule,
    (
      data[
        "final_step"
      ],
      data[
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_6_phase66_5_requires_whitehead_statement_type():
  data = build_phase66_6_data()

  rule = (
    toda_58_delta_iota9_whitehead_square_inference_rule()
  )

  assert isinstance(
    data[
      "whitehead_nu_step"
    ].conclusion,
    Toda58WhiteheadSquareUpToSignStatement,
  )

  assert find_inference_match(
    rule,
    (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_6_final_directly_reuses_phase66_3_and_phase66_4():
  data = build_phase66_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
    )
  )


def test_phase66_6_final_preserves_delta_instance_objects():
  data = build_phase66_6_data()

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  delta_statement = (
    data[
      "delta_nu_step"
    ].conclusion
  )

  assert (
    final_statement.map
    is delta_statement.map
  )

  assert (
    final_statement.element
    is delta_statement.element
  )


def test_phase66_6_final_preserves_whitehead_object():
  data = build_phase66_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    is data[
      "whitehead_nu_step"
    ].conclusion.whitehead_square
  )


