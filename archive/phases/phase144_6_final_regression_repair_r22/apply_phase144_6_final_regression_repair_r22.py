from pathlib import Path

path=Path("toda_group_proof_narrative_argument_body_renderer.py")
text=path.read_text(encoding="utf-8-sig")

old="""        if id(
          premise_step
        ) not in redundant_direct_premise_step_ids
"""
new="""        if (
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

if old not in text:
    raise RuntimeError("R22 relocation filter anchor not found")

text=text.replace(old,new,1)
path.write_text(text,encoding="utf-8")

print("Phase 144-6 R22 applied.")
print("Production:")
print("  toda_group_proof_narrative_argument_body_renderer.py")
print("Function:")
print("  render_toda_group_proof_narrative_argument_body_markdown")
print("Tests: unchanged.")
