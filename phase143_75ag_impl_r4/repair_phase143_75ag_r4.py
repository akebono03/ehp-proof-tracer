from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

old = """      + render_toda_primary_group_latex(
        statement.ambient_group
      )
"""

new = """      + (
        r"\\pi_{"
        + str(
          statement.ambient_group.group_dimension
        )
        + r"}^{"
        + str(
          statement.ambient_group.sphere_dimension
        )
        + r"}"
      )
"""

if old not in text:
  raise RuntimeError(
    "Phase 143-75AG R3 ambient-group block "
    "not found."
  )

text = text.replace(
  old,
  new,
  1,
)

ast.parse(text)
path.write_text(text, encoding="utf-8")

print("Phase 143-75AG R4 minimal renderer repair applied.")
print(
  "HomotopyGroup ambient dimensions are rendered "
  "directly from first-class fields."
)
