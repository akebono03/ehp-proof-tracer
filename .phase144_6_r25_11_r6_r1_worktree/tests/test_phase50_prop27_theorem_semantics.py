from typing import (
  get_type_hints,
)

from expression import (
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  WhiteheadProduct,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp27HopfInvariantUpToSignStatement,
  toda_prop27_iota2_whitehead_hopf_invariant_inference_rule,
)


def build_phase50_3_data():
  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  whitehead_product = (
    WhiteheadProduct(
      left=iota_2,
      right=iota_2,
    )
  )

  positive_value = Multiple(
    coefficient=2,
    expression=iota_3,
  )

  statement = (
    TodaProp27HopfInvariantUpToSignStatement(
      argument=whitehead_product,
      positive_value=positive_value,
    )
  )

  return {
    "iota_2": iota_2,
    "iota_3": iota_3,
    "whitehead_product": (
      whitehead_product
    ),
    "positive_value": (
      positive_value
    ),
    "statement": statement,
  }


def build_phase50_3_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "whitehead_product"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase50_3_statement_argument_uses_expression():
  type_hints = get_type_hints(
    TodaProp27HopfInvariantUpToSignStatement
  )

  assert type_hints[
    "argument"
  ] is Expression


def test_phase50_3_statement_positive_value_uses_expression():
  type_hints = get_type_hints(
    TodaProp27HopfInvariantUpToSignStatement
  )

  assert type_hints[
    "positive_value"
  ] is Expression


def test_phase50_3_statement_preserves_whitehead_product():
  data = build_phase50_3_data()

  assert data[
    "statement"
  ].argument == (
    data[
      "whitehead_product"
    ]
  )


def test_phase50_3_statement_preserves_positive_two_iota_3():
  data = build_phase50_3_data()

  assert data[
    "statement"
  ].positive_value == (
    Multiple(
      coefficient=2,
      expression=data[
        "iota_3"
      ],
    )
  )


def test_phase50_3_statement_is_not_sign_specific_relation():
  data = build_phase50_3_data()

  assert not isinstance(
    data[
      "statement"
    ],
    Relation,
  )


def test_phase50_3_rule_requires_whitehead_product():
  rule = (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 1

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is WhiteheadProduct
  )


def test_phase50_3_valid_iota2_whitehead_square_matches():
  data = build_phase50_3_data()

  assert find_inference_match(
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    build_phase50_3_steps(
      data
    ),
  ) is not None


def test_phase50_3_valid_iota2_whitehead_square_derives_statement():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "statement"
  ] in conclusions


def test_phase50_3_derived_statement_preserves_argument():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  assert derived.conclusion.argument == (
    data[
      "whitehead_product"
    ]
  )


def test_phase50_3_derived_statement_preserves_two_iota3():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  assert derived.conclusion.positive_value == (
    data[
      "positive_value"
    ]
  )


def test_phase50_3_wrong_whitehead_generator_is_rejected():
  data = build_phase50_3_data()

  wrong_iota = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  wrong_whitehead = WhiteheadProduct(
    left=wrong_iota,
    right=wrong_iota,
  )

  steps = (
    ProofStep(
      conclusion=wrong_whitehead,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    steps,
  ) is None


def test_phase50_3_mixed_whitehead_product_is_rejected():
  data = build_phase50_3_data()

  mixed_whitehead = WhiteheadProduct(
    left=data[
      "iota_2"
    ],
    right=data[
      "iota_3"
    ],
  )

  steps = (
    ProofStep(
      conclusion=mixed_whitehead,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    steps,
  ) is None


def test_phase50_3_missing_whitehead_product_is_rejected():
  assert find_inference_match(
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    (),
  ) is None


def test_phase50_3_derived_statement_is_inference():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase50_3_derived_statement_preserves_premise():
  data = build_phase50_3_data()

  steps = build_phase50_3_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  assert derived.premises == steps


def test_phase50_3_derived_statement_preserves_inference_rule():
  data = build_phase50_3_data()

  rule = (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      build_phase50_3_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  assert derived.inference_rule == (
    rule
  )


def test_phase50_3_reaches_fixed_point_in_one_round():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase50_3_does_not_derive_sign_specific_relation():
  data = build_phase50_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
      build_phase50_3_steps(
        data
      ),
    )
  )

  derived_relations = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
    )
  )

  assert derived_relations == ()



