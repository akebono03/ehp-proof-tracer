from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  ScalarSum,
  ScalarSymbol,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FiniteHomotopyGroupStatement,
  HomotopyGroup,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from toda_rules import (
  TodaLemma510Nu6OrdinaryCompositionReductionStatement,
  TodaLemma510Nu6OrdinaryCompositionZeroStatement,
  TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  serre_42_finite_homotopy_group_inference_rule,
  toda_lemma510_eta9_two_iota10_zero_inference_rule,
  toda_lemma510_nu6_ordinary_composition_reduction_inference_rule,
  toda_lemma510_nu6_ordinary_composition_zero_inference_rule,
  toda_lemma510_ordinary_indeterminacy_double_inference_rule,
  toda_nu_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase72r7_data():
  phase65 = (
    build_phase65_9_data()
  )

  phase59 = (
    build_phase59_8_data()
  )

  phase68 = (
    build_phase68_9_data()
  )

  phase55 = (
    build_phase55_5_integration()
  )

  prop56_step = (
    phase65[
      "integration_step"
    ]
  )

  prop53_step = (
    phase59[
      "integration_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase68[
      "nu6_eta9_zero_step"
    ]
  )

  prop51_step = (
    phase55[
      "integration_steps"
    ][
      0
    ]
  )

  pi11_s9 = HomotopyGroup(
    group_dimension=11,
    sphere_dimension=9,
  )

  pi11_s9_step = ProofStep(
    conclusion=pi11_s9,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  serre_rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  serre_match = find_inference_match(
    serre_rule,
    (
      pi11_s9_step,
    ),
  )

  assert (
    serre_match
    is not None
  )

  finite_pi11_s9_step = (
    apply_inference_match(
      serre_match
    )
  )

  reduction_rule = (
    toda_lemma510_nu6_ordinary_composition_reduction_inference_rule()
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      prop56_step,
      finite_pi11_s9_step,
    ),
  )

  assert (
    reduction_match
    is not None
  )

  reduction_step = (
    apply_inference_match(
      reduction_match
    )
  )

  ordinary_zero_rule = (
    toda_lemma510_nu6_ordinary_composition_zero_inference_rule()
  )

  ordinary_zero_match = (
    find_inference_match(
      ordinary_zero_rule,
      (
        reduction_step,
        prop53_step,
        nu6_eta9_zero_step,
      ),
    )
  )

  assert (
    ordinary_zero_match
    is not None
  )

  ordinary_zero_step = (
    apply_inference_match(
      ordinary_zero_match
    )
  )

  eta9_two_iota10_rule = (
    toda_lemma510_eta9_two_iota10_zero_inference_rule()
  )

  eta9_two_iota10_match = (
    find_inference_match(
      eta9_two_iota10_rule,
      (
        prop51_step,
      ),
    )
  )

  assert (
    eta9_two_iota10_match
    is not None
  )

  eta9_two_iota10_step = (
    apply_inference_match(
      eta9_two_iota10_match
    )
  )

  indeterminacy_rule = (
    toda_lemma510_ordinary_indeterminacy_double_inference_rule()
  )

  indeterminacy_match = (
    find_inference_match(
      indeterminacy_rule,
      (
        ordinary_zero_step,
        nu6_eta9_zero_step,
        eta9_two_iota10_step,
      ),
    )
  )

  assert (
    indeterminacy_match
    is not None
  )

  final_step = (
    apply_inference_match(
      indeterminacy_match
    )
  )

  return {
    "phase65": phase65,
    "phase59": phase59,
    "phase68": phase68,
    "phase55": phase55,
    "prop56_step": prop56_step,
    "prop53_step": prop53_step,
    "prop51_step": prop51_step,
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "pi11_s9": pi11_s9,
    "pi11_s9_step": pi11_s9_step,
    "serre_rule": serre_rule,
    "finite_pi11_s9_step": (
      finite_pi11_s9_step
    ),
    "reduction_rule": reduction_rule,
    "reduction_step": reduction_step,
    "ordinary_zero_rule": (
      ordinary_zero_rule
    ),
    "ordinary_zero_step": (
      ordinary_zero_step
    ),
    "eta9_two_iota10_rule": (
      eta9_two_iota10_rule
    ),
    "eta9_two_iota10_step": (
      eta9_two_iota10_step
    ),
    "indeterminacy_rule": (
      indeterminacy_rule
    ),
    "final_step": final_step,
  }


def test_phase72r7_pi11_s9_finiteness_is_inference():
  data = build_phase72r7_data()

  assert isinstance(
    data[
      "finite_pi11_s9_step"
    ].conclusion,
    FiniteHomotopyGroupStatement,
  )

  assert (
    data[
      "finite_pi11_s9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r7_primary_reduction_is_inference():
  data = build_phase72r7_data()

  assert isinstance(
    data[
      "reduction_step"
    ].conclusion,
    TodaLemma510Nu6OrdinaryCompositionReductionStatement,
  )

  assert (
    data[
      "reduction_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r7_primary_reduction_distinguishes_groups():
  data = build_phase72r7_data()

  statement = (
    data[
      "reduction_step"
    ].conclusion
  )

  assert (
    statement.ordinary_right_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=9,
    )
  )

  assert (
    statement.two_primary_right_group
    == TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=9,
    )
  )

  assert (
    statement.ordinary_right_group
    != statement.two_primary_right_group
  )


def test_phase72r7_primary_reduction_uses_exact_dependencies():
  data = build_phase72r7_data()

  assert (
    data[
      "reduction_step"
    ].premises
    == (
      data[
        "prop56_step"
      ],
      data[
        "finite_pi11_s9_step"
      ],
    )
  )


def test_phase72r7_ordinary_composition_zero_is_inference():
  data = build_phase72r7_data()

  assert isinstance(
    data[
      "ordinary_zero_step"
    ].conclusion,
    TodaLemma510Nu6OrdinaryCompositionZeroStatement,
  )

  assert (
    data[
      "ordinary_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r7_ordinary_zero_uses_phase59_and_phase68():
  data = build_phase72r7_data()

  assert (
    data[
      "ordinary_zero_step"
    ].premises
    == (
      data[
        "reduction_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "nu6_eta9_zero_step"
      ],
    )
  )


def test_phase72r7_eta9_two_iota10_zero_is_inference():
  data = build_phase72r7_data()

  step = (
    data[
      "eta9_two_iota10_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion.relation_type
    == RelationType.ZERO
  )

  assert (
    step.conclusion.rhs
    == Zero()
  )


def test_phase72r7_eta9_zero_reuses_prop51():
  data = build_phase72r7_data()

  assert (
    data[
      "eta9_two_iota10_step"
    ].premises
    == (
      data[
        "prop51_step"
      ],
    )
  )


def test_phase72r7_final_indeterminacy_is_inference():
  data = build_phase72r7_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r7_final_indeterminacy_uses_ordinary_ambient_group():
  data = build_phase72r7_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.ambient_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  assert (
    statement.modulus
    == 2
  )


def test_phase72r7_final_uses_exact_three_dependencies():
  data = build_phase72r7_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "ordinary_zero_step"
      ],
      data[
        "nu6_eta9_zero_step"
      ],
      data[
        "eta9_two_iota10_step"
      ],
    )
  )


def test_phase72r7_reduction_rejects_given_prop56():
  data = build_phase72r7_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop56_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "reduction_rule"
    ],
    (
      given,
      data[
        "finite_pi11_s9_step"
      ],
    ),
  ) is None


def test_phase72r7_reduction_rejects_given_finiteness():
  data = build_phase72r7_data()

  given = ProofStep(
    conclusion=(
      data[
        "finite_pi11_s9_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "reduction_rule"
    ],
    (
      data[
        "prop56_step"
      ],
      given,
    ),
  ) is None


def test_phase72r7_reduction_rejects_wrong_ordinary_group():
  data = build_phase72r7_data()

  wrong = ProofStep(
    conclusion=FiniteHomotopyGroupStatement(
      group=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=8,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "reduction_rule"
    ],
    (
      data[
        "prop56_step"
      ],
      wrong,
    ),
  ) is None


def test_phase72r7_zero_rejects_wrong_prop53_order():
  data = build_phase72r7_data()

  prop53 = (
    data[
      "prop53_step"
    ].conclusion
  )

  higher = (
    prop53
    .higher_eta_squared_group_relation
  )

  wrong_higher = replace(
    higher,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        higher.rhs.generator
      ),
    ),
  )

  wrong_prop53 = replace(
    prop53,
    higher_eta_squared_group_relation=(
      wrong_higher
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop53,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "ordinary_zero_rule"
    ],
    (
      data[
        "reduction_step"
      ],
      wrong_step,
      data[
        "nu6_eta9_zero_step"
      ],
    ),
  ) is None


def test_phase72r7_zero_rejects_given_nu6_eta9_zero():
  data = build_phase72r7_data()

  given = ProofStep(
    conclusion=(
      data[
        "nu6_eta9_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "ordinary_zero_rule"
    ],
    (
      data[
        "reduction_step"
      ],
      data[
        "prop53_step"
      ],
      given,
    ),
  ) is None


def test_phase72r7_eta9_zero_rejects_given_prop51():
  data = build_phase72r7_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop51_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "eta9_two_iota10_rule"
    ],
    (
      given,
    ),
  ) is None


def test_phase72r7_final_rejects_given_ordinary_zero():
  data = build_phase72r7_data()

  given = ProofStep(
    conclusion=(
      data[
        "ordinary_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "indeterminacy_rule"
    ],
    (
      given,
      data[
        "nu6_eta9_zero_step"
      ],
      data[
        "eta9_two_iota10_step"
      ],
    ),
  ) is None


