from pathlib import Path

path = Path("toda_group_proof_narrative_argument_multi_renderer.py")
text = path.read_text(encoding="utf-8-sig")

old = '''  for proof_step in direct_premise_steps:
    protected_step_ids.update(
      id(
        premise_step
      )
      for premise_step in proof_step.premises
    )

  return frozenset(
'''

new = '''  return frozenset(
'''

if old not in text:
    raise RuntimeError(
        "R24 frontier prerequisite-protection anchor not found"
    )

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("R24 frontier repair applied.")
