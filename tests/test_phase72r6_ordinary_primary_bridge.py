from dataclasses import replace
from functools import lru_cache

from expression import (
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FiniteHomotopyGroupStatement,
  HomotopyGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_nu5_eta8_squared_zero_delta_eta11 import (
  build_phase70_7_data,
)
from test_phase72r4_serre_finiteness import (
  build_phase72r4_pi10_s5_data,
)
from toda_rules import (
  TodaLemma510OrdinarySuspensionImageFiniteStatement,
  TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
  toda_lemma510_ordinary_suspension_image_finite_inference_rule,
  toda_lemma510_ordinary_suspension_image_in_double_inference_rule,
  toda_lemma510_ordinary_suspension_image_two_primary_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase72r6_data():
  serre = (
    build_phase72r4_pi10_s5_data()
  )

  phase70_7 = (
    build_phase70_7_data()
  )

  finite_group_step = (
    serre[
      "finite_step"
    ]
  )

  pi10_5_step = (
    phase70_7[
      "pi10_5_step"
    ]
  )

  suspension_zero_step = (
    phase70_7[
      "suspension_zero_step"
    ]
  )

  finite_image_rule = (
    toda_lemma510_ordinary_suspension_image_finite_inference_rule()
  )

  finite_image_match = find_inference_match(
    finite_image_rule,
    (
      finite_group_step,
    ),
  )

  assert (
    finite_image_match
    is not None
  )

  finite_image_step = (
    apply_inference_match(
      finite_image_match
    )
  )

  two_primary_zero_rule = (
    toda_lemma510_ordinary_suspension_image_two_primary_zero_inference_rule()
  )

  two_primary_zero_match = (
    find_inference_match(
      two_primary_zero_rule,
      (
        pi10_5_step,
        suspension_zero_step,
      ),
    )
  )

  assert (
    two_primary_zero_match
    is not None
  )

  two_primary_zero_step = (
    apply_inference_match(
      two_primary_zero_match
    )
  )

  double_rule = (
    toda_lemma510_ordinary_suspension_image_in_double_inference_rule()
  )

  double_match = find_inference_match(
    double_rule,
    (
      finite_image_step,
      two_primary_zero_step,
    ),
  )

  assert (
    double_match
    is not None
  )

  final_step = (
    apply_inference_match(
      double_match
    )
  )

  return {
    "serre": serre,
    "phase70_7": phase70_7,
    "finite_group_step": (
      finite_group_step
    ),
    "pi10_5_step": (
      pi10_5_step
    ),
    "suspension_zero_step": (
      suspension_zero_step
    ),
    "finite_image_rule": (
      finite_image_rule
    ),
    "finite_image_step": (
      finite_image_step
    ),
    "two_primary_zero_rule": (
      two_primary_zero_rule
    ),
    "two_primary_zero_step": (
      two_primary_zero_step
    ),
    "double_rule": double_rule,
    "final_step": final_step,
  }


def test_phase72r6_reuses_serre_finiteness():
  data = build_phase72r6_data()

  assert isinstance(
    data[
      "finite_group_step"
    ].conclusion,
    FiniteHomotopyGroupStatement,
  )

  assert (
    data[
      "finite_group_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r6_finite_image_is_inference():
  data = build_phase72r6_data()

  step = (
    data[
      "finite_image_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510OrdinarySuspensionImageFiniteStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72r6_finite_image_has_ordinary_groups():
  data = build_phase72r6_data()

  statement = (
    data[
      "finite_image_step"
    ].conclusion
  )

  assert (
    statement.source_group
    == HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )

  assert (
    statement.target_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  assert (
    statement.suspension_map
    == EHP_E_MAP
  )


def test_phase72r6_finite_image_uses_exact_serre_dependency():
  data = build_phase72r6_data()

  assert (
    data[
      "finite_image_step"
    ].premises
    == (
      data[
        "finite_group_step"
      ],
    )
  )


def test_phase72r6_reuses_phase70_pi10_5():
  data = build_phase72r6_data()

  assert (
    data[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_5_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )


def test_phase72r6_reuses_phase70_suspension_zero():
  data = build_phase72r6_data()

  assert (
    data[
      "suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "suspension_zero_step"
    ].conclusion.relation_type
    == RelationType.ZERO
  )


def test_phase72r6_two_primary_image_zero_is_inference():
  data = build_phase72r6_data()

  step = (
    data[
      "two_primary_zero_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72r6_two_primary_zero_uses_exact_phase70_dependencies():
  data = build_phase72r6_data()

  assert (
    data[
      "two_primary_zero_step"
    ].premises
    == (
      data[
        "pi10_5_step"
      ],
      data[
        "suspension_zero_step"
      ],
    )
  )


def test_phase72r6_final_is_ordinary_image_in_double():
  data = build_phase72r6_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  )

  assert (
    statement.suspension_map
    == EHP_E_MAP
  )

  assert (
    statement.source_group
    == HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )

  assert (
    statement.target_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  assert (
    statement.modulus
    == 2
  )


def test_phase72r6_final_is_inference_not_given():
  data = build_phase72r6_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72r6_final_uses_exact_two_branches():
  data = build_phase72r6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "finite_image_step"
      ],
      data[
        "two_primary_zero_step"
      ],
    )
  )


def test_phase72r6_finite_image_rejects_given_finiteness():
  data = build_phase72r6_data()

  given = ProofStep(
    conclusion=(
      data[
        "finite_group_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "finite_image_rule"
    ],
    (
      given,
    ),
  ) is None


def test_phase72r6_finite_image_rejects_wrong_source_group():
  data = build_phase72r6_data()

  wrong = ProofStep(
    conclusion=FiniteHomotopyGroupStatement(
      group=HomotopyGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "finite_image_rule"
    ],
    (
      wrong,
    ),
  ) is None


def test_phase72r6_two_primary_zero_rejects_wrong_order():
  data = build_phase72r6_data()

  relation = (
    data[
      "pi10_5_step"
    ].conclusion
  )

  wrong = ProofStep(
    conclusion=replace(
      relation,
      rhs=FiniteCyclicGroup(
        order=4,
        generator=(
          relation
          .rhs
          .generator
        ),
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "two_primary_zero_rule"
    ],
    (
      wrong,
      data[
        "suspension_zero_step"
      ],
    ),
  ) is None


def test_phase72r6_two_primary_zero_rejects_wrong_suspension_zero():
  data = build_phase72r6_data()

  generator = (
    data[
      "pi10_5_step"
    ].conclusion
    .rhs
    .generator
  )

  wrong = ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=generator,
      ),
      rhs=generator,
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "two_primary_zero_rule"
    ],
    (
      data[
        "pi10_5_step"
      ],
      wrong,
    ),
  ) is None


def test_phase72r6_final_rejects_given_finite_image():
  data = build_phase72r6_data()

  given = ProofStep(
    conclusion=(
      data[
        "finite_image_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      given,
      data[
        "two_primary_zero_step"
      ],
    ),
  ) is None


def test_phase72r6_final_rejects_wrong_target_group():
  data = build_phase72r6_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "two_primary_zero_step"
      ].conclusion,
      target_group=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=7,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      data[
        "finite_image_step"
      ],
      wrong,
    ),
  ) is None


def test_phase72r6_final_rejects_wrong_map():
  data = build_phase72r6_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "two_primary_zero_step"
      ].conclusion,
      suspension_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      data[
        "finite_image_step"
      ],
      wrong,
    ),
  ) is None


