from dataclasses import replace
from functools import lru_cache

from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
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
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase70_pi11_6_delta_iota13 import (
  build_phase70_8_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
  toda_prop59_higher_five_stem_zero_transport_inference_rule,
  toda_prop59_pi12_7_concrete_exactness_inference_rule,
  toda_prop59_pi12_7_suspension_surjective_inference_rule,
  toda_prop59_pi12_7_zero_inference_rule,
  toda_prop59_pi13_13_delta_surjective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_9_data():
  phase70_8 = (
    build_phase70_8_data()
  )

  pi11_6_step = (
    phase70_8[
      "final_step"
    ]
  )

  pi13_13_step = (
    phase70_8[
      "pi13_13_step"
    ]
  )

  pi13_13 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  pi11_6 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  pi12_7 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=7,
  )

  pi12_13 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=13,
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi13_13,
      middle_term=pi11_6,
      target_term=pi12_7,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  delta_e_window_step = ProofStep(
    conclusion=delta_e_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  e_h_window = (
    TodaEHPExactnessWindow(
      source_term=pi11_6,
      middle_term=pi12_7,
      target_term=pi12_13,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  e_h_window_step = ProofStep(
    conclusion=e_h_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi12_13_zero_step = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=pi12_13,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n = ScalarSymbol(
    name="n",
  )

  phase46 = (
    build_phase46_representative_result(
      n=7,
      k=5,
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

  n_ge_7_step = ProofStep(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=n,
        right=7,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop59_pi12_7_concrete_exactness_inference_rule()
  )

  delta_surjective_rule = (
    toda_prop59_pi13_13_delta_surjective_inference_rule()
  )

  suspension_surjective_rule = (
    toda_prop59_pi12_7_suspension_surjective_inference_rule()
  )

  pi12_7_zero_rule = (
    toda_prop59_pi12_7_zero_inference_rule()
  )

  higher_zero_rule = (
    toda_prop59_higher_five_stem_zero_transport_inference_rule()
  )

  delta_e_exactness_match = (
    find_inference_match(
      exactness_rule,
      (
        delta_e_window_step,
      ),
    )
  )

  assert (
    delta_e_exactness_match
    is not None
  )

  delta_e_exactness_step = (
    apply_inference_match(
      delta_e_exactness_match
    )
  )

  e_h_exactness_match = (
    find_inference_match(
      exactness_rule,
      (
        e_h_window_step,
      ),
    )
  )

  assert (
    e_h_exactness_match
    is not None
  )

  e_h_exactness_step = (
    apply_inference_match(
      e_h_exactness_match
    )
  )

  delta_surjective_match = (
    find_inference_match(
      delta_surjective_rule,
      (
        pi13_13_step,
        pi11_6_step,
      ),
    )
  )

  assert (
    delta_surjective_match
    is not None
  )

  delta_surjective_step = (
    apply_inference_match(
      delta_surjective_match
    )
  )

  suspension_surjective_match = (
    find_inference_match(
      suspension_surjective_rule,
      (
        pi12_13_zero_step,
        e_h_exactness_step,
      ),
    )
  )

  assert (
    suspension_surjective_match
    is not None
  )

  suspension_surjective_step = (
    apply_inference_match(
      suspension_surjective_match
    )
  )

  pi12_7_zero_match = (
    find_inference_match(
      pi12_7_zero_rule,
      (
        delta_surjective_step,
        delta_e_exactness_step,
        suspension_surjective_step,
      ),
    )
  )

  assert (
    pi12_7_zero_match
    is not None
  )

  pi12_7_zero_step = (
    apply_inference_match(
      pi12_7_zero_match
    )
  )

  higher_zero_match = (
    find_inference_match(
      higher_zero_rule,
      (
        pi12_7_zero_step,
        stable_isomorphism_step,
        n_ge_7_step,
      ),
    )
  )

  assert (
    higher_zero_match
    is not None
  )

  higher_zero_step = (
    apply_inference_match(
      higher_zero_match
    )
  )

  expected_delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=delta_e_window,
    )
  )

  expected_e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=e_h_window,
    )
  )

  expected_delta_surjective = (
    TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi13_13,
        target_group=pi11_6,
      ),
    )
  )

  expected_suspension_surjective = (
    TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=pi11_6,
        target_group=pi12_7,
      ),
    )
  )

  expected_pi12_7_zero = (
    TodaPrimaryGroupZeroStatement(
      group=pi12_7,
    )
  )

  expected_higher_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=5,
        ),
        sphere_dimension=n,
      )
    )
  )

  assert (
    delta_e_exactness_step.conclusion
    == expected_delta_e_exactness
  )

  assert (
    e_h_exactness_step.conclusion
    == expected_e_h_exactness
  )

  assert (
    delta_surjective_step.conclusion
    == expected_delta_surjective
  )

  assert (
    suspension_surjective_step.conclusion
    == expected_suspension_surjective
  )

  assert (
    pi12_7_zero_step.conclusion
    == expected_pi12_7_zero
  )

  assert (
    higher_zero_step.conclusion
    == expected_higher_zero
  )

  return {
    "phase70_8": phase70_8,
    "pi11_6_step": pi11_6_step,
    "pi13_13_step": pi13_13_step,
    "pi13_13": pi13_13,
    "pi11_6": pi11_6,
    "pi12_7": pi12_7,
    "pi12_13": pi12_13,
    "delta_e_window": delta_e_window,
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "e_h_window": e_h_window,
    "e_h_window_step": (
      e_h_window_step
    ),
    "pi12_13_zero_step": (
      pi12_13_zero_step
    ),
    "n": n,
    "phase46": phase46,
    "stable_isomorphism_step": (
      stable_isomorphism_step
    ),
    "n_ge_7_step": n_ge_7_step,
    "exactness_rule": exactness_rule,
    "delta_surjective_rule": (
      delta_surjective_rule
    ),
    "suspension_surjective_rule": (
      suspension_surjective_rule
    ),
    "pi12_7_zero_rule": (
      pi12_7_zero_rule
    ),
    "higher_zero_rule": (
      higher_zero_rule
    ),
    "delta_e_exactness_match": (
      delta_e_exactness_match
    ),
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "e_h_exactness_match": (
      e_h_exactness_match
    ),
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "delta_surjective_match": (
      delta_surjective_match
    ),
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "suspension_surjective_match": (
      suspension_surjective_match
    ),
    "suspension_surjective_step": (
      suspension_surjective_step
    ),
    "pi12_7_zero_match": (
      pi12_7_zero_match
    ),
    "pi12_7_zero_step": (
      pi12_7_zero_step
    ),
    "higher_zero_match": (
      higher_zero_match
    ),
    "higher_zero_step": (
      higher_zero_step
    ),
    "expected_delta_e_exactness": (
      expected_delta_e_exactness
    ),
    "expected_e_h_exactness": (
      expected_e_h_exactness
    ),
    "expected_delta_surjective": (
      expected_delta_surjective
    ),
    "expected_suspension_surjective": (
      expected_suspension_surjective
    ),
    "expected_pi12_7_zero": (
      expected_pi12_7_zero
    ),
    "expected_higher_zero": (
      expected_higher_zero
    ),
  }


def test_phase70_9_reuses_derived_pi11_6():
  data = build_phase70_9_data()

  assert (
    data[
      "pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi11_6_step"
    ].conclusion.lhs
    == data[
      "pi11_6"
    ]
  )


def test_phase70_9_reuses_foundational_pi13_13():
  data = build_phase70_9_data()

  assert (
    data[
      "pi13_13_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert isinstance(
    data[
      "pi13_13_step"
    ].conclusion.rhs,
    FreeCyclicGroup,
  )


def test_phase70_9_structural_exactness_windows_remain_given():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_e_window_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "e_h_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase70_9_derives_delta_e_exactness():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_e_exactness_step"
    ].conclusion
    == data[
      "expected_delta_e_exactness"
    ]
  )

  assert (
    data[
      "delta_e_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_derives_e_h_exactness():
  data = build_phase70_9_data()

  assert (
    data[
      "e_h_exactness_step"
    ].conclusion
    == data[
      "expected_e_h_exactness"
    ]
  )

  assert (
    data[
      "e_h_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_delta_surjective_matches():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_surjective_match"
    ]
    is not None
  )


def test_phase70_9_derives_delta_surjective():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_surjective_step"
    ].conclusion
    == data[
      "expected_delta_surjective"
    ]
  )

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_delta_surjective_uses_exact_dependencies():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_surjective_step"
    ].premises
    == (
      data[
        "pi13_13_step"
      ],
      data[
        "pi11_6_step"
      ],
    )
  )


def test_phase70_9_pi12_13_zero_is_foundational_given():
  data = build_phase70_9_data()

  assert (
    data[
      "pi12_13_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=data[
        "pi12_13"
      ],
    )
  )

  assert (
    data[
      "pi12_13_zero_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase70_9_suspension_surjective_matches():
  data = build_phase70_9_data()

  assert (
    data[
      "suspension_surjective_match"
    ]
    is not None
  )


def test_phase70_9_derives_suspension_surjective():
  data = build_phase70_9_data()

  assert (
    data[
      "suspension_surjective_step"
    ].conclusion
    == data[
      "expected_suspension_surjective"
    ]
  )

  assert (
    data[
      "suspension_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_suspension_surjective_uses_exact_dependencies():
  data = build_phase70_9_data()

  assert (
    data[
      "suspension_surjective_step"
    ].premises
    == (
      data[
        "pi12_13_zero_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase70_9_pi12_7_zero_matches():
  data = build_phase70_9_data()

  assert (
    data[
      "pi12_7_zero_match"
    ]
    is not None
  )


def test_phase70_9_derives_pi12_7_zero():
  data = build_phase70_9_data()

  assert (
    data[
      "pi12_7_zero_step"
    ].conclusion
    == data[
      "expected_pi12_7_zero"
    ]
  )

  assert (
    data[
      "pi12_7_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_pi12_7_zero_uses_exact_dependencies():
  data = build_phase70_9_data()

  assert (
    data[
      "pi12_7_zero_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
    )
  )


def test_phase70_9_reuses_toda45_isomorphism():
  data = build_phase70_9_data()

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


def test_phase70_9_toda45_source_is_pi12_7():
  data = build_phase70_9_data()

  source = (
    data[
      "stable_isomorphism_step"
    ].conclusion
    .map
    .source_group
  )

  assert (
    source
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=7,
        right=5,
      ),
      sphere_dimension=7,
    )
  )


def test_phase70_9_toda45_target_is_pi_n_plus_5_n():
  data = build_phase70_9_data()

  target = (
    data[
      "stable_isomorphism_step"
    ].conclusion
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
        right=5,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase70_9_toda45_exponent_is_n_minus_7():
  data = build_phase70_9_data()

  assert (
    data[
      "stable_isomorphism_step"
    ].conclusion
    .map
    .exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=7,
      ),
    )
  )


def test_phase70_9_range_is_n_at_least_7():
  data = build_phase70_9_data()

  assert (
    data[
      "n_ge_7_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=7,
    )
  )

  assert (
    data[
      "n_ge_7_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase70_9_higher_zero_matches():
  data = build_phase70_9_data()

  assert (
    data[
      "higher_zero_match"
    ]
    is not None
  )


def test_phase70_9_derives_higher_zero():
  data = build_phase70_9_data()

  assert (
    data[
      "higher_zero_step"
    ].conclusion
    == data[
      "expected_higher_zero"
    ]
  )

  assert (
    data[
      "higher_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_9_final_is_pi_n_plus_5_n_zero():
  data = build_phase70_9_data()

  assert (
    data[
      "higher_zero_step"
    ].conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=5,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase70_9_higher_zero_uses_exact_three_dependencies():
  data = build_phase70_9_data()

  assert (
    data[
      "higher_zero_step"
    ].premises
    == (
      data[
        "pi12_7_zero_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_7_step"
      ],
    )
  )


def test_phase70_9_delta_surjective_rejects_inference_pi13_13():
  data = build_phase70_9_data()

  derived = ProofStep(
    conclusion=(
      data[
        "pi13_13_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_surjective_rule"
    ],
    (
      derived,
      data[
        "pi11_6_step"
      ],
    ),
  ) is None


def test_phase70_9_delta_surjective_rejects_given_pi11_6():
  data = build_phase70_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi11_6_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_surjective_rule"
    ],
    (
      data[
        "pi13_13_step"
      ],
      given,
    ),
  ) is None


def test_phase70_9_suspension_surjective_rejects_inference_zero_target():
  data = build_phase70_9_data()

  derived = ProofStep(
    conclusion=(
      data[
        "pi12_13_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "suspension_surjective_rule"
    ],
    (
      derived,
      data[
        "e_h_exactness_step"
      ],
    ),
  ) is None


def test_phase70_9_pi12_7_zero_rejects_given_delta_surjective():
  data = build_phase70_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_surjective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "pi12_7_zero_rule"
    ],
    (
      given,
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
    ),
  ) is None


def test_phase70_9_pi12_7_zero_rejects_given_surjectivity():
  data = build_phase70_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "suspension_surjective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "pi12_7_zero_rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      given,
    ),
  ) is None


def test_phase70_9_higher_zero_rejects_given_pi12_7_zero():
  data = build_phase70_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi12_7_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "higher_zero_rule"
    ],
    (
      given,
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_7_step"
      ],
    ),
  ) is None


def test_phase70_9_higher_zero_rejects_given_toda45():
  data = build_phase70_9_data()

  given = ProofStep(
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
      "higher_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      given,
      data[
        "n_ge_7_step"
      ],
    ),
  ) is None


def test_phase70_9_higher_zero_rejects_wrong_range():
  data = build_phase70_9_data()

  wrong_range = ProofStep(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=data[
          "n"
        ],
        right=8,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "higher_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase70_9_exactness_rejects_wrong_window():
  data = build_phase70_9_data()

  wrong_window = replace(
    data[
      "delta_e_window"
    ],
    source_term=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=13,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "exactness_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase70_9_higher_zero_rejects_wrong_toda45_source():
  data = build_phase70_9_data()

  wrong_statement = replace(
    data[
      "stable_isomorphism_step"
    ].conclusion,
    map=replace(
      data[
        "stable_isomorphism_step"
      ].conclusion.map,
      source_group=TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=7,
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
      "higher_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      wrong_step,
      data[
        "n_ge_7_step"
      ],
    ),
  ) is None


def test_phase70_9_higher_zero_rejects_wrong_toda45_exponent():
  data = build_phase70_9_data()

  wrong_statement = replace(
    data[
      "stable_isomorphism_step"
    ].conclusion,
    map=replace(
      data[
        "stable_isomorphism_step"
      ].conclusion.map,
      exponent=ScalarSum(
        left=data[
          "n"
        ],
        right=ScalarProduct(
          left=-1,
          right=8,
        ),
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
      "higher_zero_rule"
    ],
    (
      data[
        "pi12_7_zero_step"
      ],
      wrong_step,
      data[
        "n_ge_7_step"
      ],
    ),
  ) is None


def test_phase70_9_results_are_not_given():
  data = build_phase70_9_data()

  assert (
    data[
      "pi12_7_zero_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "higher_zero_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_9_final_not_present_initially():
  data = build_phase70_9_data()

  initial_steps = (
    data[
      "pi11_6_step"
    ],
    data[
      "pi13_13_step"
    ],
    data[
      "delta_e_window_step"
    ],
    data[
      "e_h_window_step"
    ],
    data[
      "pi12_13_zero_step"
    ],
    data[
      "stable_isomorphism_step"
    ],
    data[
      "n_ge_7_step"
    ],
  )

  assert (
    data[
      "expected_higher_zero"
    ]
    not in tuple(
      step.conclusion
      for step in initial_steps
    )
  )


def test_phase70_9_uses_staged_one_shot_inference():
  data = build_phase70_9_data()

  assert (
    data[
      "delta_e_exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "e_h_exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "delta_surjective_match"
    ]
    is not None
  )

  assert (
    data[
      "suspension_surjective_match"
    ]
    is not None
  )

  assert (
    data[
      "pi12_7_zero_match"
    ]
    is not None
  )

  assert (
    data[
      "higher_zero_match"
    ]
    is not None
  )


