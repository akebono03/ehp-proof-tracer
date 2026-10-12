"""Install focused shared Web parser changes without replacing unrelated code."""
import ast
from pathlib import Path


REPLACEMENTS = {
    "_build_group_proof_inline_segments": "replacement_inline_segments.txt",
    "_build_group_proof_rendered_lines": "replacement_rendered_lines.txt",
}


def main() -> None:
    bundle = Path(__file__).resolve().parent
    target = bundle.parent / "web_group_proof.py"
    source = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    lines = source.splitlines(keepends=True)
    replacements = []
    for name, filename in REPLACEMENTS.items():
        if name not in functions:
            raise ValueError(f"Required function missing: {name}")
        node = functions[name]
        old = ast.get_source_segment(source, node)
        if name == "_build_group_proof_inline_segments":
            if "tag_position = math_value.rfind" in old:
                print("Shared punctuation parser already installed")
                return
            if 'if r"\\tag{" in math_value' not in old:
                raise ValueError("Unexpected inline parser baseline")
        else:
            if 'stripped.startswith("## ")' not in old:
                raise ValueError("Unexpected line parser baseline")
        new = (bundle / filename).read_text(encoding="utf-8")
        ast.parse(new)
        replacements.append((sum(map(len, lines[:node.lineno-1])),
                             sum(map(len, lines[:node.end_lineno])),new))

    updated = source
    for start, end, replacement in sorted(replacements, reverse=True):
        updated = updated[:start] + replacement + updated[end:]
    ast.parse(updated)
    backup = bundle.parent / "web_group_proof.phase164_r5_r3_backup.py"
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated common Web math parser; backup:", backup.name)


if __name__ == "__main__":
    main()
