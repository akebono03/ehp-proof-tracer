from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
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


def inequality_text(
  statement,
):
  return (
    scalar_text(
      statement.left
    )
    + " ≥ "
    + scalar_text(
      statement.right
    )
  )


def suspension_map_text(
  suspension_map,
):
  return (
    "E^("
    + scalar_text(
      suspension_map.exponent
    )
    + "): "
    + group_text(
      suspension_map.source_group
    )
    + " → "
    + group_text(
      suspension_map.target_group
    )
  )


def theorem_text(
  statement,
):
  if not isinstance(
    statement,
    Toda45IsomorphismStatement,
  ):
    raise TypeError(
      "statement must be a "
      "Toda45IsomorphismStatement"
    )

  return (
    suspension_map_text(
      statement.map
    )
    + " is isomorphism"
  )


def build_phase46_representative_result(
  n=None,
  k=None,
  m=None,
):
  if n is None:
    n = ScalarSymbol(
      name="n",
    )

  if k is None:
    k = ScalarSymbol(
      name="k",
    )

  if m is None:
    m = ScalarSymbol(
      name="m",
    )

  stable_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=ScalarSum(
        left=k,
        right=2,
      ),
    )
  )

  suspension_range = (
    ScalarGreaterEqualStatement(
      left=m,
      right=n,
    )
  )

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=m,
        right=ScalarProduct(
          left=-1,
          right=n,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=k,
        ),
        sphere_dimension=n,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=m,
          right=k,
        ),
        sphere_dimension=m,
      ),
    )
  )

  premise_steps = (
    ProofStep(
      conclusion=stable_range,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_range,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  theorem_rule = (
    toda_45_isomorphism_inference_rule()
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
        Toda45IsomorphismStatement,
      )
    )
  )

  return {
    "n": n,
    "k": k,
    "m": m,
    "stable_range": stable_range,
    "suspension_range": suspension_range,
    "suspension_map": suspension_map,
    "premise_steps": premise_steps,
    "theorem_rule": theorem_rule,
    "result": result,
    "theorem_steps": theorem_steps,
  }


def print_phase46_premises(
  representative,
):
  print()
  print_separator()
  print("Toda (4.5) stable-range premises")
  print_separator()
  print()

  print(
    " ",
    inequality_text(
      representative[
        "stable_range"
      ]
    ),
  )

  print(
    " ",
    inequality_text(
      representative[
        "suspension_range"
      ]
    ),
  )


def print_phase46_map(
  representative,
):
  print()
  print("Iterated suspension map:")
  print()

  print(
    " ",
    suspension_map_text(
      representative[
        "suspension_map"
      ]
    ),
  )


def print_phase46_theorem_result(
  representative,
):
  print()
  print("Toda (4.5) theorem result:")
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


def print_phase46_provenance(
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


def print_phase46_boundary():
  print()
  print_separator()
  print("Phase 46 completion boundary")
  print_separator()
  print()

  print("Implemented:")
  print(
    "  symbolic stable-range premises"
  )
  print(
    "  Toda iterated suspension map"
  )
  print(
    "  source / target Toda groups"
  )
  print(
    "  Toda (4.5) instance-aware isomorphism theorem"
  )
  print(
    "  applicability / invalid-case guards"
  )
  print(
    "  theorem provenance"
  )
  print()

  print("Still outside Phase 46:")
  print(
    "  generic IsomorphismStatement bridge"
  )
  print(
    "  generic injectivity consequence"
  )
  print(
    "  Toda Proposition 4.4"
  )
  print(
    "  general symbolic inequality solver"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 46 capability demonstration"
  )

  representative = (
    build_phase46_representative_result()
  )

  print_phase46_premises(
    representative
  )

  print_phase46_map(
    representative
  )

  print_phase46_theorem_result(
    representative
  )

  print_phase46_provenance(
    representative
  )

  print_phase46_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()
