from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_6_EQUALS_NU_7_FACT,
  NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
)
from proof import (
  ProofRule,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
  THEOREM_FACT_REPOSITORY,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaBracketMembershipStatement,
  indexed_toda_bracket_index1_defined_inference_rule,
  toda_bracket_membership_from_theorem_inference_rule,
)


def print_separator():
  print("=" * 60)


def derive_corrected_end_to_end_result():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )

  suspension_step = relation_proof_step(
    E_NU_6_EQUALS_NU_7_FACT
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  if entry is None:
    return None

  theorem_step = entry.to_proof_step()

  definedness_rule = (
    indexed_toda_bracket_index1_defined_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      definedness_rule,
      membership_rule,
    ),
    (
      first_zero_step,
      second_zero_step,
      suspension_step,
      theorem_step,
    ),
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=entry.statement.bracket,
  )

  membership_statement = (
    TodaBracketMembershipStatement(
      element=entry.statement.element,
      bracket=entry.statement.bracket,
      source=entry.reference,
      note=entry.statement.note,
    )
  )

  defined_step = next(
    (
      step
      for step in result.steps
      if step.conclusion == defined_statement
    ),
    None,
  )

  membership_step = next(
    (
      step
      for step in result.steps
      if step.conclusion == membership_statement
    ),
    None,
  )

  return (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  )


def print_phase27_corrected_inputs():
  print_separator()
  print("Phase 27 corrected mathematical inputs")
  print_separator()
  print()

  print("Goal:")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("[1] First primitive zero-composition fact")
  print("  η₃ ∘ Eν′ = 0")
  print()

  print("[2] Second primitive zero-composition fact")
  print("  ν′ ∘ ν₆ = 0")
  print()

  print("[3] Suspension identification")
  print("  Eν₆ = ν₇")
  print()

  print("Important:")
  print(
    "  the second defining condition is "
    "ν′ ∘ ν₆ = 0"
  )
  print(
    "  rather than a primitive "
    "Eν′ ∘ ν₇ = 0 fact"
  )


def print_theorem_repository_demo(data):
  print()
  print_separator()
  print("Theorem repository input")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  end-to-end data is unavailable")
    return

  (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  ) = data

  print("[4] TheoremFactRepository.lookup()")
  print("  EPSILON_3_TODA_MEMBERSHIP_FACT")
  print("  → found")
  print()

  print("[5] Literature-backed theorem fact")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("  proof rule:")
  print(
    "   ",
    theorem_step.rule,
  )

  print()

  if theorem_step.conclusion.source is not None:
    print("  source:")
    print(
      "   ",
      theorem_step.conclusion.source,
    )


def print_corrected_definedness_demo(data):
  print()
  print_separator()
  print("Corrected indexed Toda definedness")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  end-to-end data is unavailable")
    return

  (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  ) = data

  print("Apply:")
  print(
    " ",
    definedness_rule.name,
  )
  print()

  print("Premises:")
  print("  1. η₃ ∘ Eν′ = 0")
  print("  2. ν′ ∘ ν₆ = 0")
  print("  3. Eν₆ = ν₇")
  print()

  if defined_step is None:
    print("[RESULT]")
    print(
      "  {η₃,Eν′,ν₇}_1 definedness "
      "was not derived"
    )
    return

  print("[6] Derived")
  print("  {η₃,Eν′,ν₇}_1 is defined")
  print()

  print("  rule:")
  print(
    "   ",
    defined_step.rule,
  )

  print()

  print("  inference rule:")
  print(
    "   ",
    defined_step.inference_rule.name,
  )

  print()

  print("  direct premise count:")
  print(
    "   ",
    len(defined_step.premises),
  )

  print()

  if defined_step.premises == (
    first_zero_step,
    second_zero_step,
    suspension_step,
  ):
    print("  provenance:")
    print("    corrected 3-premise chain preserved")
  else:
    print("  provenance:")
    print("    unexpected premise chain")


def print_membership_demo(data):
  print()
  print_separator()
  print("Corrected end-to-end Toda membership")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  end-to-end data is unavailable")
    return

  (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  ) = data

  print("Apply:")
  print(
    " ",
    membership_rule.name,
  )
  print()

  print("Premises:")
  print(
    "  1. Toda theorem:"
  )
  print(
    "     ε₃ ∈ {η₃,Eν′,ν₇}_1"
  )
  print(
    "  2. Derived definedness:"
  )
  print(
    "     {η₃,Eν′,ν₇}_1 is defined"
  )
  print()

  if membership_step is None:
    print("[RESULT]")
    print("  membership was not derived")
    return

  print("[7] Derived")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("  rule:")
  print(
    "   ",
    membership_step.rule,
  )

  print()

  print("  inference rule:")
  print(
    "   ",
    membership_step.inference_rule.name,
  )

  print()

  if membership_step.premises == (
    theorem_step,
    defined_step,
  ):
    print("  direct provenance:")
    print("    theorem fact")
    print("    +")
    print("    derived indexed definedness")
  else:
    print("  direct provenance:")
    print("    unexpected premise chain")


def print_full_proof_trace(data):
  print()
  print_separator()
  print("Human-readable proof trace")
  print_separator()
  print()

  if data is None:
    print("[ERROR]")
    print("  end-to-end data is unavailable")
    return

  (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  ) = data

  if defined_step is None or membership_step is None:
    print("[ERROR]")
    print("  complete proof trace is unavailable")
    return

  print("GIVEN")
  print("  η₃ ∘ Eν′ = 0")
  print()

  print("GIVEN")
  print("  ν′ ∘ ν₆ = 0")
  print()

  print("GIVEN")
  print("  Eν₆ = ν₇")
  print()

  print("INFERENCE")
  print(
    " ",
    definedness_rule.name,
  )
  print("  ↓")
  print("  {η₃,Eν′,ν₇}_1 is defined")
  print()

  print("GIVEN")
  print("  Toda theorem:")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("INFERENCE")
  print(
    " ",
    membership_rule.name,
  )
  print("  ↓")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("Inference engine:")
  print(
    "  rounds =",
    result.round_count,
  )
  print(
    "  termination =",
    result.termination_reason,
  )


def print_corrected_boundary(data):
  print()
  print_separator()
  print("Phase 27 corrected boundary")
  print_separator()
  print()

  print("Primitive production knowledge:")
  print("  η₃ ∘ Eν′ = 0")
  print("  ν′ ∘ ν₆ = 0")
  print("  Eν₆ = ν₇")
  print()

  print("Derived:")
  print("  {η₃,Eν′,ν₇}_1 is defined")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("Not used as primitive defining knowledge:")
  print("  Eν′ ∘ ν₇ = 0")
  print()

  print("Important:")
  print(
    "  displayed adjacent entries "
    "do not determine the indexed "
    "defining conditions"
  )

  if data is None:
    return

  (
    entry,
    first_zero_step,
    second_zero_step,
    suspension_step,
    theorem_step,
    definedness_rule,
    membership_rule,
    result,
    defined_step,
    membership_step,
  ) = data

  print()

  if (
    defined_step is not None
    and membership_step is not None
    and result.round_count == 2
  ):
    print("[CONCLUSION]")
    print(
      "  corrected ε₃ Toda proof chain "
      "runs end-to-end"
    )
  else:
    print("[CONCLUSION]")
    print(
      "  corrected end-to-end proof "
      "was not completed"
    )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 27 corrected end-to-end "
    "capability demonstration"
  )
  print()

  print_phase27_corrected_inputs()

  data = derive_corrected_end_to_end_result()

  print_theorem_repository_demo(
    data
  )

  print_corrected_definedness_demo(
    data
  )

  print_membership_demo(
    data
  )

  print_full_proof_trace(
    data
  )

  print_corrected_boundary(
    data
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



