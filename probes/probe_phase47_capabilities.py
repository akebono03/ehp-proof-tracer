from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
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
  TodaProp44IsomorphismStatement,
  toda_prop44_isomorphism_inference_rule,
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

  if isinstance(
    expression,
    Multiple,
  ):
    return (
      str(
        expression.coefficient
      )
      + element_text(
        expression.expression
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
      "relation lhs must be "
      "a MapApplication"
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


def theorem_text(
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


def build_phase47_representative_result(
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

  source_group = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n_minus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=two_n_minus_one,
      ),
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
  )

  theorem_rule = (
    toda_prop44_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      theorem_rule,
      premise_steps,
    )
  )

  theorem_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        TodaProp44IsomorphismStatement,
      )
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
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "premise_steps": premise_steps,
    "theorem_rule": theorem_rule,
    "result": result,
    "theorem_steps": theorem_steps,
  }


def print_phase47_premises(
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


def print_phase47_map(
  representative,
):
  print()
  print("Decomposition map:")
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


def print_phase47_theorem_result(
  representative,
):
  print()
  print(
    "Toda Proposition 4.4 "
    "theorem result:"
  )
  print()

  for step in representative[
    "theorem_steps"
  ]:
    print(
      " ",
      theorem_text(
        step.conclusion
      ),
    )


def print_phase47_provenance(
  representative,
):
  print()
  print_separator()
  print("Provenance / fixed point")
  print_separator()
  print()

  print(
    "theorem isomorphism count =",
    len(
      representative[
        "theorem_steps"
      ]
    ),
  )

  print(
    "premise count =",
    len(
      representative[
        "premise_steps"
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
    "fixed point =",
    (
      representative[
        "result"
      ].termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase47_boundary():
  print()
  print_separator()
  print("Phase 47 boundary")
  print_separator()
  print()

  print("Implemented:")
  print(
    "  TodaPrimaryGroup membership"
  )
  print(
    "  symbolic decomposition source / target"
  )
  print(
    "  Toda Proposition 4.4 decomposition map"
  )
  print(
    "  positive / negative Hopf applicability"
  )
  print(
    "  instance-aware Proposition 4.4 isomorphism theorem"
  )
  print(
    "  applicability / invalid-case guards"
  )
  print(
    "  theorem provenance"
  )
  print()

  print("Still outside Phase 47:")
  print(
    "  generic IsomorphismStatement bridge"
  )
  print(
    "  generic InjectiveMapStatement consequence"
  )
  print(
    "  E injectivity consequence"
  )
  print(
    "  generic map-property type generalization"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 47 capability demonstration"
  )

  representative = (
    build_phase47_representative_result()
  )

  print_phase47_premises(
    representative
  )

  print_phase47_map(
    representative
  )

  print_phase47_theorem_result(
    representative
  )

  print_phase47_provenance(
    representative
  )

  print_phase47_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()


