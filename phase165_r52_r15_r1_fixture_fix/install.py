from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
src = Path(__file__).resolve().parent / "test_phase165_r52_r15_ordered_citation.py"
dst = root / "phase165_r52_r15_ordered_citation" / src.name
if not dst.exists():
    raise SystemExit("R15 test file not found; install R15 first")
old = dst.read_text(encoding="utf-8")
if "def _fixture(*, available=1, cited_position=1, citing_position=2, dependencies=()):" not in old:
    raise SystemExit("R15 fixture differs from expected baseline; no changes made")
backup = dst.with_suffix(".py.r15_r1_backup")
if backup.exists():
    raise SystemExit("Backup already exists; no changes made")
shutil.copy2(dst, backup)
shutil.copy2(src, dst)
print("R15-R1: fixture source_id added; production files unchanged")
