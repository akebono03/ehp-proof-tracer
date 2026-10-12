"""Install two shared Web display-parser functions with AST-backed baseline checks."""
import ast
from pathlib import Path

REPLACEMENTS = {
    "_build_group_proof_inline_segments": "replacement_inline_segments.txt",
    "_build_group_proof_rendered_lines": "replacement_rendered_lines.txt",
}


def _check_original_shape(name: str, node: ast.FunctionDef) -> bool:
    """Accept multiline formatting without confusing unrelated implementations."""
    calls = (
        {"find", "append"}
        if name == "_build_group_proof_inline_segments"
        else {"splitlines", "append"}
    )
    called = {
        part.func.attr
        for part in ast.walk(node)
        if isinstance(part, ast.Call) and isinstance(part.func, ast.Attribute)
    }
    text_values = {
        part.value
        for part in ast.walk(node)
        if isinstance(part, ast.Constant) and isinstance(part.value, str)
    }
    if not calls.issubset(called):
        return False
    if name == "_build_group_proof_inline_segments":
        return r"\tag{" in text_values and "inline_math" in text_values
    return "## " in text_values and r"\[" in text_values


def main() -> None:
    bundle = Path(__file__).resolve().parent
    target = bundle.parent / "web_group_proof.py"
    source = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    functions = {
        node.name: node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    lines = source.splitlines(keepends=True)
    planned = []
    installed_count = 0

    for name, filename in REPLACEMENTS.items():
        if name not in functions:
            raise ValueError(f"Required function missing: {name}")
        node = functions[name]
        old = ast.get_source_segment(source, node)
        new = (bundle / filename).read_text(encoding="utf-8")
        new_tree = ast.parse(new)
        if len(new_tree.body) != 1 or not isinstance(new_tree.body[0], ast.FunctionDef):
            raise ValueError(f"Replacement must contain one complete function: {name}")
        if new_tree.body[0].name != name:
            raise ValueError(f"Replacement function name mismatch: {name}")
        if ast.dump(node, include_attributes=False) == ast.dump(new_tree.body[0], include_attributes=False):
            installed_count += 1
            continue
        if not _check_original_shape(name, node):
            raise ValueError(f"Unexpected parser structure: {name}")
        planned.append((
            sum(map(len, lines[:node.lineno - 1])),
            sum(map(len, lines[:node.end_lineno])),
            new,
        ))

    if installed_count == len(REPLACEMENTS):
        print("Shared Web math parser already installed; no changes")
        return

    updated = source
    for start, end, new in sorted(planned, reverse=True):
        updated = updated[:start] + new + updated[end:]
    ast.parse(updated)
    backup = bundle.parent / "web_group_proof.phase164_r5_r3_backup.py"
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated common Web math parser; backup:", backup.name)


if __name__ == "__main__":
    main()
