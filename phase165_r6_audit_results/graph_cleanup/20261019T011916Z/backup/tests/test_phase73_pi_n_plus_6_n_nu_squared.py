from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase73_pi14_8_nu8_squared import (
  build_phase73_8a3_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_nu_family_definition_statement,
  toda_prop511_higher_six_stem_nu_squared_transport_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_8b_data():
  phase73_8a3 = (
    build_phase73_8a3_data()
  )

  pi14_8_step = (
    phase73_8a3[
      "final_step"
    ]
  )

  n = ScalarSymbol(
    name="n",
  )

  phase46 = (
    build_phase46_representative_result(
      n=8,
      k=6,
      m=n,
    )
  )

  stable_isomorphism_step = (
    phase46[
      "theorem_steps"
    ][
      0
    ]
  )

  n_ge_9_statement = (
    ScalarGreaterEqualStatement(
      left=n,
      right=9,
    )
  )

  n_ge_9_step = ProofStep(
    conclusion=n_ge_9_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop511_higher_six_stem_nu_squared_transport_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      pi14_8_step,
      stable_isomorphism_step,
      n_ge_9_step,
    ),
  )

  assert (
    match
    is not None
  )

  final_step = (
    apply_inference_match(
      match
    )
  )

  nu_n = (
    toda_nu_family_definition_statement(
      n
    ).element
  )

  n_plus_three = ScalarSum(
    left=n,
    right=3,
  )

  n_plus_six = ScalarSum(
    left=n,
    right=6,
  )

  nu_n_plus_three = HomotopyElement(
    name="ν_(n+3)",
    dimension=n_plus_three,
    source=n_plus_six,
    target=n_plus_three,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_three,
    ),
  )

  nu_n_squared = Composition(
    left=nu_n,
    right=nu_n_plus_three,
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=n_plus_six,
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu_n_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase73_8a3": (
      phase73_8a3
    ),
    "pi14_8_step": (
      pi14_8_step
    ),
    "n": n,
    "phase46": phase46,
    "stable_isomorphism_step": (
      stable_isomorphism_step
    ),
    "n_ge_9_statement": (
      n_ge_9_statement
    ),
    "n_ge_9_step": (
      n_ge_9_step
    ),
    "rule": rule,
    "final_step": final_step,
    "nu_n": nu_n,
    "n_plus_three": (
      n_plus_three
    ),
    "n_plus_six": (
      n_plus_six
    ),
    "nu_n_plus_three": (
      nu_n_plus_three
    ),
    "nu_n_squared": (
      nu_n_squared
    ),
    "expected_relation": (
      expected_relation
    ),
  }


def test_phase73_8b_reuses_phase73_8a3_pi14_8():
  data = build_phase73_8b_data()

  assert (
    data[
      "pi14_8_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_8b_reuses_derived_toda45_isomorphism():
  data = build_phase73_8b_data()

  assert isinstance(
    data[
      "stable_isomorphism_step"
    ].conclusion,
    Toda45IsomorphismStatement,
  )

  assert (
    data[
      "stable_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_8b_toda45_source_is_pi14_8_structurally():
  data = build_phase73_8b_data()

  source = (
    data[
      "stable_isomorphism_step"
    ]
    .conclusion
    .map
    .source_group
  )

  assert (
    source
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=8,
        right=6,
      ),
      sphere_dimension=8,
    )
  )


def test_phase73_8b_toda45_target_is_pi_n_plus_6_n():
  data = build_phase73_8b_data()

  target = (
    data[
      "stable_isomorphism_step"
    ]
    .conclusion
    .map
    .target_group
  )

  assert (
    target
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=6,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase73_8b_toda45_exponent_is_n_minus_8():
  data = build_phase73_8b_data()

  assert (
    data[
      "stable_isomorphism_step"
    ]
    .conclusion
    .map
    .exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=8,
      ),
    )
  )


def test_phase73_8b_range_is_n_at_least_9():
  data = build_phase73_8b_data()

  assert (
    data[
      "n_ge_9_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=9,
    )
  )

  assert (
    data[
      "n_ge_9_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase73_8b_derives_expected_higher_group():
  data = build_phase73_8b_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_relation"
    ]
  )


def test_phase73_8b_final_group_is_pi_n_plus_6_n():
  data = build_phase73_8b_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=6,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase73_8b_final_group_has_order_two():
  data = build_phase73_8b_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase73_8b_generator_is_symbolic_nu_n_squared():
  data = build_phase73_8b_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.rhs.generator
    == Composition(
      left=data[
        "nu_n"
      ],
      right=data[
        "nu_n_plus_three"
      ],
    )
  )


def test_phase73_8b_generator_is_type_compatible():
  data = build_phase73_8b_data()

  assert (
    data[
      "nu_n_squared"
    ].is_type_compatible()
  )


def test_phase73_8b_shifted_nu_has_expected_structure():
  data = build_phase73_8b_data()

  assert (
    data[
      "nu_n_plus_three"
    ]
    == HomotopyElement(
      name="ν_(n+3)",
      dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=3,
      ),
      source=ScalarSum(
        left=data[
          "n"
        ],
        right=6,
      ),
      target=ScalarSum(
        left=data[
          "n"
        ],
        right=3,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=data[
            "n"
          ],
          right=3,
        ),
      ),
    )
  )


def test_phase73_8b_preserves_exact_provenance():
  data = build_phase73_8b_data()

  final_step = (
    data[
      "final_step"
    ]
  )

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    final_step.premises
    == (
      data[
        "pi14_8_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_9_step"
      ],
    )
  )


def test_phase73_8b_rejects_given_pi14_8_relation():
  data = build_phase73_8b_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi14_8_step"
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
      given_step,
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_9_step"
      ],
    ),
  ) is None


def test_phase73_8b_rejects_given_toda45_isomorphism():
  data = build_phase73_8b_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "stable_isomorphism_step"
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
        "pi14_8_step"
      ],
      given_step,
      data[
        "n_ge_9_step"
      ],
    ),
  ) is None


def test_phase73_8b_rejects_n_at_least_8_as_final_range():
  data = build_phase73_8b_data()

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=8,
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
        "pi14_8_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      wrong_range_step,
    ),
  ) is None

