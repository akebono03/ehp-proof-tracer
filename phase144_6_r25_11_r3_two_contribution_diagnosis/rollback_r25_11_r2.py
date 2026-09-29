from pathlib import Path

TARGET = Path("toda_group_proof_narrative_argument_multi_renderer.py")

R25_11_R2 = """  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )

  return frozenset(
"""

DEVELOP = """  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    for proof_step in direct_premise_steps:
      protected_step_ids.update(
        id(
          premise_step
        )
        for premise_step in proof_step.premises
      )

  return frozenset(
"""


def main() -> None:
  text = TARGET.read_text(encoding="utf-8-sig")

  if DEVELOP in text and R25_11_R2 not in text:
    print("R25-11-R2 rollback already complete.")
    return

  count = text.count(R25_11_R2)
  if count != 1:
    raise RuntimeError(
      "R25-11-R2 rollback anchor mismatch: "
      f"found {count}"
    )

  TARGET.write_text(
    text.replace(R25_11_R2, DEVELOP, 1),
    encoding="utf-8",
  )
  print("R25-11-R2 production change rolled back.")
  print("Restored develop definition-only frontier protection.")


if __name__ == "__main__":
  main()
