from pathlib import Path

TARGET = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

OLD = """        if (
          id(
            premise_step
          ) not in redundant_direct_premise_step_ids
          and (
            excluded_non_exact_step_ids is None
            or id(
              premise_step
            ) not in excluded_non_exact_step_ids
          )
        )
"""

NEW = """        if (
          id(
            premise_step
          ) not in redundant_direct_premise_step_ids
          and (
            excluded_non_exact_step_ids is None
            or id(
              premise_step
            ) not in excluded_non_exact_step_ids
          )
          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
        )
"""

text = TARGET.read_text(encoding="utf-8")

if OLD not in text:
  if NEW in text:
    print("R25-9A-R1 relocation repair already applied.")
  else:
    raise RuntimeError(
      "R25-9A-R1 relocated-premise anchor not found"
    )
else:
  TARGET.write_text(
    text.replace(
      OLD,
      NEW,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "R25-9A-R1 relocation hidden-step repair applied."
  )
