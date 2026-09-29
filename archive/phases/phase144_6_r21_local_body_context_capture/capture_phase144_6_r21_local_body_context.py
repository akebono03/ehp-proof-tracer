from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_argument_body_renderer.py")
text = path.read_text(encoding="utf-8-sig")
tree = ast.parse(text)

names = {
    "render_toda_group_proof_narrative_argument_body_markdown",
    "_relocatable_toda_group_proof_narrative_direct_derivation_premises",
    "_insert_toda_group_proof_narrative_relocated_direct_premises",
}

lines = text.splitlines()
found = []

for node in tree.body:
    if (
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in names
    ):
        found.append(node)

if not found:
    raise RuntimeError("target body-renderer functions not found")

print("=" * 78)
print(path)
print("Production changes: none")
print("=" * 78)

for node in found:
    print()
    print("#" * 78)
    print(f"{node.name} lines {node.lineno}-{node.end_lineno}")
    print("#" * 78)
    print("\n".join(lines[node.lineno - 1:node.end_lineno]))
