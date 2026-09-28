from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Suspension,
  Zero,
)
from homotopy_groups import (
  TodaPrimaryGroup,
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
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
  toda_lemma45_n3_suspension_zero_reflection_inference_rule,
  toda_lemma57_e2_eta2_alpha_composition_inference_rule,
  toda_lemma57_e2_eta2_alpha_zero_inference_rule,
  toda_lemma57_nu_prime_hypothesis_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop51_eta4_twice_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase67_5_data():
  phase55 = (
    build_phase55_representative_result()
  )

  phase60_9 = (
    build_phase60_9_data()
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  nu5_definition = (
    toda_nu_family_definition_statement(
      5
    )
  )

  nu5_definition_step = ProofStep(
    conclusion=nu5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
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

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  expected_hypothesis = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    )
  )

  expected_final = Relation(
    lhs=Suspension(
      expression=Composition(
        left=eta_2,
        right=nu_prime,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  hypothesis_rule = (
    toda_lemma57_nu_prime_hypothesis_inference_rule()
  )

  eta4_rule = (
    toda_prop51_eta4_twice_zero_inference_rule()
  )

  composition_rule = (
    toda_lemma57_e2_eta2_alpha_composition_inference_rule()
  )

  double_zero_rule = (
    toda_lemma57_e2_eta2_alpha_zero_inference_rule()
  )

  reflection_rule = (
    toda_lemma45_n3_suspension_zero_reflection_inference_rule()
  )

  rules = (
    hypothesis_rule,
    eta4_rule,
    composition_rule,
    double_zero_rule,
    reflection_rule,
  )

  premise_steps = (
    prop51_step,
    lemma54_step,
    nu5_definition_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  hypothesis_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hypothesis
    )
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
    "phase55": phase55,
    "phase60_9": phase60_9,
    "prop51_step": prop51_step,
    "lemma54_step": lemma54_step,
    "nu5_definition": nu5_definition,
    "nu5_definition_step": (
      nu5_definition_step
    ),
    "nu_prime": nu_prime,
    "eta_2": eta_2,
    "expected_hypothesis": (
      expected_hypothesis
    ),
    "expected_final": expected_final,
    "hypothesis_rule": hypothesis_rule,
    "eta4_rule": eta4_rule,
    "composition_rule": (
      composition_rule
    ),
    "double_zero_rule": (
      double_zero_rule
    ),
    "reflection_rule": (
      reflection_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "hypothesis_step": hypothesis_step,
    "final_step": final_step,
  }


def test_phase67_5_reuses_derived_lemma54():
  data = build_phase67_5_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_5_uses_concrete_nu5_definition():
  data = build_phase67_5_data()

  assert (
    data[
      "nu5_definition"
    ]
    == toda_nu_family_definition_statement(
      5
    )
  )

  assert (
    data[
      "nu5_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase67_5_nu5_is_e_nu4():
  data = build_phase67_5_data()

  definition = data[
    "nu5_definition"
  ]

  assert (
    definition
    .iterated_suspension
    .exponent
    == 1
  )

  assert (
    definition
    .iterated_suspension
    .expression
    == data[
      "lemma54_step"
    ].conclusion.nu4
  )


def test_phase67_5_rule_matches_dependencies():
  data = build_phase67_5_data()

  assert find_inference_match(
    data[
      "hypothesis_rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      data[
        "nu5_definition_step"
      ],
    ),
  ) is not None


def test_phase67_5_derives_nu_prime_hypothesis():
  data = build_phase67_5_data()

  assert (
    data[
      "hypothesis_step"
    ].conclusion
    == data[
      "expected_hypothesis"
    ]
  )

  assert (
    data[
      "hypothesis_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_5_hypothesis_is_e2_nu_prime_in_pi8_s5_image():
  data = build_phase67_5_data()

  statement = (
    data[
      "hypothesis_step"
    ].conclusion
  )

  assert (
    statement.element
    == IteratedSuspension(
      expression=data[
        "nu_prime"
      ],
      exponent=2,
    )
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )


def test_phase67_5_hypothesis_provenance_is_exact():
  data = build_phase67_5_data()

  assert (
    data[
      "hypothesis_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
      data[
        "nu5_definition_step"
      ],
    )
  )


def test_phase67_5_rejects_given_lemma54():
  data = build_phase67_5_data()

  given_lemma54 = ProofStep(
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
      "hypothesis_rule"
    ],
    (
      given_lemma54,
      data[
        "nu5_definition_step"
      ],
    ),
  ) is None


def test_phase67_5_rejects_wrong_nu_family_index():
  data = build_phase67_5_data()

  wrong_definition_step = ProofStep(
    conclusion=(
      toda_nu_family_definition_statement(
        6
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hypothesis_rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      wrong_definition_step,
    ),
  ) is None


def test_phase67_5_rejects_wrong_lemma54_double_relation():
  data = build_phase67_5_data()

  lemma54 = (
    data[
      "lemma54_step"
    ].conclusion
  )

  wrong_lemma54 = replace(
    lemma54,
    double_suspension_relation=Relation(
      lhs=(
        lemma54
        .double_suspension_relation
        .lhs
      ),
      rhs=IteratedSuspension(
        expression=data[
          "nu_prime"
        ],
        exponent=3,
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_lemma54,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "hypothesis_rule"
    ],
    (
      wrong_step,
      data[
        "nu5_definition_step"
      ],
    ),
  ) is None


def test_phase67_5_general_lemma_reuses_derived_hypothesis():
  data = build_phase67_5_data()

  composition_match = (
    find_inference_match(
      data[
        "composition_rule"
      ],
      (
        data[
          "hypothesis_step"
        ],
      ),
    )
  )

  assert composition_match is not None


def test_phase67_5_derives_e_eta2_nu_prime_zero():
  data = build_phase67_5_data()

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


def test_phase67_5_final_is_not_initial_premise():
  data = build_phase67_5_data()

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


def test_phase67_5_final_depends_on_derived_hypothesis():
  data = build_phase67_5_data()

  seen_ids = set()

  def visit(
    step,
  ):
    for premise in step.premises:
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

      visit(
        premise
      )

  visit(
    data[
      "final_step"
    ]
  )

  assert (
    id(
      data[
        "hypothesis_step"
      ]
    )
    in seen_ids
  )


def test_phase67_5_final_depends_on_lemma54():
  data = build_phase67_5_data()

  seen_ids = set()

  def visit(
    step,
  ):
    for premise in step.premises:
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

      visit(
        premise
      )

  visit(
    data[
      "final_step"
    ]
  )

  assert (
    id(
      data[
        "lemma54_step"
      ]
    )
    in seen_ids
  )


def test_phase67_5_final_result_is_not_given():
  data = build_phase67_5_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase67_5_reaches_fixed_point():
  data = build_phase67_5_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


