from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Suspension,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FreeCyclicGroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
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
  find_applicable_inference_rules,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
)
from toda_rules import (
  toda_lemma41_even_nonzero_case_inference_rule,
  toda_lemma41_even_zero_case_inference_rule,
  toda_lemma41_even_zero_h_alpha_inference_rule,
  toda_lemma41_even_zero_suspension_primary_inference_rule,
  toda_lemma41_odd_case_inference_rule,
)


def print_separator():
  print("=" * 72)


def scalar_text(
  value,
):
  if isinstance(
    value,
    int,
  ):
    return str(
      value
    )

  if isinstance(
    value,
    ScalarSymbol,
  ):
    return value.name

  if isinstance(
    value,
    ScalarProduct,
  ):
    left = scalar_text(
      value.left
    )

    right = scalar_text(
      value.right
    )

    return (
      f"{left}{right}"
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    left = scalar_text(
      value.left
    )

    if (
      isinstance(
        value.right,
        int,
      )
      and value.right < 0
    ):
      return (
        f"{left}{value.right}"
      )

    right = scalar_text(
      value.right
    )

    return (
      f"{left}+{right}"
    )

  return str(
    value
  )


def expression_text(
  expression,
):
  if isinstance(
    expression,
    HomotopyElement,
  ):
    generator = (
      expression.generator
    )

    if (
      generator is not None
      and generator.family == "ι"
      and generator.index is not None
    ):
      return (
        "ι_{"
        + scalar_text(
          generator.index
        )
        + "}"
      )

    return expression.name

  if isinstance(
    expression,
    WhiteheadProduct,
  ):
    return (
      "["
      + expression_text(
        expression.left
      )
      + ","
      + expression_text(
        expression.right
      )
      + "]"
    )

  if isinstance(
    expression,
    MapApplication,
  ):
    return (
      expression.map.name
      + "("
      + expression_text(
        expression.expression
      )
      + ")"
    )

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      "E"
      + expression_text(
        expression.expression
      )
    )

  if isinstance(
    expression,
    Zero,
  ):
    return "0"

  return str(
    expression
  )


def group_text(
  group,
):
  if isinstance(
    group,
    TodaPrimaryGroup,
  ):
    return (
      "π_{"
      + scalar_text(
        group.group_dimension
      )
      + "}^{"
      + scalar_text(
        group.sphere_dimension
      )
      + "}"
    )

  if isinstance(
    group,
    PrimaryComponent,
  ):
    return (
      "π_{"
      + scalar_text(
        group.group_dimension
      )
      + "}(S^{"
      + scalar_text(
        group.sphere_dimension
      )
      + "};"
      + str(
        group.prime
      )
      + ")"
    )

  if isinstance(
    group,
    FreeCyclicGroup,
  ):
    return (
      "Z{"
      + expression_text(
        group.generator
      )
      + "}"
    )

  if isinstance(
    group,
    DirectSumGroup,
  ):
    return " ⊕ ".join(
      group_text(
        summand
      )
      for summand
      in group.summands
    )

  return str(
    group
  )


def relation_text(
  relation,
):
  if (
    relation.relation_type
    == RelationType.ZERO
  ):
    symbol = "="
  elif (
    relation.relation_type
    == RelationType.INEQUALITY
  ):
    symbol = "!="
  elif (
    relation.relation_type
    == RelationType.EQUALITY
  ):
    symbol = "="
  else:
    symbol = (
      relation.relation_type.value
    )

  if isinstance(
    relation.lhs,
    (
      TodaPrimaryGroup,
      PrimaryComponent,
      FreeCyclicGroup,
      DirectSumGroup,
    ),
  ):
    lhs = group_text(
      relation.lhs
    )
  else:
    lhs = expression_text(
      relation.lhs
    )

  if isinstance(
    relation.rhs,
    (
      TodaPrimaryGroup,
      PrimaryComponent,
      FreeCyclicGroup,
      DirectSumGroup,
    ),
  ):
    rhs = group_text(
      relation.rhs
    )
  else:
    rhs = expression_text(
      relation.rhs
    )

  return (
    f"{lhs} {symbol} {rhs}"
  )


def primary_component_membership_text(
  statement,
):
  if not isinstance(
    statement,
    PrimaryComponentMembershipStatement,
  ):
    raise TypeError(
      "statement must be a "
      "PrimaryComponentMembershipStatement"
    )

  return (
    expression_text(
      statement.element
    )
    + " ∈ "
    + group_text(
      statement.component
    )
  )


def premise_text(
  step,
):
  conclusion = (
    step.conclusion
  )

  if isinstance(
    conclusion,
    OddScalarStatement,
  ):
    return (
      scalar_text(
        conclusion.scalar
      )
      + " odd"
    )

  if isinstance(
    conclusion,
    EvenScalarStatement,
  ):
    return (
      scalar_text(
        conclusion.scalar
      )
      + " even"
    )

  if isinstance(
    conclusion,
    Relation,
  ):
    return relation_text(
      conclusion
    )

  return str(
    conclusion
  )


def build_symbolic_whitehead_relation(
  n,
  relation_type,
):
  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  return Relation(
    lhs=WhiteheadProduct(
      left=iota_n_minus_one,
      right=iota_n_minus_one,
    ),
    rhs=Zero(),
    relation_type=relation_type,
  )


def find_case_derived_step(
  result,
):
  return next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        TodaPrimaryGroup,
      )
    )
  )


def find_zero_case_alpha_condition_steps(
  result,
):
  h_step = next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      is EHP_H_MAP
    )
  )

  primary_membership_step = next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        PrimaryComponentMembershipStatement,
      )
    )
  )

  return (
    h_step,
    primary_membership_step,
  )


def build_phase44_representative_cases():
  n = ScalarSymbol(
    name="n",
  )

  rules = (
    toda_lemma41_odd_case_inference_rule(),
    toda_lemma41_even_nonzero_case_inference_rule(),
    toda_lemma41_even_zero_case_inference_rule(),
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nonzero_step = ProofStep(
    conclusion=(
      build_symbolic_whitehead_relation(
        n,
        RelationType.INEQUALITY,
      )
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  zero_step = ProofStep(
    conclusion=(
      build_symbolic_whitehead_relation(
        n,
        RelationType.ZERO,
      )
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  scenarios = (
    (
      "odd",
      (
        odd_step,
      ),
    ),
    (
      "even_nonzero",
      (
        even_step,
        nonzero_step,
      ),
    ),
    (
      "even_zero",
      (
        even_step,
        zero_step,
      ),
    ),
  )

  cases = {}

  for name, premises in scenarios:
    applicable_rules = (
      find_applicable_inference_rules(
        rules,
        premises,
      )
    )

    result = (
      run_inference_until_stable_with_history(
        rules,
        premises,
      )
    )

    derived_step = (
      find_case_derived_step(
        result
      )
    )

    cases[
      name
    ] = {
      "premises": premises,
      "applicable_rules": (
        applicable_rules
      ),
      "result": result,
      "derived_step": (
        derived_step
      ),
    }

  zero_case_rules = (
    rules[
      2
    ],
    toda_lemma41_even_zero_h_alpha_inference_rule(),
    toda_lemma41_even_zero_suspension_primary_inference_rule(),
  )

  zero_case_premises = cases[
    "even_zero"
  ][
    "premises"
  ]

  zero_case_applicable_rules = (
    find_applicable_inference_rules(
      zero_case_rules,
      zero_case_premises,
    )
  )

  zero_case_result = (
    run_inference_until_stable_with_history(
      zero_case_rules,
      zero_case_premises,
    )
  )

  (
    h_alpha_step,
    primary_membership_step,
  ) = (
    find_zero_case_alpha_condition_steps(
      zero_case_result
    )
  )

  cases[
    "even_zero"
  ][
    "zero_case_rules"
  ] = zero_case_rules

  cases[
    "even_zero"
  ][
    "zero_case_applicable_rules"
  ] = (
    zero_case_applicable_rules
  )

  cases[
    "even_zero"
  ][
    "zero_case_result"
  ] = zero_case_result

  cases[
    "even_zero"
  ][
    "alpha_condition_steps"
  ] = (
    h_alpha_step,
    primary_membership_step,
  )

  return {
    "n": n,
    "rules": rules,
    "cases": cases,
  }


def print_phase44_case(
  title,
  case,
):
  print()
  print_separator()
  print(title)
  print_separator()
  print()

  print("Premises:")

  for premise in case[
    "premises"
  ]:
    print(
      " ",
      premise_text(
        premise
      ),
    )

  print()

  print(
    "Applicable rule =",
    case[
      "applicable_rules"
    ][
      0
    ].name,
  )

  print()

  print(
    "Conclusion:"
  )

  print(
    " ",
    relation_text(
      case[
        "derived_step"
      ].conclusion
    ),
  )

  print()

  print(
    "provenance premise count =",
    len(
      case[
        "derived_step"
      ].premises
    ),
  )

  print(
    "fixed point =",
    (
      case[
        "result"
      ].termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase44_alpha_conditions(
  case,
):
  (
    h_alpha_step,
    primary_membership_step,
  ) = case[
    "alpha_condition_steps"
  ]

  print()
  print("α conditions:")

  print(
    " ",
    relation_text(
      h_alpha_step.conclusion
    ),
  )

  print(
    " ",
    primary_component_membership_text(
      primary_membership_step.conclusion
    ),
  )

  print()

  print(
    "α-condition applicable rule count =",
    len(
      case[
        "zero_case_applicable_rules"
      ]
    ),
  )

  print(
    "α-condition derived step count =",
    len(
      case[
        "zero_case_result"
      ].round_results[
        0
      ].new_steps
    ),
  )

  print(
    "α-condition fixed point =",
    (
      case[
        "zero_case_result"
      ].termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase44_applicability(
  result,
):
  print()
  print_separator()
  print("Case applicability / exclusivity")
  print_separator()
  print()

  cases = result[
    "cases"
  ]

  for name in (
    "odd",
    "even_nonzero",
    "even_zero",
  ):
    applicable = cases[
      name
    ][
      "applicable_rules"
    ]

    print(
      name,
      "applicable rule count =",
      len(
        applicable
      ),
    )


def print_phase44_boundary():
  print()
  print_separator()
  print("Phase 44 completion boundary")
  print_separator()
  print()

  print("Implemented:")
  print(
    "  n odd case semantics"
  )
  print(
    "  n even + Whitehead nonzero case semantics"
  )
  print(
    "  n even + Whitehead zero case semantics"
  )
  print(
    "  zero-case H(α)=ι_(2n-1) condition"
  )
  print(
    "  zero-case Eα primary membership condition"
  )
  print(
    "  structural symbolic generator indexing"
  )
  print(
    "  structural free cyclic / direct-sum groups"
  )
  print(
    "  PrimaryComponent membership representation"
  )
  print()

  print("Still outside Phase 44:")
  print(
    "  automatic Whitehead-product zero inference"
  )
  print(
    "  automatic Whitehead-product nonzero inference"
  )
  print(
    "  ZERO / INEQUALITY contradiction detection"
  )
  print(
    "  Whitehead-product bilinearity"
  )
  print(
    "  Whitehead-product antisymmetry"
  )
  print(
    "  automatic alpha existence / uniqueness machinery"
  )
  print(
    "  Toda Proposition 4.2 semantics"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 44 capability demonstration"
  )

  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  print_phase44_case(
    "Toda Lemma 4.1: n odd",
    cases[
      "odd"
    ],
  )

  print_phase44_case(
    (
      "Toda Lemma 4.1: "
      "n even + Whitehead nonzero"
    ),
    cases[
      "even_nonzero"
    ],
  )

  print_phase44_case(
    (
      "Toda Lemma 4.1: "
      "n even + Whitehead zero"
    ),
    cases[
      "even_zero"
    ],
  )

  print_phase44_alpha_conditions(
    cases[
      "even_zero"
    ]
  )

  print_phase44_applicability(
    result
  )

  print_phase44_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()


