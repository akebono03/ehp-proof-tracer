from pathlib import Path

ROOT = Path.cwd()

main_path = ROOT / "main.py"
main_text = main_path.read_text(encoding="utf-8-sig")

r24_main = """    if (
      mode == "narrative"
      and max_depth is not None
    ):
      narrative_replay = (
        build_toda_group_result_proof_replay(
          group_result
        )
      )
      presentation = (
        build_toda_group_proof_presentation(
          narrative_replay
        )
      )
    else:
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )
"""

pre_r24_main = """    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )
"""

if r24_main in main_text:
  main_text = main_text.replace(
    r24_main,
    pre_r24_main,
    1,
  )
elif pre_r24_main not in main_text:
  raise RuntimeError(
    "main.py is neither in the expected R24 state "
    "nor in the expected pre-R24 state"
  )

main_path.write_text(
  main_text,
  encoding="utf-8",
)
print("Rolled back R24 main.py complete-replay change.")

multi_path = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
multi_text = multi_path.read_text(
  encoding="utf-8-sig"
)

anchor = """  protected_step_ids.update(
    id(
      proof_step
    )
    for proof_step in direct_premise_steps
  )

  return frozenset(
"""

restored = """  protected_step_ids.update(
    id(
      proof_step
    )
    for proof_step in direct_premise_steps
  )

  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )

  return frozenset(
"""

if restored in multi_text:
  pass
elif anchor in multi_text:
  multi_text = multi_text.replace(
    anchor,
    restored,
    1,
  )
else:
  raise RuntimeError(
    "multi renderer R24 rollback anchor not found"
  )

multi_path.write_text(
  multi_text,
  encoding="utf-8",
)
print("Rolled back R24 second-level premise-protection removal.")
print("No other production change was made.")
