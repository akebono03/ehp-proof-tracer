from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from toda_rules import (
  TodaHopfInvariantIsomorphismStatement,
  TodaLemma54Statement,
  toda_59_eta3_nu4_inference_rule,
  toda_prop58_eta3_nu4_hopf_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_7_data():
  phase60_9 = (
    build_phase60_9_data()
  )

  phase65_3 = (
    build_phase65_3_data()
  )

  phase68_3 = (
    build_phase68_3_data()
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  equation57_step = (
    phase65_3[
      "equation57_step"
    ]
  )

  hopf_isomorphism_step = (
    phase68_3[
      "hopf_isomorphism_step"
    ]
  )

  hopf_rule = (
    toda_prop58_eta3_nu4_hopf_inference_rule()
  )

  final_rule = (
    toda_59_eta3_nu4_inference_rule()
  )

  rules = (
    hopf_rule,
    final_rule,
  )

  premise_steps = (
    lemma54_step,
    equation57_step,
    hopf_isomorphism_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  eta_6 = HomotopyElement(
    name="η₆",
    dimension=6,
    source=7,
    target=6,
    generator=GeneratorSymbol(
      family="η",
      index=6,
    ),
  )

  eta3_nu4 = Composition(
    left=eta_3,
    right=nu_4,
  )

  nu_prime_eta6 = Composition(
    left=nu_prime,
    right=eta_6,
  )

  eta5_squared = Composition(
    left=eta_5,
    right=eta_6,
  )

  expected_hopf = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta3_nu4,
    ),
    rhs=eta5_squared,
    relation_type=RelationType.EQUALITY,
  )

  hopf_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf
    )
  )

  expected_final = Relation(
    lhs=eta3_nu4,
    rhs=nu_prime_eta6,
    relation_type=RelationType.EQUALITY,
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase60_9": phase60_9,
    "phase65_3": phase65_3,
    "phase68_3": phase68_3,
    "lemma54_step": lemma54_step,
    "equation57_step": (
      equation57_step
    ),
    "hopf_isomorphism_step": (
      hopf_isomorphism_step
    ),
    "hopf_rule": hopf_rule,
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "eta_3": eta_3,
    "nu_4": nu_4,
    "nu_prime": nu_prime,
    "eta_5": eta_5,
    "eta_6": eta_6,
    "eta3_nu4": eta3_nu4,
    "nu_prime_eta6": (
      nu_prime_eta6
    ),
    "eta5_squared": (
      eta5_squared
    ),
    "expected_hopf": (
      expected_hopf
    ),
    "hopf_step": hopf_step,
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_7_reuses_derived_lemma54():
  data = build_phase68_7_data()

  assert isinstance(
    data[
      "lemma54_step"
    ].conclusion,
    TodaLemma54Statement,
  )

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_7_reuses_derived_equation57():
  data = build_phase68_7_data()

  assert (
    data[
      "equation57_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_7_reuses_derived_hopf_isomorphism():
  data = build_phase68_7_data()

  assert isinstance(
    data[
      "hopf_isomorphism_step"
    ].conclusion,
    TodaHopfInvariantIsomorphismStatement,
  )

  assert (
    data[
      "hopf_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_7_hopf_isomorphism_is_pi7_3_to_pi7_5():
  data = build_phase68_7_data()

  assert (
    data[
      "hopf_isomorphism_step"
    ].conclusion.map
    == TodaHopfInvariantMap(
      source_group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=5,
      ),
    )
  )


def test_phase68_7_derives_h_eta3_nu4():
  data = build_phase68_7_data()

  assert (
    data[
      "hopf_step"
    ].conclusion
    == data[
      "expected_hopf"
    ]
  )

  assert (
    data[
      "hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_7_h_eta3_nu4_is_eta5_squared():
  data = build_phase68_7_data()

  assert (
    data[
      "hopf_step"
    ].conclusion.rhs
    == data[
      "eta5_squared"
    ]
  )


def test_phase68_7_hopf_step_uses_only_lemma54():
  data = build_phase68_7_data()

  assert (
    data[
      "hopf_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
    )
  )


def test_phase68_7_equation57_has_same_hopf_value():
  data = build_phase68_7_data()

  assert (
    data[
      "equation57_step"
    ].conclusion.rhs
    == data[
      "hopf_step"
    ].conclusion.rhs
  )


def test_phase68_7_derives_toda59():
  data = build_phase68_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_7_toda59_left_is_eta3_nu4():
  data = build_phase68_7_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == data[
      "eta3_nu4"
    ]
  )


def test_phase68_7_toda59_right_is_nu_prime_eta6():
  data = build_phase68_7_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == data[
      "nu_prime_eta6"
    ]
  )


def test_phase68_7_final_uses_exact_three_dependencies():
  data = build_phase68_7_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "hopf_isomorphism_step"
      ],
      data[
        "hopf_step"
      ],
      data[
        "equation57_step"
      ],
    )
  )


def test_phase68_7_rejects_given_lemma54():
  data = build_phase68_7_data()

  given = ProofStep(
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
      "hopf_rule"
    ],
    (
      given,
    ),
  ) is None


def test_phase68_7_rejects_given_hopf_isomorphism():
  data = build_phase68_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "hopf_isomorphism_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      given,
      data[
        "hopf_step"
      ],
      data[
        "equation57_step"
      ],
    ),
  ) is None


def test_phase68_7_rejects_given_eta3_nu4_hopf():
  data = build_phase68_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "hopf_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "hopf_isomorphism_step"
      ],
      given,
      data[
        "equation57_step"
      ],
    ),
  ) is None


def test_phase68_7_rejects_given_equation57():
  data = build_phase68_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "equation57_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "hopf_isomorphism_step"
      ],
      data[
        "hopf_step"
      ],
      given,
    ),
  ) is None


def test_phase68_7_final_result_not_present_initially():
  data = build_phase68_7_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase68_7_final_result_is_not_given():
  data = build_phase68_7_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase68_7_reaches_fixed_point():
  data = build_phase68_7_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


