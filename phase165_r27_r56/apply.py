"""R27-R56: remove only dead legacy imports from migrated Web group entries.

Never rewrite a function body, alter its public interface, or remove an import
which is referenced anywhere in the module. The decision uses the local tree.
"""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    "web_group_query.py": frozenset({"toda_calculation_facade", "toda_human_readable_renderer"}),
    "web_group_proof.py": frozenset({"toda_calculation_facade", "repository_element_presentation"}),
}


def transform(source: str, modules: frozenset[str]) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    references = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            references.add(node.id)
    edits = []
    removed = []
    kept = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.module not in modules:
            continue
        unused = [a for a in node.names if (a.asname or a.name) not in references]
        used = [a for a in node.names if (a.asname or a.name) in references]
        if used:
            kept.append(node.module)
        if not unused:
            continue
        if used:
            # Do not risk changing the formatting of a mixed import.
            kept.append(node.module)
            continue
        edits.append((node.lineno - 1, node.end_lineno))
        removed.append(node.module)
    for start, stop in sorted(edits, reverse=True):
        lines[start:stop] = []
    output = ''.join(lines)
    ast.parse(output)
    return output, tuple(sorted(set(removed))), tuple(sorted(set(kept)))


def apply(root: Path = ROOT) -> dict:
    planned = []
    for filename, modules in TARGETS.items():
        path = root / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8-sig")
        updated, removed, kept = transform(original, modules)
        planned.append((path, original, updated, removed, kept))
    backup = root / "phase165_r27_r56_backup"
    for path, original, updated, _, _ in planned:
        if updated != original and (backup / path.name).exists():
            if (backup / path.name).read_text(encoding="utf-8-sig") != original:
                raise RuntimeError("backup conflict: " + path.name)
    modified = []
    for path, original, updated, _, _ in planned:
        if updated == original:
            continue
        backup.mkdir(exist_ok=True)
        if not (backup / path.name).exists():
            shutil.copy2(path, backup / path.name)
        path.write_text(updated, encoding="utf-8")
        modified.append(path.name)
    result = {
        "phase": "165 R27-R56",
        "status": "CHANGED" if modified else "ALREADY_INSTALLED_OR_IMPORTS_STILL_USED",
        "modified_files": modified,
        "removed_unused_imports": {p.name: list(removed) for p, _, _, removed, _ in planned},
        "retained_used_imports": {p.name: list(kept) for p, _, _, _, kept in planned},
        "legacy_group_calculation_removed": False,
        "remaining_legacy_repository_modules": sorted(p.stem for p in root.glob('repository_*.py')),
        "full_pytest_run": False,
    }
    (root / "phase165_r27_r56_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
