from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
ast.parse(text)

old = '      + render_toda_expression_latex(\n        statement.two_primary_right_group\n      )\n'
new = '      + _render_phase143_75ao_homotopy_group(\n        statement.two_primary_right_group\n      )\n'

count = text.count(old)
if count != 1:
    raise RuntimeError(
        "Expected exactly one Phase 143-75AP "
        "two_primary_right_group expression rendering; "
        f"found {count}."
    )

text = text.replace(old, new, 1)
ast.parse(text)
path.write_text(text, encoding="utf-8")

print(
    "Phase 143-75AP R4 primary-group rendering "
    "repair applied."
)
