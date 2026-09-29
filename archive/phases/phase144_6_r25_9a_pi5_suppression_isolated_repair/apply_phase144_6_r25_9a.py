from pathlib import Path

TARGET = Path(
  "toda_group_proof_narrative_argument_multi_renderer.py"
)

OLD = """  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )

  return frozenset(
"""

NEW = """  if (
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

text = TARGET.read_text(encoding="utf-8")

if OLD not in text:
  if NEW in text:
    print("R25-9A production repair already applied.")
  else:
    raise RuntimeError(
      "R25-9A frontier protection anchor not found"
    )
else:
  text = text.replace(
    OLD,
    NEW,
    1,
  )
  TARGET.write_text(
    text,
    encoding="utf-8",
  )
  print(
    "R25-9A isolated suppression repair applied."
  )
