"""Replace the entire Web group builder, retaining a backup and unchanged imports."""
import ast
from pathlib import Path


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    target = project / "web_group_proof.py"
    source = target.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "build_standard_web_group_proof_view"]
    if len(functions) != 1:
        raise ValueError("expected exactly one Web group proof builder")
    previous = functions[0]
    if "phase164_r5_web_registry_connection" not in ast.get_source_segment(source, previous):
        raise ValueError("Phase 164 R5 Web connection not installed; refusing to patch")
    replacement = (Path(__file__).parent / "replacement_web_function.txt").read_text(encoding="utf-8")
    ast.parse(replacement)
    current_lines = source.splitlines(keepends=True)
    start = sum(map(len, current_lines[:previous.lineno - 1]))
    finish = sum(map(len, current_lines[:previous.end_lineno]))
    updated = source[:start] + replacement.rstrip() + "\n" + source[finish:]
    ast.parse(updated)
    backup = project / "web_group_proof.phase164_r5_r1_backup.py"
    if updated == source:
        print("Common Renderer Web builder already installed")
        return
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated Web Group Proof builder; backup:", backup.name)


if __name__ == "__main__":
    main()
