from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarSum,
  ScalarSymbol,
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
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
  toda_lemma57_e2_eta2_alpha_composition_inference_rule,
  toda_lemma57_e2_eta2_alpha_zero_inference_rule,
  toda_prop51_eta4_twice_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase67_3_data():
  phase55 = (
    build_phase55_representative_result()
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  i = ScalarSymbol(
    name="i",
  )

  i_plus_two = ScalarSum(
    left=i,
    right=2,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
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

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  e2_alpha = IteratedSuspension(
    expression=alpha,
    exponent=2,
  )

  hypothesis = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=e2_alpha,
      source_group=TodaPrimaryGroup(
        group_dimension=i_plus_two,
        sphere_dimension=5,
      ),
    )
  )

  hypothesis_step = ProofStep(
    conclusion=hypothesis,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=eta_4,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  composition_relation = Relation(
    lhs=IteratedSuspension(
      expression=Composition(
        left=eta_2,
        right=alpha,
      ),
      exponent=2,
    ),
    rhs=Composition(
      left=eta_4,
      right=e2_alpha,
    ),
    relation_type=RelationType.EQUALITY,
  )

  final_zero = Relation(
    lhs=IteratedSuspension(
      expression=Composition(
        left=eta_2,
        right=alpha,
      ),
      exponent=2,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  eta4_rule = (
    toda_prop51_eta4_twice_zero_inference_rule()
  )

  composition_rule = (
    toda_lemma57_e2_eta2_alpha_composition_inference_rule()
  )

  zero_rule = (
    toda_lemma57_e2_eta2_alpha_zero_inference_rule()
  )

  rules = (
    eta4_rule,
    composition_rule,
    zero_rule,
  )

  premise_steps = (
    prop51_step,
    hypothesis_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  return {
    "phase55": phase55,
    "prop51_step": prop51_step,
    "i": i,
    "i_plus_two": i_plus_two,
    "alpha": alpha,
    "eta_2": eta_2,
    "eta_4": eta_4,
    "e2_alpha": e2_alpha,
    "hypothesis": hypothesis,
    "hypothesis_step": hypothesis_step,
    "eta4_zero": eta4_zero,
    "composition_relation": (
      composition_relation
    ),
    "final_zero": final_zero,
    "eta4_rule": eta4_rule,
    "composition_rule": (
      composition_rule
    ),
    "zero_rule": zero_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
  }


def test_phase67_3_reuses_derived_prop51():
  data = build_phase67_3_data()

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_3_hypothesis_is_given():
  data = build_phase67_3_data()

  assert isinstance(
    data[
      "hypothesis_step"
    ].conclusion,
    TodaLemma57TwoIota5ImageMembershipStatement,
  )

  assert (
    data[
      "hypothesis_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase67_3_derives_two_eta4_zero():
  data = build_phase67_3_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "eta4_zero"
    ]
    in conclusions
  )


def test_phase67_3_derives_double_suspension_composition_relation():
  data = build_phase67_3_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "composition_relation"
    ]
    in conclusions
  )


def test_phase67_3_composition_relation_preserves_hypothesis_provenance():
  data = build_phase67_3_data()

  step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "composition_relation"
      ]
    )
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.premises
    == (
      data[
        "hypothesis_step"
      ],
    )
  )


def test_phase67_3_composition_rule_accepts_inference_hypothesis():
  data = build_phase67_3_data()

  inference_hypothesis = ProofStep(
    conclusion=data[
      "hypothesis"
    ],
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "composition_rule"
    ],
    (
      inference_hypothesis,
    ),
  ) is not None


def test_phase67_3_zero_rule_accepts_inference_hypothesis():
  data = build_phase67_3_data()

  inference_hypothesis = ProofStep(
    conclusion=data[
      "hypothesis"
    ],
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  composition_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "composition_relation"
      ]
    )
  )

  eta4_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "eta4_zero"
      ]
    )
  )

  assert find_inference_match(
    data[
      "zero_rule"
    ],
    (
      inference_hypothesis,
      composition_step,
      eta4_step,
    ),
  ) is not None


def test_phase67_3_composition_rule_rejects_wrong_source_group():
  data = build_phase67_3_data()

  wrong_hypothesis = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=data[
        "e2_alpha"
      ],
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=data[
            "i"
          ],
          right=3,
        ),
        sphere_dimension=5,
      ),
    )
  )

  wrong_step = ProofStep(
    conclusion=wrong_hypothesis,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "composition_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase67_3_derives_e2_eta2_alpha_zero():
  data = build_phase67_3_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "final_zero"
    ]
    in conclusions
  )


def test_phase67_3_final_zero_preserves_three_dependencies():
  data = build_phase67_3_data()

  eta4_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "eta4_zero"
      ]
    )
  )

  composition_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "composition_relation"
      ]
    )
  )

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "final_zero"
      ]
    )
  )

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    final_step.premises
    == (
      data[
        "hypothesis_step"
      ],
      composition_step,
      eta4_step,
    )
  )


def test_phase67_3_zero_rule_rejects_given_eta4_zero():
  data = build_phase67_3_data()

  composition_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "composition_relation"
      ]
    )
  )

  given_eta4_zero = ProofStep(
    conclusion=data[
      "eta4_zero"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "zero_rule"
    ],
    (
      data[
        "hypothesis_step"
      ],
      composition_step,
      given_eta4_zero,
    ),
  ) is None


def test_phase67_3_zero_rule_rejects_given_composition_relation():
  data = build_phase67_3_data()

  eta4_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "eta4_zero"
      ]
    )
  )

  given_composition = ProofStep(
    conclusion=data[
      "composition_relation"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "zero_rule"
    ],
    (
      data[
        "hypothesis_step"
      ],
      given_composition,
      eta4_step,
    ),
  ) is None


def test_phase67_3_zero_rule_rejects_wrong_eta4_zero():
  data = build_phase67_3_data()

  composition_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "composition_relation"
      ]
    )
  )

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=Multiple(
        coefficient=4,
        expression=data[
          "eta_4"
        ],
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "zero_rule"
    ],
    (
      data[
        "hypothesis_step"
      ],
      composition_step,
      wrong_zero,
    ),
  ) is None


def test_phase67_3_final_result_is_not_given():
  data = build_phase67_3_data()

  final_steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "final_zero"
      ]
    )
  )

  assert len(
    final_steps
  ) == 1

  assert (
    final_steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_3_reaches_fixed_point():
  data = build_phase67_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 2
  )


