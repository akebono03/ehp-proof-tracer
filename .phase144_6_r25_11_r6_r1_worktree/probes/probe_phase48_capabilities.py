from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
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
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SuspensionInjectiveStatement,
  toda_prop44_first_summand_restriction_inference_rule,
  toda_prop44_isomorphism_inference_rule,
  toda_prop44_suspension_injective_inference_rule,
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

    if (
      value.left == -1
    ):
      return (
        "-"
        + right
      )

    return (
      left
      + right
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    left = scalar_text(
      value.left
    )

    right = scalar_text(
      value.right
    )

    if isinstance(
      value.right,
      ScalarProduct,
    ):
      if (
        value.right.left
        == -1
      ):
        return (
          left
          + "-"
          + scalar_text(
            value.right.right
          )
        )

    if (
      isinstance(
        value.right,
        int,
      )
      and value.right < 0
    ):
      return (
        left
        + str(
          value.right
        )
      )

    return (
      left
      + "+"
      + right
    )

  return str(
    value
  )


def group_text(
  group,
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


def direct_sum_text(
  group,
):
  return " ⊕ ".join(
    group_text(
      summand
    )
    for summand in group.summands
  )


def element_text(
  expression,
):
  if isinstance(
    expression,
    HomotopyElement,
  ):
    return expression.name

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      "E"
      + element_text(
        expression.expression
      )
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      element_text(
        expression.left
      )
      + "∘"
      + element_text(
        expression.right
      )
    )

  if isinstance(
    expression,
    Sum,
  ):
    return (
      element_text(
        expression.left
      )
      + " + "
      + element_text(
        expression.right
      )
    )

  return str(
    expression
  )


def membership_text(
  statement,
):
  return (
    element_text(
      statement.element
    )
    + " ∈ "
    + group_text(
      statement.group
    )
  )


def hopf_relation_text(
  relation,
):
  if not isinstance(
    relation.lhs,
    MapApplication,
  ):
    raise TypeError(
      "relation lhs must be a "
      "MapApplication"
    )

  return (
    relation.lhs.map.name
    + "("
    + element_text(
      relation.lhs.expression
    )
    + ") = "
    + element_text(
      relation.rhs
    )
  )


def decomposition_map_text(
  decomposition_map,
):
  return (
    "Φ: "
    + direct_sum_text(
      decomposition_map.source_group
    )
    + " → "
    + group_text(
      decomposition_map.target_group
    )
  )


def decomposition_formula_text(
  decomposition_map,
):
  return (
    "Φ("
    + element_text(
      decomposition_map.beta
    )
    + ","
    + element_text(
      decomposition_map.gamma
    )
    + ") = "
    + element_text(
      decomposition_map.formula
    )
  )


def suspension_map_text(
  suspension_map,
):
  return (
    "E: "
    + group_text(
      suspension_map.source_group
    )
    + " → "
    + group_text(
      suspension_map.target_group
    )
  )


def isomorphism_text(
  statement,
):
  if not isinstance(
    statement,
    TodaProp44IsomorphismStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaProp44IsomorphismStatement"
    )

  return (
    decomposition_map_text(
      statement.map
    )
    + " is isomorphism"
  )


def restriction_text(
  statement,
):
  if not isinstance(
    statement,
    TodaProp44FirstSummandRestrictionStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaProp44FirstSummandRestrictionStatement"
    )

  first_summand = (
    statement
    .decomposition_map
    .source_group
    .summands[
      0
    ]
  )

  return (
    "Φ|_{"
    + group_text(
      first_summand
    )
    + "} = "
    + suspension_map_text(
      statement.suspension_map
    )
  )


def injectivity_text(
  statement,
):
  if not isinstance(
    statement,
    TodaProp44SuspensionInjectiveStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaProp44SuspensionInjectiveStatement"
    )

  return (
    suspension_map_text(
      statement.map
    )
    + " is injective"
  )


def build_phase48_representative_result(
  i=None,
  n=None,
):
  if i is None:
    i = ScalarSymbol(
      name="i",
    )

  if n is None:
    n = ScalarSymbol(
      name="n",
    )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i,
  )

  iota = HomotopyElement(
    name="ι_(2n-1)",
    dimension=two_n_minus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=two_n_minus_one,
    ),
  )

  membership = (
    TodaPrimaryGroupMembershipStatement(
      element=alpha,
      group=TodaPrimaryGroup(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
      ),
    )
  )

  hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    ),
    rhs=iota,
    relation_type=RelationType.EQUALITY,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=Composition(
      left=alpha,
      right=gamma,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=alpha,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  suspension_map = TodaSuspensionMap(
    source_group=first_summand,
    target_group=target_group,
  )

  premise_steps = (
    ProofStep(
      conclusion=membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=hopf_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=decomposition_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  isomorphism_rule = (
    toda_prop44_isomorphism_inference_rule()
  )

  restriction_rule = (
    toda_prop44_first_summand_restriction_inference_rule()
  )

  injectivity_rule = (
    toda_prop44_suspension_injective_inference_rule()
  )

  rules = (
    isomorphism_rule,
    restriction_rule,
    injectivity_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  isomorphism_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  restriction_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44FirstSummandRestrictionStatement,
    )
  )

  injectivity_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  return {
    "i": i,
    "n": n,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "iota": iota,
    "membership": membership,
    "hopf_relation": hopf_relation,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "suspension_map": suspension_map,
    "premise_steps": premise_steps,
    "isomorphism_rule": (
      isomorphism_rule
    ),
    "restriction_rule": (
      restriction_rule
    ),
    "injectivity_rule": (
      injectivity_rule
    ),
    "rules": rules,
    "result": result,
    "isomorphism_steps": (
      isomorphism_steps
    ),
    "restriction_steps": (
      restriction_steps
    ),
    "injectivity_steps": (
      injectivity_steps
    ),
  }


def print_phase48_premises(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Proposition 4.4 premises"
  )
  print_separator()
  print()

  print(
    " ",
    membership_text(
      representative[
        "membership"
      ]
    ),
  )

  print(
    " ",
    hopf_relation_text(
      representative[
        "hopf_relation"
      ]
    ),
  )

  print()
  print(
    "Decomposition map:"
  )
  print()

  print(
    " ",
    decomposition_map_text(
      representative[
        "decomposition_map"
      ]
    ),
  )

  print(
    " ",
    decomposition_formula_text(
      representative[
        "decomposition_map"
      ]
    ),
  )

  print()
  print(
    "Suspension map instance:"
  )
  print()

  print(
    " ",
    suspension_map_text(
      representative[
        "suspension_map"
      ]
    ),
  )


def print_phase48_inference(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 48 inference"
  )
  print_separator()
  print()

  print(
    "Toda Proposition 4.4 "
    "isomorphism:"
  )
  print()

  for step in representative[
    "isomorphism_steps"
  ]:
    print(
      " ",
      isomorphism_text(
        step.conclusion
      ),
    )

  print()
  print(
    "First-summand restriction:"
  )
  print()

  for step in representative[
    "restriction_steps"
  ]:
    print(
      " ",
      restriction_text(
        step.conclusion
      ),
    )

  print()
  print(
    "Suspension injectivity "
    "consequence:"
  )
  print()

  for step in representative[
    "injectivity_steps"
  ]:
    print(
      " ",
      injectivity_text(
        step.conclusion
      ),
    )


def print_phase48_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / fixed point"
  )
  print_separator()
  print()

  print(
    "given premise count =",
    len(
      representative[
        "premise_steps"
      ]
    ),
  )

  print(
    "isomorphism count =",
    len(
      representative[
        "isomorphism_steps"
      ]
    ),
  )

  print(
    "restriction count =",
    len(
      representative[
        "restriction_steps"
      ]
    ),
  )

  print(
    "injectivity count =",
    len(
      representative[
        "injectivity_steps"
      ]
    ),
  )

  print(
    "derived round count =",
    representative[
      "result"
    ].round_count,
  )

  print(
    "round 1 new step count =",
    len(
      representative[
        "result"
      ].round_results[
        0
      ].new_steps
    ),
  )

  print(
    "round 2 new step count =",
    len(
      representative[
        "result"
      ].round_results[
        1
      ].new_steps
    ),
  )

  print(
    "fixed point =",
    (
      representative[
        "result"
      ].termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase48_boundary():
  print()
  print_separator()
  print(
    "Phase 48 boundary"
  )
  print_separator()
  print()

  print("Implemented:")
  print(
    "  instance-aware suspension map"
  )
  print(
    "  Proposition 4.4 first-summand restriction"
  )
  print(
    "  Proposition 4.4 suspension injectivity consequence"
  )
  print(
    "  cross-instance rejection"
  )
  print(
    "  theorem provenance"
  )
  print(
    "  fixed-point end-to-end inference"
  )
  print()

  print(
    "Still outside Phase 48:"
  )
  print(
    "  generic InjectiveMapStatement bridge"
  )
  print(
    "  generic map-property type generalization"
  )
  print(
    "  general direct-sum inclusion machinery"
  )
  print(
    "  automatic equality reflection through TodaSuspensionMap"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 48 capability demonstration"
  )

  representative = (
    build_phase48_representative_result()
  )

  print_phase48_premises(
    representative
  )

  print_phase48_inference(
    representative
  )

  print_phase48_provenance(
    representative
  )

  print_phase48_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


