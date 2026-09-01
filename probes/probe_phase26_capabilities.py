from expression import (
  HomotopyElement,
  Suspension,
  TodaBracket,
)
from generator_facts import (
  ETA_3_GENERATOR,
  GENERATOR_FACT_REPOSITORY,
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
  THEOREM_FACT_REPOSITORY,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaBracketMembershipStatement,
  toda_bracket_membership_from_theorem_inference_rule,
)


def print_separator():
  print("=" * 60)


def print_existing_membership_demo():
  print_separator()
  print("Existing actual Toda membership inference")
  print_separator()
  print()
  print("Goal:")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement,
  )

  if entry is None:
    print("[ERROR]")
    print("  theorem fact was not found")
    return

  theorem_step = entry.to_proof_step()

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=entry.statement.bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    toda_bracket_membership_from_theorem_inference_rule(),
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=entry.statement.element,
    bracket=entry.statement.bracket,
    source=entry.reference,
    note=entry.statement.note,
  )

  derived = any(
    step.conclusion == membership
    for step in result.steps
  )

  print("[RESULT]")
  if derived:
    print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  else:
    print("  membership was not derived")

  print()
  print("  termination =", result.termination_reason)


def materialize_actual_entries():
  eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="η₃",
        dimension=3,
        generator=ETA_3_GENERATOR,
      )
    )
  )

  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  nu_7 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=NU_7_GENERATOR,
      )
    )
  )

  return eta_3, nu_prime, nu_7


def print_phase26_generator_typing_demo():
  print()
  print_separator()
  print("Phase 26 actual generator typing")
  print_separator()
  print()

  eta_3, nu_prime, nu_7 = materialize_actual_entries()

  if eta_3 is None or nu_prime is None or nu_7 is None:
    print("[ERROR]")
    print("  one or more production generator facts could not be materialized")
    return None

  e_nu_prime = Suspension(
    expression=nu_prime,
  )

  print("[1] Production generator facts")
  print(
    f"  η₃  : S^{eta_3.source} → S^{eta_3.target}"
  )
  print(
    f"  ν′  : S^{nu_prime.source} → S^{nu_prime.target}"
  )
  print(
    f"  ν₇  : S^{nu_7.source} → S^{nu_7.target}"
  )
  print()

  print("[2] Existing Suspension semantics")
  print(
    f"  Eν′ : S^{e_nu_prime.source} → S^{e_nu_prime.target}"
  )
  print()

  print("[3] Typing / ambient-group consistency")
  print(
    "  η₃  =",
    GENERATOR_FACT_REPOSITORY
    .is_typing_ambient_group_consistent(
      ETA_3_GENERATOR
    ),
  )
  print(
    "  ν′  =",
    GENERATOR_FACT_REPOSITORY
    .is_typing_ambient_group_consistent(
      NU_PRIME_GENERATOR
    ),
  )
  print(
    "  ν₇  =",
    GENERATOR_FACT_REPOSITORY
    .is_typing_ambient_group_consistent(
      NU_7_GENERATOR
    ),
  )

  return eta_3, e_nu_prime, nu_7


def print_phase26_actual_toda_compatibility_demo(entries):
  print()
  print_separator()
  print("Phase 26 actual ε₃ Toda entry compatibility")
  print_separator()
  print()

  if entries is None:
    print("[ERROR]")
    print("  typed entries are unavailable")
    return

  eta_3, e_nu_prime, nu_7 = entries

  bracket = TodaBracket(
    first=eta_3,
    second=e_nu_prime,
    third=nu_7,
    index=1,
  )

  first_compatible = (
    eta_3.source
    == e_nu_prime.target
  )

  second_compatible = (
    e_nu_prime.source
    == nu_7.target
  )

  print("Bracket:")
  print("  {η₃,Eν′,ν₇}_1")
  print()

  print("[1] η₃ ∘ Eν′")
  print(
    "  η₃.source =",
    eta_3.source,
  )
  print(
    "  Eν′.target =",
    e_nu_prime.target,
  )
  print(
    "  type-compatible =",
    first_compatible,
  )
  print()

  print("[2] Eν′ ∘ ν₇")
  print(
    "  Eν′.source =",
    e_nu_prime.source,
  )
  print(
    "  ν₇.target =",
    nu_7.target,
  )
  print(
    "  type-compatible =",
    second_compatible,
  )
  print()

  print("[3] TodaBracket compatibility query")
  compatible = (
    bracket
    .are_defining_compositions_type_compatible()
  )
  print(
    "  result =",
    compatible,
  )
  print()

  print("[CONCLUSION]")
  if compatible:
    print(
      "  {η₃,Eν′,ν₇}_1 has type-compatible defining compositions"
    )
  else:
    print(
      "  {η₃,Eν′,ν₇}_1 is not type-compatible"
    )


def print_phase26_boundary():
  print()
  print_separator()
  print("Phase 26 completion boundary")
  print_separator()
  print()

  print("Now available from production facts:")
  print("  η₃  : S⁴ → S³")
  print("  ν′  : S⁶ → S³")
  print("  Eν′ : S⁷ → S⁴")
  print("  ν₇  : S¹⁰ → S⁷")
  print()
  print("Validated:")
  print("  η₃ ∘ Eν′ is type-compatible")
  print("  Eν′ ∘ ν₇ is type-compatible")
  print("  {η₃,Eν′,ν₇}_1 has type-compatible defining compositions")
  print()
  print("Still outside Phase 26:")
  print("  η₃ ∘ Eν′ = 0 from production knowledge")
  print("  Eν′ ∘ ν₇ = 0 from production knowledge")
  print("  Toda definedness derived from those zero compositions")
  print("  generator-fact ProofStep / LiteratureReference provenance")
  print()
  print("Important:")
  print("  type-compatible != zero composition != Toda definedness")


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 26 capability demonstration")
  print()

  print_existing_membership_demo()
  entries = print_phase26_generator_typing_demo()
  print_phase26_actual_toda_compatibility_demo(
    entries
  )
  print_phase26_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()
