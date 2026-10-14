"""Phase 165 R27-R39: detach pure LaTeX formatting from old repository types."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

MODULE = "toda_conclusion_latex_renderer"
OLD_MODULE = "repository_element_presentation"
SYMBOL = "render_repository_conclusion_latex"
TARGETS = (
    "phase162_r3e_structured_root_renderer.py",
    "phase162_validated_proof_presentation.py",
    "toda_group_proof_generic_narrative_renderer.py",
    "toda_group_proof_narrative_renderer.py",
    "toda_group_proof_outline_renderer.py",
    "toda_group_result_proof_replay_renderer.py",
    "toda_group_structure_transport_reason.py",
    "web_generator_proof.py",
    "web_generator_proof_scope.py",
    "web_generator_applicability.py",
    "web_generator_execution.py",
    "web_group_proof_common.py",
)


def rewrite_imports(source: str) -> tuple[str, bool]:
    """Move only the function import; leave other legacy type imports intact."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    changes: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.module != OLD_MODULE:
            continue
        imported = [alias for alias in node.names if alias.name == SYMBOL]
        if not imported:
            continue
        if len(imported) != 1:
            raise RuntimeError("duplicate conclusion renderer import")
        old_names = [alias for alias in node.names if alias.name != SYMBOL]
        if any(alias.name == "*" for alias in node.names):
            raise RuntimeError("cannot rewrite wildcard import")
        alias = imported[0]
        exported = alias.name + (" as " + alias.asname if alias.asname else "")
        replacement = f"from {MODULE} import {exported}\n"
        if old_names:
            remaining = ", ".join(
                item.name + (" as " + item.asname if item.asname else "")
                for item in old_names
            )
            replacement += f"from {OLD_MODULE} import {remaining}\n"
        changes.append((node.lineno - 1, node.end_lineno, replacement))
    if not changes:
        return source, False
    for first, last, replacement in sorted(changes, reverse=True):
        lines[first:last] = [replacement]
    output = "".join(lines)
    ast.parse(output)
    return output, True


def plan(root: Path, new_module_source: str) -> dict:
    """Check that source and destinations are valid before touching files."""
    if not (root / OLD_MODULE.replace(".", "/")).with_suffix(".py").exists():
        raise FileNotFoundError("expected existing legacy renderer is missing")
    ast.parse(new_module_source)
    new_path = root / f"{MODULE}.py"
    if new_path.exists() and new_path.read_text(encoding="utf-8") != new_module_source:
        raise RuntimeError("different shared renderer already exists")
    modified = {}
    skipped = []
    for filename in TARGETS:
        path = root / filename
        if not path.is_file():
            skipped.append(filename)
            continue
        original = path.read_text(encoding="utf-8")
        updated, changed = rewrite_imports(original)
        if changed:
            modified[filename] = updated
    return {"modified": modified, "skipped": skipped, "new_module": not new_path.exists()}


def apply(root: Path, package: Path) -> dict:
    source = (package / f"{MODULE}.py").read_text(encoding="utf-8")
    work = plan(root, source)
    backup_dir = root / "phase165_r27_r39_backup"
    for filename, updated in work["modified"].items():
        dst = backup_dir / filename
        if dst.exists() and dst.read_text(encoding="utf-8") != (root / filename).read_text(encoding="utf-8"):
            raise RuntimeError(f"backup conflict: {filename}")
    backup_dir.mkdir(exist_ok=True)
    for filename in work["modified"]:
        dst = backup_dir / filename
        if not dst.exists():
            shutil.copy2(root / filename, dst)
    new_path = root / f"{MODULE}.py"
    if not new_path.exists():
        new_path.write_text(source, encoding="utf-8")
    for filename, updated in work["modified"].items():
        (root / filename).write_text(updated, encoding="utf-8")
    result = {
        "phase": "165 R27-R39",
        "status": "CHANGED" if work["modified"] or work["new_module"] else "ALREADY_INSTALLED",
        "modified_files": sorted(work["modified"]),
        "new_shared_renderer": MODULE if work["new_module"] else None,
        "legacy_renderer_preserved": True,
        "skipped_missing_optional_files": work["skipped"],
        "deleted_repository_modules": [],
        "full_pytest_run": False,
    }
    (root / "phase165_r27_r39_audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    print(json.dumps(apply(root, Path(__file__).resolve().parent), ensure_ascii=False, indent=2))
