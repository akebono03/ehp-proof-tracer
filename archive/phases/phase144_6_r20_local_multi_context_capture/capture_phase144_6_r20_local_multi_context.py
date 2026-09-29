from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_argument_multi_renderer.py")
text = path.read_text(encoding="utf-8-sig")
tree = ast.parse(text)

target = None
for node in tree.body:
    if (
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name
        == "render_toda_group_proof_narrative_multi_argument_markdown"
    ):
        target = node
        break

if target is None:
    raise RuntimeError(
        "render_toda_group_proof_narrative_multi_argument_markdown not found"
    )

lines = text.splitlines()
start = target.lineno
end = target.end_lineno

print("=" * 78)
print(path)
print(
    "render_toda_group_proof_narrative_multi_argument_markdown "
    f"lines {start}-{end}"
)
print("Production changes: none")
print("=" * 78)
print("\n".join(lines[start - 1:end]))
