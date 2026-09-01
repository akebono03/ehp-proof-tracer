from expression import HomotopyElement
from generator_facts import (
  ETA_3_GENERATOR,
  GENERATOR_FACT_REPOSITORY,
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


def print_phase24_toda_membership_demo():
  print_separator()
  print("Phase 24までの実 Toda 推論")
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
    print("  theorem fact が repository に見つかりません。")
    return

  theorem_step = entry.to_proof_step()

  print("[1] Theorem repository lookup")
  print("  EPSILON_3_TODA_MEMBERSHIP_FACT")
  print("  → found")
  print()

  print("[2] Literature-backed theorem fact")
  print("  theorem:")
  print("    ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  if theorem_step.conclusion.source is not None:
    print("  source:")
    print(
      "   ",
      theorem_step.conclusion.source,
    )
    print()

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=entry.statement.bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  print("[3] GIVEN")
  print("  {η₃,Eν′,ν₇}_1 is defined")
  print()

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  print("[4] Apply inference rule")
  print(
    " ",
    membership_rule,
  )
  print()

  result = run_inference_until_stable_with_history(
    membership_rule,
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

  derived_step = next(
    (
      step
      for step in result.steps
      if step.conclusion == membership
    ),
    None,
  )

  if derived_step is None:
    print("[RESULT]")
    print("  membership was not derived")
    return

  print("[5] Derived")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("Direct premises:")
  for index, premise in enumerate(
    derived_step.premises,
    start=1,
  ):
    print(
      f"  {index}.",
      premise.conclusion,
    )

  print()
  print("Inference result:")
  print(
    "  rule =",
    derived_step.rule,
  )
  print(
    "  termination =",
    result.termination_reason,
  )
  print()
  print("[CONCLUSION]")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")


def print_phase25_generator_typing_demo():
  print()
  print_separator()
  print("Phase 25 generator typing")
  print_separator()
  print()

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  print("[1] Untyped structured generator")
  print("  name      = η₃")
  print(
    "  generator =",
    eta_3.generator,
  )
  print(
    "  source    =",
    eta_3.source,
  )
  print(
    "  target    =",
    eta_3.target,
  )
  print()

  typing_fact = (
    GENERATOR_FACT_REPOSITORY.lookup_typing(
      ETA_3_GENERATOR,
    )
  )

  print("[2] GeneratorFactRepository.lookup_typing()")

  if typing_fact is None:
    print("  η₃ typing fact was not found")
    return

  print("  found:")
  print(
    f"    η₃ : S^{typing_fact.source}"
    f" → S^{typing_fact.target}"
  )
  print()

  typed_eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      eta_3,
    )
  )

  print("[3] materialize_typed_element()")

  if typed_eta_3 is None:
    print("  materialization failed")
    return

  print("  before:")
  print(
    f"    source={eta_3.source}, "
    f"target={eta_3.target}"
  )
  print()

  print("  after:")
  print(
    f"    source={typed_eta_3.source}, "
    f"target={typed_eta_3.target}"
  )
  print()

  print("  mathematical meaning:")
  print(
    f"    η₃ : S^{typed_eta_3.source}"
    f" → S^{typed_eta_3.target}"
  )
  print()

  ambient_fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      ETA_3_GENERATOR,
    )
  )

  print("[4] GeneratorFactRepository.lookup_ambient_group()")

  if ambient_fact is None:
    print("  η₃ ambient-group fact was not found")
  else:
    print(
      "  "
      f"η₃ ∈ π_{ambient_fact.group_dimension}"
      f"(S^{ambient_fact.sphere_dimension})"
    )

  print()
  print("[5] Non-mutation check")
  print(
    "  original source =",
    eta_3.source,
  )
  print(
    "  original target =",
    eta_3.target,
  )
  print(
    "  new source      =",
    typed_eta_3.source,
  )
  print(
    "  new target      =",
    typed_eta_3.target,
  )
  print()

  print("[CONCLUSION]")
  print(
    "  explicit registered generator fact"
  )
  print(
    "  → repository lookup"
  )
  print(
    "  → typed HomotopyElement"
  )
  print(
    "  → η₃ : S⁴ → S³"
  )


def print_current_boundary():
  print()
  print_separator()
  print("Phase 25 completion boundary")
  print_separator()
  print()

  print("現在 production fact から確認できる:")
  print("  η₃ : S⁴ → S³")
  print("  η₃ ∈ π₄(S³)")
  print()

  print("Phase 24までに推論できる:")
  print("  ε₃ ∈ {η₃,Eν′,ν₇}_1")
  print()

  print("まだ Phase 25ではできない:")
  print("  ν′ の production typing")
  print("  ν₇ の production typing")
  print("  repository からの Eν′ automatic typing")
  print(
    "  ε₃ bracket 全3 entry の "
    "production typing"
  )
  print()

  print(
    "したがって現時点では、"
    "membership inference と generator typing は"
  )
  print(
    "存在するが、ε₃ の証明を generator facts から"
    "完全 end-to-end にはまだ接続していない。"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 25 capability demonstration")
  print()

  print_phase24_toda_membership_demo()
  print_phase25_generator_typing_demo()
  print_current_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



