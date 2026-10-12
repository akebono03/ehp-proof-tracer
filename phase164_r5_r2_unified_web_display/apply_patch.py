"""Fail-closed replacement of the sole public Web group builder."""
import ast
from pathlib import Path
import shutil


def main() -> None:
    bundle = Path(__file__).resolve().parent
    project = bundle.parent
    target = project / "web_group_proof.py"
    before = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(before)
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "build_standard_web_group_proof_view"]
    if len(found) != 1:
        raise ValueError("Expected exactly one public Web group proof builder")
    original = found[0]
    previous = ast.get_source_segment(before, original)
    if "phase164_r5_r2_common_replay" in previous:
        print("R5-R2 Web group builder already installed")
        return
    if "phase164_r5_web_registry_connection" not in previous:
        raise ValueError("R5-R1 baseline missing: refusing to overwrite unexpected code")
    replacement = (bundle / "replacement_web_function.txt").read_text(encoding="utf-8")
    ast.parse(replacement)
    lines = before.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:original.lineno - 1])
    end = sum(len(line) for line in lines[:original.end_lineno])
    after = before[:start] + replacement.rstrip() + "\n" + before[end:]
    ast.parse(after)
    backup = project / "web_group_proof.phase164_r5_r2_backup.py"
    if not backup.exists():
        backup.write_text(before, encoding="utf-8")
    target.write_text(after, encoding="utf-8")
    print("Updated unified Web group proof builder; backup:", backup.name)


if __name__ == "__main__":
    main()
