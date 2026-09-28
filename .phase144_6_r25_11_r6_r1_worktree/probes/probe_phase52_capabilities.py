from expression import (
  Multiple,
  WhiteheadProduct,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  run_inference_until_stable_with_history,
)
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
  expression_text,
  print_separator,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
)


def build_phase52_representative_result():
  phase50 = (
    build_phase50_representative_result()
  )

  rules = (
    phase50[
      "rules"
    ]
    + (
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    )
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      phase50[
        "premise_steps"
      ],
    )
  )

  eta_2 = phase50[
    "eta_2"
  ]

  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )

  delta_whitehead_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and isinstance(
        step.conclusion.positive_value,
        WhiteheadProduct,
      )
    )
  )

  whitehead_two_eta_2_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        TodaPi32WhiteheadSquareUpToSignStatement,
      )
      and step.conclusion.positive_value
      == two_eta_2
    )
  )

  delta_two_eta_2_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and step.conclusion.positive_value
      == two_eta_2
    )
  )

  return {
    "phase50": phase50,
    "premise_steps": (
      phase50[
        "premise_steps"
      ]
    ),
    "rules": rules,
    "result": result,
    "eta_2": eta_2,
    "two_eta_2": two_eta_2,
    "delta_whitehead_steps": (
      delta_whitehead_steps
    ),
    "whitehead_two_eta_2_steps": (
      whitehead_two_eta_2_steps
    ),
    "delta_two_eta_2_steps": (
      delta_two_eta_2_steps
    ),
  }


def print_phase52_bridge(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 52 direct Delta bridge"
  )
  print_separator()
  print()

  delta_whitehead = (
    representative[
      "delta_whitehead_steps"
    ][
      0
    ]
    .conclusion
  )

  whitehead_two_eta_2 = (
    representative[
      "whitehead_two_eta_2_steps"
    ][
      0
    ]
    .conclusion
  )

  delta_two_eta_2 = (
    representative[
      "delta_two_eta_2_steps"
    ][
      0
    ]
    .conclusion
  )

  print(
    "  Δ("
    + expression_text(
      delta_whitehead.element
    )
    + ") = ±"
    + expression_text(
      delta_whitehead.positive_value
    )
  )

  print(
    "  "
    + expression_text(
      whitehead_two_eta_2.whitehead_square
    )
    + " = ±"
    + expression_text(
      whitehead_two_eta_2.positive_value
    )
  )

  print(
    "  ↓"
  )

  print(
    "  Δ("
    + expression_text(
      delta_two_eta_2.element
    )
    + ") = ±"
    + expression_text(
      delta_two_eta_2.positive_value
    )
  )


def print_phase52_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / fixed point"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  bridge_step = (
    representative[
      "delta_two_eta_2_steps"
    ][
      0
    ]
  )

  derived_steps = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  print(
    "bridge rule =",
    bridge_step
    .inference_rule
    .name,
  )

  print(
    "bridge premise count =",
    len(
      bridge_step.premises
    ),
  )

  print(
    "bridge premises are derived =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in bridge_step.premises
    ),
  )

  print(
    "bridge result is derived =",
    (
      bridge_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "given premise count =",
    len(
      representative[
        "premise_steps"
      ]
    ),
  )

  print(
    "derived step count =",
    len(
      derived_steps
    ),
  )

  print(
    "derived round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase52_rounds(
  representative,
):
  print()
  print_separator()
  print(
    "Inference rounds"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  for index, round_result in enumerate(
    result.round_results,
    start=1,
  ):
    print(
      "round",
      index,
      "new step count =",
      len(
        round_result.new_steps
      ),
    )


def print_phase52_boundary():
  print()
  print_separator()
  print(
    "Phase 52 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Delta(iota_5) = "
    "±[iota_2,iota_2]"
  )
  print(
    "  [iota_2,iota_2] = "
    "±2eta_2"
  )
  print(
    "  Delta(iota_5) = ±2eta_2"
  )
  print(
    "  Toda-specific direct bridge"
  )

  print()
  print(
    "Still outside Phase 52:"
  )
  print(
    "  general up-to-sign transitivity"
  )
  print(
    "  general sign solver"
  )
  print(
    "  Toda (4.5) finite-cyclic transport"
  )
  print(
    "  higher eta-family bridge"
  )
  print(
    "  Proposition 5.1 integration"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 52 capability demonstration"
  )

  representative = (
    build_phase52_representative_result()
  )

  print_phase52_bridge(
    representative
  )

  print_phase52_rounds(
    representative
  )

  print_phase52_provenance(
    representative
  )

  print_phase52_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


