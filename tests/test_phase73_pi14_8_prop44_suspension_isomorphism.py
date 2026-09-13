from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
  toda_prop511_pi14_8_prop44_zero_second_summand_suspension_isomorphism_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_8a2_data():
  pi13_7 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=7,
  )

  pi14_15 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=15,
  )

  pi14_8 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=8,
  )

  beta = HomotopyElement(
    name="β",
    dimension=13,
    source=13,
    target=7,
    generator=GeneratorSymbol(
      family="β",
    ),
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=14,
    source=14,
    target=15,
    generator=GeneratorSymbol(
      family="γ",
    ),
  )

  sigma_8 = HomotopyElement(
    name="σ₈",
    dimension=8,
    source=15,
    target=8,
    generator=GeneratorSymbol(
      family="σ",
      index=8,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          pi13_7,
          pi14_15,
        ),
      ),
      target_group=pi14_8,
      alpha=sigma_8,
      beta=beta,
      gamma=gamma,
      formula=Sum(
        left=Suspension(
          expression=beta,
        ),
        right=Composition(
          left=sigma_8,
          right=gamma,
        ),
      ),
    )
  )

  prop44_statement = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  prop44_step = ProofStep(
    conclusion=prop44_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  zero_statement = (
    TodaPrimaryGroupZeroStatement(
      group=pi14_15,
    )
  )

  zero_step = ProofStep(
    conclusion=zero_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  expected_map = TodaSuspensionMap(
    source_group=pi13_7,
    target_group=pi14_8,
  )

  expected_isomorphism = (
    TodaSuspensionIsomorphismStatement(
      map=expected_map,
    )
  )

  rule = (
    toda_prop511_pi14_8_prop44_zero_second_summand_suspension_isomorphism_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      prop44_step,
      zero_step,
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

  return {
    "pi13_7": pi13_7,
    "pi14_15": pi14_15,
    "pi14_8": pi14_8,
    "beta": beta,
    "gamma": gamma,
    "sigma_8": sigma_8,
    "decomposition_map": (
      decomposition_map
    ),
    "prop44_statement": (
      prop44_statement
    ),
    "prop44_step": prop44_step,
    "zero_statement": (
      zero_statement
    ),
    "zero_step": zero_step,
    "expected_map": (
      expected_map
    ),
    "expected_isomorphism": (
      expected_isomorphism
    ),
    "rule": rule,
    "final_step": final_step,
  }


def test_phase73_8a2_derives_expected_suspension_isomorphism():
  data = build_phase73_8a2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_isomorphism"
    ]
  )


def test_phase73_8a2_uses_inference_provenance():
  data = build_phase73_8a2_data()

  final_step = data[
    "final_step"
  ]

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    final_step.premises
    == (
      data[
        "prop44_step"
      ],
      data[
        "zero_step"
      ],
    )
  )


def test_phase73_8a2_suspension_map_has_expected_source():
  data = build_phase73_8a2_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .map
    .source_group
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=7,
    )
  )


def test_phase73_8a2_suspension_map_has_expected_target():
  data = build_phase73_8a2_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .map
    .target_group
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    )
  )


def test_phase73_8a2_rejects_wrong_zero_second_summand():
  data = build_phase73_8a2_data()

  wrong_zero_step = ProofStep(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=15,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "prop44_step"
      ],
      wrong_zero_step,
    ),
  )

  assert (
    match
    is None
  )


def test_phase73_8a2_rejects_wrong_target_group():
  data = build_phase73_8a2_data()

  wrong_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        data[
          "pi13_7"
        ],
        data[
          "pi14_15"
        ],
      ),
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    ),
    alpha=data[
      "sigma_8"
    ],
    beta=data[
      "beta"
    ],
    gamma=data[
      "gamma"
    ],
    formula=Sum(
      left=Suspension(
        expression=data[
          "beta"
        ],
      ),
      right=Composition(
        left=data[
          "sigma_8"
        ],
        right=data[
          "gamma"
        ],
      ),
    ),
  )

  wrong_prop44_step = ProofStep(
    conclusion=TodaProp44IsomorphismStatement(
      map=wrong_map,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_prop44_step,
      data[
        "zero_step"
      ],
    ),
  )

  assert (
    match
    is None
  )


def test_phase73_8a2_rejects_wrong_decomposition_formula():
  data = build_phase73_8a2_data()

  wrong_formula_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          data[
            "pi13_7"
          ],
          data[
            "pi14_15"
          ],
        ),
      ),
      target_group=data[
        "pi14_8"
      ],
      alpha=data[
        "sigma_8"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=Suspension(
        expression=data[
          "beta"
        ],
      ),
    )
  )

  wrong_prop44_step = ProofStep(
    conclusion=TodaProp44IsomorphismStatement(
      map=wrong_formula_map,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_prop44_step,
      data[
        "zero_step"
      ],
    ),
  )

  assert (
    match
    is None
  )

