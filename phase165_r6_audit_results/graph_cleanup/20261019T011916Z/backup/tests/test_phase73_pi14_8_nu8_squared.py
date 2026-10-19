from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase73_pi13_7_nu7_squared import (
  build_phase73_7c_data,
)
from test_phase73_pi14_8_prop44_suspension_isomorphism import (
  build_phase73_8a2_data,
)
from toda_rules import (
  toda_nu_family_definition_statement,
  toda_prop511_pi14_8_nu8_squared_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_8a3_data():
  phase73_7c = (
    build_phase73_7c_data()
  )

  phase73_8a2 = (
    build_phase73_8a2_data()
  )

  pi13_7_step = (
    phase73_7c[
      "final_step"
    ]
  )

  suspension_isomorphism_step = (
    phase73_8a2[
      "final_step"
    ]
  )

  rule = (
    toda_prop511_pi14_8_nu8_squared_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      pi13_7_step,
      suspension_isomorphism_step,
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

  nu_8 = (
    toda_nu_family_definition_statement(
      8
    ).element
  )

  nu_11 = (
    toda_nu_family_definition_statement(
      11
    ).element
  )

  nu8_squared = Composition(
    left=nu_8,
    right=nu_11,
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu8_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase73_7c": (
      phase73_7c
    ),
    "phase73_8a2": (
      phase73_8a2
    ),
    "pi13_7_step": (
      pi13_7_step
    ),
    "suspension_isomorphism_step": (
      suspension_isomorphism_step
    ),
    "rule": rule,
    "final_step": final_step,
    "nu_8": nu_8,
    "nu_11": nu_11,
    "nu8_squared": (
      nu8_squared
    ),
    "expected_relation": (
      expected_relation
    ),
  }


def test_phase73_8a3_derives_pi14_8_nu8_squared():
  data = build_phase73_8a3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_relation"
    ]
  )


def test_phase73_8a3_group_is_pi14_8():
  data = build_phase73_8a3_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    )
  )


def test_phase73_8a3_group_order_is_two():
  data = build_phase73_8a3_data()

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


def test_phase73_8a3_generator_is_canonical_nu8_squared():
  data = build_phase73_8a3_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.rhs.generator
    == Composition(
      left=(
        toda_nu_family_definition_statement(
          8
        ).element
      ),
      right=(
        toda_nu_family_definition_statement(
          11
        ).element
      ),
    )
  )


def test_phase73_8a3_generator_is_type_compatible():
  data = build_phase73_8a3_data()

  assert (
    data[
      "nu8_squared"
    ].is_type_compatible()
  )


def test_phase73_8a3_preserves_provenance():
  data = build_phase73_8a3_data()

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
        "pi13_7_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
    )
  )


def test_phase73_8a3_rejects_wrong_source_order():
  data = build_phase73_8a3_data()

  source_relation = (
    data[
      "pi13_7_step"
    ].conclusion
  )

  wrong_relation = replace(
    source_relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        source_relation
        .rhs
        .generator
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "suspension_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_8a3_rejects_wrong_source_generator():
  data = build_phase73_8a3_data()

  source_relation = (
    data[
      "pi13_7_step"
    ].conclusion
  )

  nu_7 = (
    toda_nu_family_definition_statement(
      7
    ).element
  )

  nu_11 = (
    toda_nu_family_definition_statement(
      11
    ).element
  )

  wrong_relation = replace(
    source_relation,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=nu_7,
        right=nu_11,
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "suspension_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_8a3_rejects_wrong_suspension_target():
  data = build_phase73_8a3_data()

  wrong_isomorphism = (
    TodaSuspensionIsomorphismStatement(
      map=TodaSuspensionMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=7,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=15,
          sphere_dimension=9,
        ),
      ),
    )
  )

  wrong_step = ProofStep(
    conclusion=wrong_isomorphism,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi13_7_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase73_8a3_rejects_given_source_relation():
  data = build_phase73_8a3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi13_7_step"
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
        "suspension_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_8a3_rejects_given_suspension_isomorphism():
  data = build_phase73_8a3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "suspension_isomorphism_step"
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
        "pi13_7_step"
      ],
      given_step,
    ),
  ) is None



