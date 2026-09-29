from pathlib import Path

path = Path("main.py")
text = path.read_text(encoding="utf-8-sig")

old = '''  else:
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
'''

new = '''  else:
    if (
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

    if mode == "outline":
'''

if old not in text:
    raise RuntimeError(
        "R24 CLI presentation anchor not found"
    )

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("R24 CLI Narrative completeness repair applied.")
