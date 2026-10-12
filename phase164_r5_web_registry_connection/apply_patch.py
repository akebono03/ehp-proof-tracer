"""Replace one checked Web builder function with its complete R5 implementation."""
from pathlib import Path
import ast


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    source = project / "web_group_proof.py"
    replacement = (Path(__file__).resolve().parent / "replacement_web_function.txt").read_text(encoding="utf-8")
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "build_standard_web_group_proof_view"]
    if len(functions) != 1:
        raise ValueError("expected exactly one group proof builder")
    old = functions[0]
    original_body = "\n".join(text.splitlines()[old.lineno-1:old.end_lineno])
    if "phase164_r5_web_registry_connection" in original_body:
        print("R5 Web builder already present")
        return
    required = ("build_phase162_pi5_3_web_replay", "_build_group_proof_rendered_lines", "build_toda_group_result_proof_replay")
    if not all(token in original_body for token in required):
        raise ValueError("existing Web proof builder differs; abort without changes")
    ast.parse(replacement)
    lines = text.splitlines(keepends=True)
    original_start = sum(len(line) for line in lines[:old.lineno-1])
    original_end = sum(len(line) for line in lines[:old.end_lineno])
    updated = text[:original_start] + replacement.rstrip("\n") + "\n" + text[original_end:]
    ast.parse(updated)
    backup = project / "web_group_proof.phase164_r5_backup.py"
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")
    source.write_text(updated, encoding="utf-8")
    print("Updated web_group_proof.py; backup:", backup.name)


if __name__ == "__main__":
    main()
