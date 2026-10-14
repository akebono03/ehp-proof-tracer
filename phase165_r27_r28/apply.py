"""Phase 165 R27-R28: safely retire orphaned Prop. 5.8 / 5.11 bootstrap chain."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

TARGETS = (
    "toda_prop58_zero_bootstrap.py",
    "toda_prop511_zero_bootstrap.py",
)


def active_imports(root: Path) -> list[dict[str, str]]:
    """Find direct imports of candidate modules in root-level production modules."""
    modules = {Path(name).stem for name in TARGETS}
    references: list[dict[str, str]] = []
    for path in sorted(root.glob("*.py")):
        if path.name in TARGETS:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            raise RuntimeError(f"Cannot safely audit {path.name}: {exc}") from exc
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in modules:
                    references.append({"file": path.name, "module": node.module, "line": str(node.lineno)})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in modules:
                        references.append({"file": path.name, "module": alias.name, "line": str(node.lineno)})
    return references


def apply(root: Path | None = None) -> dict[str, object]:
    root = Path.cwd() if root is None else root
    audit = root / "phase165_r27_r28_audit.json"
    blocked = active_imports(root)
    if blocked:
        result = {"phase": "165 R27-R28", "status": "BLOCKED", "references": blocked, "deleted": [], "full_pytest_run": False}
        audit.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        raise RuntimeError(f"Active imports found; no files deleted. See {audit.name}")
    saved = root / "phase165_r27_r28_removed_backup"
    existing = [root / name for name in TARGETS if (root / name).is_file()]
    if existing:
        saved.mkdir(exist_ok=True)
    removed = []
    for path in existing:
        backup = saved / path.name
        if backup.exists() and backup.read_bytes() != path.read_bytes():
            raise RuntimeError(f"Backup collision for {path.name}; manual review required")
    for path in existing:
        shutil.copy2(path, saved / path.name)
        path.unlink()
        removed.append(path.name)
    result = {"phase": "165 R27-R28", "status": "REMOVED" if removed else "ALREADY_REMOVED", "references": [], "deleted": removed, "full_pytest_run": False}
    audit.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(apply(), indent=2, ensure_ascii=False))
