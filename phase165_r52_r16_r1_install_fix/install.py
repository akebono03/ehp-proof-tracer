"""R52-R16-R1: install missing R15 module and R16 patch without changing R15 rules."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
R15 = ROOT / "phase165_r52_r15_ordered_citation.py"
R16 = ROOT / "phase165_r52_r16_web_citation_gate.py"
if not TARGET.is_file() or not (ROOT / "phase165_r3_recursive_search.py").is_file():
    raise SystemExit("Repository root files missing; no changes made")
source = TARGET.read_text(encoding="utf-8")
needle = "def search_shared_group_goal("
if source.count(needle) != 1:
    raise SystemExit("Search function boundary missing; no changes made")
old_function = source[source.index(needle):]
new_function = (PACKAGE / "search_shared_group_goal.txt").read_text(encoding="utf-8")
if old_function.strip() != new_function.strip() and "excluded_ids" not in old_function:
    raise SystemExit("Expected R14 root guard; no changes made")
record_needle = "        records.extend(source.records)"
record_replacement = (
    "        records.extend(replace(record, assertion_id=prefix + record.assertion_id) "
    "for record in source.records)"
)
if source.count(record_needle) not in (0, 1):
    raise SystemExit("Unexpected registry record schema; no changes made")
if source.count(record_needle) == 0 and record_replacement not in source:
    raise SystemExit("Unknown registry merge code; no changes made")
new_source = source[:source.index(needle)] + new_function
new_source = new_source.replace(record_needle, record_replacement)
# R15 is installed by the original R15 runner only as a nested package file.
# Copy its original, unchanged version into the repository root if absent.
expected_r15 = (PACKAGE / "phase165_r52_r15_ordered_citation.py").read_bytes()
if R15.exists() and R15.read_bytes() != expected_r15:
    raise SystemExit("Existing root R15 module differs from approved R15 source; no changes made")
# Validate all candidate modules before writing any file.
compile(new_source, str(TARGET), "exec")
for item in ("phase165_r52_r15_ordered_citation.py", "phase165_r52_r16_web_citation_gate.py"):
    candidate = PACKAGE / item
    compile(candidate.read_text(encoding="utf-8"), str(candidate), "exec")
backup = ROOT / "phase165_r52_r9_shared_math.py.r52_r16_backup"
if not backup.exists():
    shutil.copy2(TARGET, backup)
if not R15.exists():
    shutil.copy2(PACKAGE / "phase165_r52_r15_ordered_citation.py", R15)
shutil.copy2(PACKAGE / "phase165_r52_r16_web_citation_gate.py", R16)
if TARGET.read_text(encoding="utf-8") != new_source:
    TARGET.write_text(new_source, encoding="utf-8")
print("R52-R16-R1: R15 root module and R16 shared search installed")
