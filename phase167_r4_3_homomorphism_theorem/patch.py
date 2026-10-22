from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("toda_group_proof_narrative_renderer.py")
OLD = "全射性と核の決定から, 第一同型定理より $"
NEW = "全射性と核の決定から, 準同型定理より $"
FUNCTION_NAME = "render_toda_group_proof_narrative_markdown"


def extract_function_source(source: str, function_name: str) -> str:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            lines = source.splitlines(keepends=True)
            return "".join(lines[node.lineno - 1:node.end_lineno])
    raise RuntimeError(f"function not found: {function_name}")


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"target not found: {TARGET.resolve()}")

    source = TARGET.read_text(encoding="utf-8")
    old_count = source.count(OLD)
    new_count = source.count(NEW)

    if old_count == 0 and new_count == 1:
        print(f"ALREADY_PATCHED: {TARGET.resolve()}")
        Path("phase167_r4_3_homomorphism_theorem/modified_function_full.py").write_text(
            extract_function_source(source, FUNCTION_NAME),
            encoding="utf-8",
        )
        return

    if old_count != 1:
        raise RuntimeError(
            f"expected exactly one active target phrase, found {old_count}: {OLD}"
        )

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_dir = Path("phase167_r4_3_homomorphism_theorem_backup") / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / TARGET.name
    shutil.copy2(TARGET, backup)

    patched = source.replace(OLD, NEW, 1)

    if patched.count(OLD) != 0:
        raise RuntimeError("old phrase remains in active renderer after replacement")
    if patched.count(NEW) != 1:
        raise RuntimeError("new phrase count is not exactly one after replacement")

    ast.parse(patched)
    TARGET.write_text(patched, encoding="utf-8")

    Path("phase167_r4_3_homomorphism_theorem/modified_function_full.py").write_text(
        extract_function_source(patched, FUNCTION_NAME),
        encoding="utf-8",
    )

    print(f"PATCHED: {TARGET.resolve()}")
    print(f"BACKUP: {backup.resolve()}")
    print(
        "FULL MODIFIED FUNCTION: "
        + str(
            Path(
                "phase167_r4_3_homomorphism_theorem/modified_function_full.py"
            ).resolve()
        )
    )


if __name__ == "__main__":
    main()
