"""Replace the complete R14 search function, retaining all other code."""
from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
if not TARGET.is_file() or not (ROOT / "phase165_r52_r15_ordered_citation.py").is_file():
    raise SystemExit("Run from the repository root with R15 installed")
source = TARGET.read_text(encoding="utf-8")
needle = "def search_shared_group_goal("
if source.count(needle) != 1 or "excluded_ids" not in source[source.index(needle):]:
    raise SystemExit("Expected installed R14 root guard; no files changed")
new_function = (PACKAGE / "search_shared_group_goal.txt").read_text(encoding="utf-8")
new_source = source[:source.index(needle)] + new_function
record_needle = "        records.extend(source.records)"
record_replacement = (
    "        records.extend(replace(record, assertion_id=prefix + record.assertion_id) "
    "for record in source.records)"
)
if new_source.count(record_needle) != 1:
    raise SystemExit("Expected merged registry record code; no files changed")
new_source = new_source.replace(record_needle, record_replacement)
backup = ROOT / "phase165_r52_r9_shared_math.py.r52_r16_backup"
if not backup.exists():
    shutil.copy2(TARGET, backup)
shutil.copy2(PACKAGE / "phase165_r52_r16_web_citation_gate.py", ROOT / "phase165_r52_r16_web_citation_gate.py")
TARGET.write_text(new_source, encoding="utf-8")
print("R52-R16 web citation screening installed; existing adopted-source boundary retained")
