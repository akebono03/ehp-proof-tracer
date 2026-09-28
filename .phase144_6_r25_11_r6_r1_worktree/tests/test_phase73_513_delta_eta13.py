from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Zero,
)
from homotopy_groups import (
  HomotopyGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from test_phase60_toda54_t0_bridge import (
  build_phase60_5_data,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase72r8_corrected_lemma510_integration import (
  build_phase72r8_data,
)
from test_phase73_513_delta_nu9 import (
  build_phase73_6a_data,
)
from toda_rules import (
  Toda54BracketUpToSignStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaDeltaImageUpToSignStatement,
  TodaLemma510BracketModuloStatement,
  TodaProp51FiniteDimensionalStatement,
  toda_eta_family_definition_statement,
  toda_prop511_513_delta_eta13_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_6c_data():
  phase55 = (
    build_phase55_5_integration()
  )

  phase60 = (
    build_phase60_5_data()
  )

  phase62 = (
    build_phase62_6_data()
  )

  phase72r8 = (
    build_phase72r8_data()
  )

  phase73_6a = (
    build_phase73_6a_data()
  )

  prop51_step = (
    phase55[
      "integration_steps"
    ][
      0
    ]
  )

  toda54_step = (
    phase60[
      "t0_step"
    ]
  )

  toda55_step = (
    phase62[
      "integration_step"
    ]
  )

  lemma510_step = (
    phase72r8[
      "final_step"
    ]
  )

  delta_nu9_step = (
    phase73_6a[
      "final_step"
    ]
  )

  eta_13 = (
    toda_eta_family_definition_statement(
      13
    ).element
  )

  expected_statement = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=eta_13,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  rule = (
    toda_prop511_513_delta_eta13_zero_inference_rule()
  )

  premise_steps = (
    lemma510_step,
    prop51_step,
    toda54_step,
    toda55_step,
    delta_nu9_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
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

  return {
    "phase55": phase55,
    "phase60": phase60,
    "phase62": phase62,
    "phase72r8": phase72r8,
    "phase73_6a": phase73_6a,
    "prop51_step": prop51_step,
    "toda54_step": toda54_step,
    "toda55_step": toda55_step,
    "lemma510_step": lemma510_step,
    "delta_nu9_step": (
      delta_nu9_step
    ),
    "eta_13": eta_13,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
  }


def test_phase73_6c_reuses_corrected_lemma510():
  data = build_phase73_6c_data()

  statement = (
    data[
      "lemma510_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaLemma510BracketModuloStatement,
  )

  assert (
    data[
      "lemma510_step"
    ].rule
    == ProofRule.INFERENCE
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


def test_phase73_6c_does_not_use_primary_lemma510_ambient_group():
  data = build_phase73_6c_data()

  assert (
    data[
      "lemma510_step"
    ].conclusion
    .ambient_group
    != TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase73_6c_reuses_derived_prop51():
  data = build_phase73_6c_data()

  assert isinstance(
    data[
      "prop51_step"
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6c_reuses_derived_toda54_t0():
  data = build_phase73_6c_data()

  assert isinstance(
    data[
      "toda54_step"
    ].conclusion,
    Toda54BracketUpToSignStatement,
  )

  assert (
    data[
      "toda54_step"
    ].conclusion
    .bracket
    .index
    is None
  )

  assert (
    data[
      "toda54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6c_reuses_derived_toda55():
  data = build_phase73_6c_data()

  assert isinstance(
    data[
      "toda55_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "toda55_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6c_reuses_first_513_relation():
  data = build_phase73_6c_data()

  assert isinstance(
    data[
      "delta_nu9_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_nu9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6c_eta13_has_expected_typing():
  data = build_phase73_6c_data()

  eta_13 = (
    data[
      "eta_13"
    ]
  )

  assert (
    eta_13.dimension
    == 13
  )

  assert (
    eta_13.source
    == 14
  )

  assert (
    eta_13.target
    == 13
  )

  assert (
    eta_13.generator
    == GeneratorSymbol(
      family="η",
      index=13,
    )
  )


def test_phase73_6c_rule_matches_dependencies():
  data = build_phase73_6c_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase73_6c_derives_delta_eta13_zero():
  data = build_phase73_6c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6c_final_lhs_is_delta_eta13():
  data = build_phase73_6c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "eta_13"
      ],
    )
  )


def test_phase73_6c_final_rhs_is_zero():
  data = build_phase73_6c_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.rhs
    == Zero()
  )

  assert (
    relation.relation_type
    == RelationType.ZERO
  )


def test_phase73_6c_final_uses_exact_five_dependencies():
  data = build_phase73_6c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "lemma510_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    )
  )


def test_phase73_6c_rejects_given_lemma510():
  data = build_phase73_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "lemma510_step"
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
      given,
      data[
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6c_rejects_primary_lemma510_ambient_group():
  data = build_phase73_6c_data()

  statement = (
    data[
      "lemma510_step"
    ].conclusion
  )

  wrong_statement = replace(
    statement,
    ambient_group=TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
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
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6c_rejects_wrong_lemma510_modulus():
  data = build_phase73_6c_data()

  statement = (
    data[
      "lemma510_step"
    ].conclusion
  )

  wrong_statement = replace(
    statement,
    modulus=4,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
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
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6c_rejects_given_toda54():
  data = build_phase73_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda54_step"
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
        "lemma510_step"
      ],
      data[
        "prop51_step"
      ],
      given,
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6c_rejects_given_toda55():
  data = build_phase73_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda55_step"
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
        "lemma510_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      given,
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6c_rejects_given_first_513_relation():
  data = build_phase73_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_nu9_step"
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
        "lemma510_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      given,
    ),
  ) is None


def test_phase73_6c_rejects_wrong_first_513_coefficient():
  data = build_phase73_6c_data()

  statement = (
    data[
      "delta_nu9_step"
    ].conclusion
  )

  wrong_statement = replace(
    statement,
    positive_value=Multiple(
      coefficient=4,
      expression=(
        statement
        .positive_value
        .expression
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "lemma510_step"
      ],
      data[
        "prop51_step"
      ],
      data[
        "toda54_step"
      ],
      data[
        "toda55_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase73_6c_final_is_not_given():
  data = build_phase73_6c_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


