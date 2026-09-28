from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from test_phase71_toda512_n4_delta_injective import (
  build_phase71_2_data,
)
from test_phase71_toda512_n5_delta_injective import (
  build_phase71_3_data,
)
from test_phase71_toda512_n6_delta_injective import (
  build_phase71_4_data,
)
from toda_rules import (
  Toda512DeltaInjectivityStatement,
  TodaDeltaInjectiveStatement,
  toda_512_delta_injectivity_integration_inference_rule,
  toda_512_delta_injectivity_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase71_5_data():
  phase71_2 = (
    build_phase71_2_data()
  )

  phase71_3 = (
    build_phase71_3_data()
  )

  phase71_4 = (
    build_phase71_4_data()
  )

  n4_step = (
    phase71_2[
      "final_step"
    ]
  )

  n5_step = (
    phase71_3[
      "final_step"
    ]
  )

  n6_step = (
    phase71_4[
      "final_step"
    ]
  )

  expected_statement = (
    Toda512DeltaInjectivityStatement(
      n4_injectivity=(
        n4_step.conclusion
      ),
      n5_injectivity=(
        n5_step.conclusion
      ),
      n6_injectivity=(
        n6_step.conclusion
      ),
      literature_statements=(
        toda_512_delta_injectivity_literature_statements()
      ),
    )
  )

  rule = (
    toda_512_delta_injectivity_integration_inference_rule()
  )

  premise_steps = (
    n4_step,
    n5_step,
    n6_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert match is not None

  integration_step = (
    apply_inference_match(
      match
    )
  )

  assert (
    integration_step.conclusion
    == expected_statement
  )

  return {
    "phase71_2": phase71_2,
    "phase71_3": phase71_3,
    "phase71_4": phase71_4,
    "n4_step": n4_step,
    "n5_step": n5_step,
    "n6_step": n6_step,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "integration_step": (
      integration_step
    ),
  }


def test_phase71_5_reuses_three_derived_injectivity_results():
  data = build_phase71_5_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in (
      data[
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    )
  )


def test_phase71_5_n4_is_expected_map():
  data = build_phase71_5_data()

  assert (
    data[
      "n4_step"
    ].conclusion
    == TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=4,
        ),
      )
    )
  )


def test_phase71_5_n5_is_expected_map():
  data = build_phase71_5_data()

  assert (
    data[
      "n5_step"
    ].conclusion
    == TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=11,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
      )
    )
  )


def test_phase71_5_n6_is_expected_map():
  data = build_phase71_5_data()

  assert (
    data[
      "n6_step"
    ].conclusion
    == TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      )
    )
  )


def test_phase71_5_rule_matches_three_cases():
  data = build_phase71_5_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase71_5_derives_aggregate():
  data = build_phase71_5_data()

  assert isinstance(
    data[
      "integration_step"
    ].conclusion,
    Toda512DeltaInjectivityStatement,
  )

  assert (
    data[
      "integration_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_5_aggregate_preserves_n4_object():
  data = build_phase71_5_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .n4_injectivity
    is data[
      "n4_step"
    ].conclusion
  )


def test_phase71_5_aggregate_preserves_n5_object():
  data = build_phase71_5_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .n5_injectivity
    is data[
      "n5_step"
    ].conclusion
  )


def test_phase71_5_aggregate_preserves_n6_object():
  data = build_phase71_5_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .n6_injectivity
    is data[
      "n6_step"
    ].conclusion
  )


def test_phase71_5_uses_exact_three_dependencies():
  data = build_phase71_5_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    )
  )


def test_phase71_5_has_toda512_literature():
  data = build_phase71_5_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert (
    len(
      literature
    )
    == 1
  )

  assert (
    literature[
      0
    ].reference.label
    == "Toda (5.12)"
  )

  assert (
    literature[
      0
    ].reference.locator
    == "Equation (5.12)"
  )

  assert (
    literature[
      0
    ].reference.author
    == "H. Toda"
  )

  assert (
    literature[
      0
    ].reference.year
    == 1962
  )


def test_phase71_5_literature_contains_three_case_scope():
  data = build_phase71_5_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert (
    "pi_(n+7)^(2n+1)"
    in statement
  )

  assert (
    "pi_(n+5)^n"
    in statement
  )

  assert (
    "n=4, 5, 6"
    in statement
  )


def test_phase71_5_rejects_given_n4():
  data = build_phase71_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "n4_step"
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
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    ),
  ) is None


def test_phase71_5_rejects_given_n5():
  data = build_phase71_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "n5_step"
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
        "n4_step"
      ],
      given,
      data[
        "n6_step"
      ],
    ),
  ) is None


def test_phase71_5_rejects_given_n6():
  data = build_phase71_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "n6_step"
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
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      given,
    ),
  ) is None


def test_phase71_5_rejects_wrong_n4_map():
  data = build_phase71_5_data()

  wrong_statement = (
    replace(
      data[
        "n4_step"
      ].conclusion,
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=4,
        ),
      ),
    )
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
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    ),
  ) is None


def test_phase71_5_rejects_wrong_n5_map():
  data = build_phase71_5_data()

  wrong_statement = (
    replace(
      data[
        "n5_step"
      ].conclusion,
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=10,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
      ),
    )
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
        "n4_step"
      ],
      wrong_step,
      data[
        "n6_step"
      ],
    ),
  ) is None


def test_phase71_5_rejects_wrong_n6_map():
  data = build_phase71_5_data()

  wrong_statement = (
    replace(
      data[
        "n6_step"
      ].conclusion,
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=6,
        ),
      ),
    )
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
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase71_5_final_is_not_given():
  data = build_phase71_5_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


