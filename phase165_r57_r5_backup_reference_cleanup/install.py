"""Phase 165 R57-R5: remove a provably unreferenced historical renderer helper.

Backups are not production consumers. This installer never deletes backups.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

TARGET_NAME = "toda_group_proof_narrative_renderer.py"
DEAD_NAME = "_phase159_render_pi_n_plus_1_n_stable_transport_narrative"
PUBLIC_NAME = "render_toda_group_proof_narrative_markdown"


def classify_reference(path: Path, root: Path) -> str:
    """Conservatively classify Python sources; uncertain files remain production."""
    relative = path.relative_to(root)
    parts = relative.parts
    lower = path.name.lower()
    if "archive" in parts or "backup" in parts or "backups" in parts:
        return "backup"
    if any(tag in lower for tag in ("backup", ".bak", "pre_cleanup", "pre-change", "pre_change")):
        return "backup"
    if lower.startswith("test_") or "tests" in parts:
        return "test"
    return "production"


def references_in_live_sources(root: Path, target: Path) -> dict[str, list[str]]:
    """Search root production modules and tests, separating historical backup files."""
    report = {"production": [], "test": [], "backup": []}
    for path in sorted(root.glob("*.py")):
        if path == target:
            continue
        if DEAD_NAME not in path.read_text(encoding="utf-8-sig"):
            continue
        report[classify_reference(path, root)].append(str(path.relative_to(root)))
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        for path in sorted(tests_dir.rglob("*.py")):
            if DEAD_NAME in path.read_text(encoding="utf-8-sig"):
                report[classify_reference(path, root)].append(str(path.relative_to(root)))
    return report


def remove_dead_helper(source: str) -> tuple[str, bool]:
    """Delete only the named function when no surviving AST Name reference remains."""
    tree = ast.parse(source)
    helpers = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == DEAD_NAME]
    if not helpers:
        return source, False
    if len(helpers) != 1:
        raise RuntimeError("multiple historical helper definitions: refusing deletion")
    helper = helpers[0]
    other_code = [node for node in ast.walk(tree) if isinstance(node, ast.Name) and node.id == DEAD_NAME and isinstance(node.ctx, ast.Load) and not helper.lineno <= node.lineno <= helper.end_lineno]
    if other_code:
        raise RuntimeError("historical helper is still referenced by current module")
    before_public = len([node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == PUBLIC_NAME])
    if before_public < 2:
        raise RuntimeError("expected captured common renderer and final public renderer")
    lines = source.splitlines(keepends=True)
    del lines[helper.lineno - 1:helper.end_lineno]
    updated = "".join(lines)
    rewritten = ast.parse(updated)
    after_public = len([node for node in rewritten.body if isinstance(node, ast.FunctionDef) and node.name == PUBLIC_NAME])
    if before_public != after_public:
        raise RuntimeError("renderer entry definitions unexpectedly changed")
    if "_phase160_r7_previous_public_narrative_renderer" not in updated:
        raise RuntimeError("live common renderer capture missing")
    return updated, True


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    target = root / TARGET_NAME
    if not target.is_file():
        raise FileNotFoundError(target)
    source_bytes = target.read_bytes()
    text = source_bytes.decode("utf-8-sig")
    newline = "\r\n" if b"\r\n" in source_bytes else "\n"
    report = references_in_live_sources(root, target)
    output = root / "phase165_r57_r5_reference_audit.json"
    output.write_text(json.dumps({"helper": DEAD_NAME, "references": report, "deleted": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["production"] or report["test"]:
        raise RuntimeError("active production/test references exist; see " + str(output))
    updated, removed = remove_dead_helper(text)
    if not removed:
        print("R57-R5: historical helper already absent; no modification")
        return 0
    # Removing code from CRLF source must preserve original format.
    backup = target.with_name(target.name + ".phase165_r57_r5_backup")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_bytes(updated.replace("\r\n", "\n").replace("\n", newline).encode("utf-8"))
    output.write_text(json.dumps({"helper": DEAD_NAME, "references": report, "deleted": True, "modified_file": TARGET_NAME}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R57-R5: removed unused Phase 159 helper; preserved backup files and live public renderer")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Full pytest NOT run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
