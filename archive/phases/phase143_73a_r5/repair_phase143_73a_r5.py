from pathlib import Path
import ast

repo = Path.cwd()
renderer = repo / "toda_group_proof_narrative_renderer.py"

text = renderer.read_text(encoding="utf-8")
text = text.replace("\r\n", "\n").replace("\r", "\n")

old_import = """from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
"""
new_import = """from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
"""

if old_import not in text:
    if "_render_scalar_latex," not in text:
        raise RuntimeError(
            "toda_human_readable_renderer import anchor not found"
        )
else:
    text = text.replace(
        old_import,
        new_import,
        1,
    )

old_block = """  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.left
      )
      + r" \\ge "
      + render_toda_expression_latex(
        statement.right
      )
    )
"""

new_block = """  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return (
      _render_scalar_latex(
        statement.left
      )
      + r" \\ge "
      + _render_scalar_latex(
        statement.right
      )
    )
"""

if old_block not in text:
    raise RuntimeError(
        "Phase 143-73A ScalarGreaterEqualStatement block not found"
    )

text = text.replace(
    old_block,
    new_block,
    1,
)

ast.parse(
    text,
    filename="toda_group_proof_narrative_renderer.py",
)

renderer.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)

print("Phase 143-73A R5 applied.")
print("Changed only ScalarGreaterEqualStatement scalar rendering.")
print("Renderer syntax check passed.")
