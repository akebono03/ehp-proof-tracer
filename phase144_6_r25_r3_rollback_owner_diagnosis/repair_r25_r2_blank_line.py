from pathlib import Path

path = Path.cwd() / "toda_group_proof_narrative_argument_multi_renderer.py"
text = path.read_text(encoding="utf-8-sig")

old = """  )

def render_toda_group_proof_narrative_multi_argument_markdown(
"""

new = """  )


def render_toda_group_proof_narrative_multi_argument_markdown(
"""

if new in text:
  print("Canonical inter-function blank line already present.")
elif old in text:
  text = text.replace(
    old,
    new,
    1,
  )
  path.write_text(
    text,
    encoding="utf-8",
  )
  print("Restored the single missing inter-function blank line.")
else:
  raise RuntimeError(
    "Expected R25-R2 function boundary not found."
  )
