from ehp_rules import (
  EHPZeroCompositionStatement,
  ehp_exactness_implies_zero_composition_inference_rule,
)
from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ExactnessStatement,
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  toda_prop42_delta_e_exactness_inference_rule,
  toda_prop42_e_h_exactness_inference_rule,
  toda_prop42_exactness_to_generic_inference_rule,
  toda_prop42_h_delta_exactness_inference_rule,
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
    return (
      scalar_text(
        value.left
      )
      + scalar_text(
        value.right
      )
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
        left
        + str(
          value.right
        )
      )

    return (
      left
      + "+"
      + scalar_text(
        value.right
      )
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


def window_text(
  window,
):
  return (
    group_text(
      window.source_term
    )
    + " -"
    + window.first_map.name
    + "→ "
    + group_text(
      window.middle_term
    )
    + " -"
    + window.second_map.name
    + "→ "
    + group_text(
      window.target_term
    )
  )


def exactness_text(
  statement,
):
  if not isinstance(
    statement,
    ExactnessStatement,
  ):
    raise TypeError(
      "statement must be an "
      "ExactnessStatement"
    )

  return (
    statement.first_map.name
    + "-"
    + statement.second_map.name
    + " exact"
  )


def zero_composition_text(
  statement,
):
  if not isinstance(
    statement,
    EHPZeroCompositionStatement,
  ):
    raise TypeError(
      "statement must be an "
      "EHPZeroCompositionStatement"
    )

  return (
    statement.second_map.name
    + "∘"
    + statement.first_map.name
    + " = 0"
  )


def build_phase45_symbolic_sequence(
  i,
  n,
):
  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  return TodaEHPSequence(
    terms=(
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n_plus_one,
      ),
    ),
    maps=(
      EHP_E_MAP,
      EHP_H_MAP,
      EHP_DELTA_MAP,
      EHP_E_MAP,
    ),
  )


def build_phase45_windows(
  sequence,
):
  return (
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        0
      ],
      middle_term=sequence.terms[
        1
      ],
      target_term=sequence.terms[
        2
      ],
      first_map=sequence.maps[
        0
      ],
      second_map=sequence.maps[
        1
      ],
    ),
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        1
      ],
      middle_term=sequence.terms[
        2
      ],
      target_term=sequence.terms[
        3
      ],
      first_map=sequence.maps[
        1
      ],
      second_map=sequence.maps[
        2
      ],
    ),
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        2
      ],
      middle_term=sequence.terms[
        3
      ],
      target_term=sequence.terms[
        4
      ],
      first_map=sequence.maps[
        2
      ],
      second_map=sequence.maps[
        3
      ],
    ),
  )


def build_phase45_representative_result(
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

  sequence = (
    build_phase45_symbolic_sequence(
      i,
      n,
    )
  )

  windows = (
    build_phase45_windows(
      sequence
    )
  )

  premise_steps = tuple(
    ProofStep(
      conclusion=window,
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for window in windows
  )

  theorem_rules = (
    toda_prop42_e_h_exactness_inference_rule(),
    toda_prop42_h_delta_exactness_inference_rule(),
    toda_prop42_delta_e_exactness_inference_rule(),
  )

  bridge_rule = (
    toda_prop42_exactness_to_generic_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  rules = (
    theorem_rules
    + (
      bridge_rule,
      zero_composition_rule,
    )
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
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
        TodaProp42ExactnessStatement,
      )
    )
  )

  generic_exactness_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        ExactnessStatement,
      )
    )
  )

  zero_composition_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        EHPZeroCompositionStatement,
      )
    )
  )

  return {
    "i": i,
    "n": n,
    "sequence": sequence,
    "windows": windows,
    "premise_steps": premise_steps,
    "theorem_rules": theorem_rules,
    "bridge_rule": bridge_rule,
    "zero_composition_rule": (
      zero_composition_rule
    ),
    "rules": rules,
    "result": result,
    "theorem_steps": theorem_steps,
    "generic_exactness_steps": (
      generic_exactness_steps
    ),
    "zero_composition_steps": (
      zero_composition_steps
    ),
  }


def print_phase45_sequence(
  representative,
):
  print()
  print_separator()
  print("Toda Proposition 4.2")
  print_separator()
  print()

  print("2-primary EHP exactness windows:")
  print()

  for window in representative[
    "windows"
  ]:
    print(
      " ",
      window_text(
        window
      ),
    )


def print_phase45_theorem_results(
  representative,
):
  print()
  print("Toda theorem exactness:")
  print()

  for step in representative[
    "theorem_steps"
  ]:
    print(
      " ",
      window_text(
        step.conclusion.window
      ),
      "is exact",
    )


def print_phase45_generic_bridge(
  representative,
):
  print()
  print("Generic exactness bridge:")
  print()

  for step in representative[
    "generic_exactness_steps"
  ]:
    print(
      " ",
      exactness_text(
        step.conclusion
      ),
    )


def print_phase45_generic_consequence(
  representative,
):
  print()
  print(
    "Existing generic EHP consequence:"
  )
  print()

  for step in representative[
    "zero_composition_steps"
  ]:
    print(
      " ",
      zero_composition_text(
        step.conclusion
      ),
    )


def print_phase45_provenance(
  representative,
):
  print()
  print_separator()
  print("Provenance / fixed point")
  print_separator()
  print()

  print(
    "theorem exactness count =",
    len(
      representative[
        "theorem_steps"
      ]
    ),
  )

  print(
    "generic exactness count =",
    len(
      representative[
        "generic_exactness_steps"
      ]
    ),
  )

  print(
    "zero composition count =",
    len(
      representative[
        "zero_composition_steps"
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


def print_phase45_boundary():
  print()
  print_separator()
  print("Phase 45 completion boundary")
  print_separator()
  print()

  print("Implemented:")
  print(
    "  symbolic E / H / Delta maps"
  )
  print(
    "  Toda EHP structural sequence"
  )
  print(
    "  instance-aware exactness windows"
  )
  print(
    "  three Toda Proposition 4.2 exactness rules"
  )
  print(
    "  instance-aware Toda exactness statements"
  )
  print(
    "  bridge to generic ExactnessStatement"
  )
  print(
    "  existing generic zero-composition reuse"
  )
  print()

  print("Still outside Phase 45:")
  print(
    "  Toda (4.5) stable-range isomorphism"
  )
  print(
    "  Toda Proposition 4.4"
  )
  print(
    "  symbolic map typing solver"
  )
  print(
    "  general symbolic dimension solver"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 45 capability demonstration"
  )

  representative = (
    build_phase45_representative_result()
  )

  print_phase45_sequence(
    representative
  )

  print_phase45_theorem_results(
    representative
  )

  print_phase45_generic_bridge(
    representative
  )

  print_phase45_generic_consequence(
    representative
  )

  print_phase45_provenance(
    representative
  )

  print_phase45_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



