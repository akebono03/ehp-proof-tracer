"""Guarded R4 migration of old generic renderer imports and duplicate definition."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

OLD = "toda_group_proof_generic_narrative_renderer"
PRIMARY = "toda_group_proof_narrative_renderer"
SHARED = "toda_group_proof_narrative_shared_components"
PUBLIC = {"render_toda_partial_proof_narrative_markdown", "render_toda_group_proof_generic_narrative_markdown"}
PREVIOUS = "_phase160_r7_previous_public_narrative_renderer"
RENAMED = "_phase160_r7_pre_transport_narrative"
BACKUP = ".phase165_renderer_r4_backup"


def imported_names(path: Path) -> tuple[tuple[str, ...], ...]:
    tree = ast.parse(path.read_text(encoding="utf8"))
    return tuple(tuple(alias.name for alias in node.names) for node in ast.walk(tree)
                 if isinstance(node, ast.ImportFrom) and node.module == OLD)


def rewrite_imports(source: str) -> tuple[str, int]:
    tree = ast.parse(source)
    changes: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == OLD:
            names = {alias.name for alias in node.names}
            if "*" in names:
                raise RuntimeError("star import from retired renderer cannot be migrated")
            if names & PUBLIC and names - PUBLIC:
                raise RuntimeError("mixed helper/public import needs manual separation")
            target = PRIMARY if names & PUBLIC else SHARED
            oldlines = source.splitlines(keepends=True)
            start = sum(len(s) for s in oldlines[:node.lineno-1])
            end = sum(len(s) for s in oldlines[:node.end_lineno])
            original = source[start:end]
            replacement = original.replace("from " + OLD + " import", "from " + target + " import", 1)
            if replacement == original:
                raise RuntimeError("unrecognized old import syntax")
            changes.append((start,end,replacement))
        elif isinstance(node, ast.Import) and any(alias.name == OLD for alias in node.names):
            if len(node.names) != 1:
                raise RuntimeError("combined legacy import requires review")
            alias = node.names[0]
            oldlines = source.splitlines(keepends=True)
            start = sum(len(s) for s in oldlines[:node.lineno-1])
            end = sum(len(s) for s in oldlines[:node.end_lineno])
            original = source[start:end]
            destination = PRIMARY if "render_toda_partial_proof_narrative_markdown" in source else SHARED
            replacement = original.replace(OLD, destination, 1)
            changes.append((start,end,replacement))
    for start, end, replacement in sorted(changes, reverse=True):
        source = source[:start] + replacement + source[end:]
    ast.parse(source)
    return source, len(changes)


def rewrite_duplicate(source: str) -> str:
    nodes = [x for x in ast.parse(source).body if isinstance(x, ast.FunctionDef)
             and x.name == "render_toda_group_proof_narrative_markdown"]
    if len(nodes) == 1:
        if ("def " + RENAMED + "(") in source:
            return source
        raise RuntimeError("expected R1 duplicate or already migrated state")
    if len(nodes) != 2:
        raise RuntimeError("expected exactly two R1 duplicate public definitions")
    first = nodes[0]
    lines = source.splitlines(keepends=True)
    original = lines[first.lineno-1]
    wanted = "def render_toda_group_proof_narrative_markdown("
    if not original.startswith(wanted):
        raise RuntimeError("unexpected first renderer definition")
    lines[first.lineno-1] = original.replace(wanted, "def " + RENAMED + "(", 1)
    source = "".join(lines)
    old_assignment = PREVIOUS + " = (\n  render_toda_group_proof_narrative_markdown\n)"
    new_assignment = PREVIOUS + " = (\n  " + RENAMED + "\n)"
    if source.count(old_assignment) != 1:
        raise RuntimeError("old internal renderer alias not found uniquely")
    source = source.replace(old_assignment, new_assignment, 1)
    ast.parse(source)
    return source


def find_legacy_imports(project: Path) -> list[str]:
    out = []
    for path in sorted(project.rglob("*.py")):
        if any(part.startswith(".") for part in path.relative_to(project).parts):
            continue
        if "phase165_renderer_r4_legacy_retirement" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf8"))
        except (UnicodeError, SyntaxError):
            continue
        if any((isinstance(x, ast.ImportFrom) and x.module == OLD) or
               (isinstance(x, ast.Import) and any(a.name == OLD for a in x.names))
               for x in ast.walk(tree)):
            out.append(path.relative_to(project).as_posix())
    return out


def install(project: Path) -> dict:
    project = project.resolve()
    primary = project / (PRIMARY + ".py")
    shared = project / (SHARED + ".py")
    alias_dir = project / OLD
    alias = alias_dir / "__init__.py"
    if not all(p.is_file() for p in (primary, shared, alias)):
        if not alias_dir.exists() and primary.is_file() and shared.is_file() and not find_legacy_imports(project):
            return {"status": "ALREADY_INSTALLED", "modified_files": 0}
        raise RuntimeError("expected R3 baseline and old alias package")
    if not (project / "phase165_renderer_narrative_model.py").is_file():
        raise RuntimeError("R2 model missing")
    if not (project / "phase165_r52_partial_proof.py").is_file():
        raise RuntimeError("R3 public entry missing")
    if not ("def render_narrative_proof_model(" in primary.read_text(encoding="utf8")):
        raise RuntimeError("R3 dispatcher missing")
    files = [project / name for name in find_legacy_imports(project)]
    if primary not in files:
        raise RuntimeError("canonical renderer unexpectedly lacks legacy imports")
    modifications: dict[Path, str] = {}
    migrated = 0
    for path in files:
        src = path.read_text(encoding="utf8")
        modified, count = rewrite_imports(src)
        if path == primary:
            modified = rewrite_duplicate(modified)
        if modified != src:
            modifications[path] = modified
        migrated += count
    if find_legacy_imports_after(modifications, files):
        raise RuntimeError("unmigrated import in proposed changes")
    backup = project / BACKUP
    if backup.exists():
        raise RuntimeError("R4 backup directory already exists; refusing overwrite")
    backup.mkdir()
    manifest = {"modified": [p.relative_to(project).as_posix() for p in modifications],
                "legacy_imports_migrated": migrated, "alias_package": OLD}
    try:
        for file, updated in modifications.items():
            dest = backup / file.relative_to(project)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
        dest = backup / OLD
        shutil.copytree(alias_dir, dest)
        (backup / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf8")
        for file, updated in modifications.items():
            file.write_text(updated, encoding="utf8")
        shutil.rmtree(alias_dir)
        remaining = find_legacy_imports(project)
        if remaining:
            raise RuntimeError("remaining old imports: " + ", ".join(remaining))
        definitions = [x for x in ast.parse(primary.read_text(encoding="utf8")).body
                       if isinstance(x, ast.FunctionDef) and x.name == "render_toda_group_proof_narrative_markdown"]
        if len(definitions) != 1:
            raise RuntimeError("canonical public renderer is not unique")
    except BaseException:
        restore(project)
        raise
    return {"status": "INSTALLED", "modified_files": len(modifications),
            "legacy_imports_migrated": migrated, "duplicate_public_definition": "RESOLVED",
            "legacy_alias": "DELETED", "full_pytest_run": False}


def find_legacy_imports_after(modifications: dict[Path, str], files: list[Path]) -> bool:
    for path in files:
        tree = ast.parse(modifications.get(path, path.read_text(encoding="utf8")))
        for x in ast.walk(tree):
            if isinstance(x, ast.ImportFrom) and x.module == OLD:
                return True
            if isinstance(x, ast.Import) and any(a.name == OLD for a in x.names):
                return True
    return False


def restore(project: Path) -> None:
    backup = project / BACKUP
    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf8"))
    for filename in manifest["modified"]:
        original = backup / filename
        destination = project / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, destination)
    alias = project / OLD
    if alias.exists():
        shutil.rmtree(alias)
    shutil.copytree(backup / OLD, alias)


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print(json.dumps(install(folder.parent), ensure_ascii=False, indent=2))
