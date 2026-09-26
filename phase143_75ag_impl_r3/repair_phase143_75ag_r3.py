from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
  '      + r" \\\\in "\n',
  '      + r" \\in "\n',
  1,
)
text = text.replace(
  '      + r" \\\\pmod{"\n',
  '      + r" \\pmod{"\n',
  1,
)

old_scalar = """      + render_toda_scalar_latex(
        statement.modulus
      )
"""
new_scalar = """      + str(
        statement.modulus
      )
"""

if old_scalar not in text:
  raise RuntimeError(
    "Phase 143-75AG R2 scalar block not found."
  )

text = text.replace(
  old_scalar,
  new_scalar,
  1,
)

ast.parse(text)
path.write_text(text, encoding="utf-8")

print("Phase 143-75AG R3 minimal renderer repair applied.")
print("Undefined scalar helper removed; LaTeX escapes corrected.")
