from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_argument_body_renderer.py")
text = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
tree = ast.parse(text)
lines = text.splitlines()

for node in tree.body:
  if (
    isinstance(node, ast.FunctionDef)
    and node.name
    == "render_toda_group_proof_narrative_argument_body_markdown"
  ):
    output = "\n".join(
      lines[node.lineno - 1:node.end_lineno]
    ) + "\n"
    Path(
      ".\\phase143_75ap_r17\\"
      "render_toda_group_proof_narrative_argument_body_markdown.txt"
    ).write_text(
      output,
      encoding="utf-8",
    )
    print(
      "Wrote complete changed function to "
      "phase143_75ap_r17\\"
      "render_toda_group_proof_narrative_argument_body_markdown.txt"
    )
    break
else:
  raise RuntimeError("Target function not found.")
