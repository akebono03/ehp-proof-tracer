"""Guarded, reversible, minimal Phase 165 R5-R11 migration."""
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OLD = ROOT / "phase162_web_narrative_integration.py"
REPLAY = ROOT / "phase162_pi5_3_web_replay.py"
NEW = ROOT / "phase162_ehp_leaf_inputs.py"
BACKUP = ROOT / ".phase165_r5_r11_backup"
OLD_IMPORT = "from phase162_web_narrative_integration import _phase162_ehp_leaves"
NEW_IMPORT = "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves"


def read_file(path):
    data = path.read_bytes()
    return data.decode("utf-8-sig"), data.startswith(b"\xef\xbb\xbf"), "\r\n" if b"\r\n" in data else "\n"


def write_file(path, content, bom, newline):
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + normalized.replace("\n", newline).encode("utf-8"))


def install():
    if BACKUP.exists():
        raise RuntimeError("Backup exists. Refusing to overwrite: " + str(BACKUP))
    if NEW.exists():
        raise RuntimeError("New leaf module already exists: " + str(NEW))
    for path in (OLD, REPLAY):
        if not path.is_file():
            raise RuntimeError("Required file not found: " + str(path))
    old, old_bom, old_newline = read_file(OLD)
    replay, replay_bom, replay_newline = read_file(REPLAY)
    tree = ast.parse(old)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "_phase162_ehp_leaves"]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one existing EHP leaf function")
    node = matches[0]
    source_lines = old.splitlines(keepends=True)
    function_source = "".join(source_lines[node.lineno - 1:node.end_lineno]).replace("\r\n", "\n")
    template = (PACKAGE / "phase162_ehp_leaf_inputs.py").read_text(encoding="utf-8")
    new_func = template[template.index("def _phase162_ehp_leaves():"):]
    if ast.dump(ast.parse(function_source), include_attributes=False) != ast.dump(ast.parse(new_func), include_attributes=False):
        raise RuntimeError("Local leaf function differs from vetted source: no migration")
    if replay.count(OLD_IMPORT) != 1:
        raise RuntimeError("Expected one replay import, found " + str(replay.count(OLD_IMPORT)))
    # Preserve entire module outside this function. Replace with a compatibility alias.
    source_lines[node.lineno - 1:node.end_lineno] = [NEW_IMPORT + "\n"]
    changed_old = "".join(source_lines)
    changed_replay = replay.replace(OLD_IMPORT, NEW_IMPORT, 1)
    ast.parse(changed_old)
    ast.parse(changed_replay)
    BACKUP.mkdir()
    try:
        shutil.copy2(OLD, BACKUP / OLD.name)
        shutil.copy2(REPLAY, BACKUP / REPLAY.name)
        NEW.write_bytes((PACKAGE / "phase162_ehp_leaf_inputs.py").read_bytes())
        write_file(OLD, changed_old, old_bom, old_newline)
        write_file(REPLAY, changed_replay, replay_bom, replay_newline)
    except BaseException:
        restore()
        raise
    return {"status": "INSTALLED", "modified_files": [OLD.name, REPLAY.name], "added_file": NEW.name, "backup": BACKUP.name, "removed_legacy_renderer": False, "full_pytest_run": False}


def restore():
    for path in (OLD, REPLAY):
        backup = BACKUP / path.name
        if backup.is_file():
            shutil.copy2(backup, path)
    if NEW.exists():
        NEW.unlink()
    return {"status": "RESTORED"}


if __name__ == "__main__":
    print(json.dumps(install(), ensure_ascii=False, indent=2))
