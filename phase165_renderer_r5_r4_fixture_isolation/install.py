from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

OLD = "from toda_group_proof_generic_narrative_renderer import (\n        _render_generic_narrative_step,\n    )"
NEW = "from toda_group_proof_narrative_renderer import (\n        _render_generic_narrative_step,\n    )"
TARGET = Path("tests/test_phase162_r2_validated_proof_presentation.py")
BACKUP = Path(".phase165_renderer_r5_r3_test_backup/test_phase162_r2_validated_proof_presentation.py")

def install(project: Path) -> dict:
    path = project / TARGET
    backup = project / BACKUP
    if not path.is_file():
        raise FileNotFoundError(str(path))
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    text = data.decode("utf-8-sig")
    normalized = text.replace("\r\n", "\n")
    if normalized.count(NEW) == 2 and normalized.count(OLD) == 0:
        return {"status": "ALREADY_INSTALLED", "changed_file": str(TARGET), "import_sites": 2}
    if normalized.count(OLD) != 2:
        raise RuntimeError("Unexpected imports in target test; no changes made: " + str(normalized.count(OLD)))
    modified = normalized.replace(OLD, NEW)
    ast.parse(modified)
    if len([n for n in ast.walk(ast.parse(modified)) if isinstance(n, ast.ImportFrom) and n.module == 'toda_group_proof_generic_narrative_renderer']) != 0:
        raise RuntimeError('Unmigrated old imports: no changes made')
    if backup.exists():
        if backup.read_bytes() != data:
            raise RuntimeError('Backup already exists with different content; no changes made')
    else:
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    linebreak = "\r\n" if b"\r\n" in data else "\n"
    output = (b"\xef\xbb\xbf" if bom else b"") + modified.replace("\n", linebreak).encode("utf-8")
    path.write_bytes(output)
    return {"status": "INSTALLED", "changed_file": str(TARGET), "import_sites": 2, "backup": str(BACKUP)}

def restore(project: Path) -> dict:
    backup = project / BACKUP
    destination = project / TARGET
    if not backup.is_file():
        raise FileNotFoundError(str(backup))
    shutil.copy2(backup, destination)
    return {"status": "RESTORED", "path": str(TARGET)}

if __name__ == '__main__':
    import sys
    project = Path(__file__).resolve().parent.parent
    result = restore(project) if len(sys.argv) > 1 and sys.argv[1] == '--restore' else install(project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
