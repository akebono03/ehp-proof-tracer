from pathlib import Path

TARGET = Path("toda_group_proof_narrative_argument_multi_renderer.py")

OLD = """  if (
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

NEW = """  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )

  return frozenset(
"""

def main() -> None:
  if not TARGET.is_file():
    raise FileNotFoundError(f"target production file not found: {TARGET}")
  text = TARGET.read_text(encoding="utf-8-sig")
  if NEW in text and OLD not in text:
    print("R25-11-R2 ownership-boundary repair already applied.")
    return
  count = text.count(OLD)
  if count != 1:
    raise RuntimeError(
      "expected exactly one definition-only direct-premise protection "
      f"block; found {count}"
    )
  TARGET.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
  print("R25-11-R2 ownership-boundary repair applied.")
  print("Changed only: _toda_group_proof_narrative_argument_frontier_hidden_step_ids")
  print("Restored direct-premise prerequisite protection for every argument role.")
  print("Semantic closure itself is unchanged.")

if __name__ == "__main__":
  main()
