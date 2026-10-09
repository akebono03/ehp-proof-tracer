"""Apply delimiter fix to the existing R3 renderer, preserving other changes."""
from pathlib import Path
import ast
import shutil

bundle = Path(__file__).resolve().parent
root = bundle.parent
target = root / "phase162_r3_narrative_connection.py"
if not target.is_file():
    raise SystemExit("Phase 162 R3 renderer not found")
previous = target.read_text(encoding="utf-8-sig")
if "def _phase162_web_display_math_delimiters(" in previous:
    print("Display-math delimiter conversion already installed")
else:
    needle = '        markdown=heading + "\\n---\\n\\n## 証明\\n\\n" + detailed_ehp + "\\n\\n" + conclusion,'
    if previous.count(needle) != 1 or previous.count("def render_phase162_r3_narrative(") != 1:
        raise SystemExit("Unexpected R3 renderer; refusing speculative modification")
    helper = (bundle / "display_math_helper.py.txt").read_text(encoding="utf-8")
    updated = previous.replace(
        "def render_phase162_r3_narrative(",
        helper + "def render_phase162_r3_narrative(", 1
    )
    replacement = (
        '        markdown=_phase162_web_display_math_delimiters(\n'
        '            heading + "\\n---\\n\\n## 証明\\n\\n" + detailed_ehp + "\\n\\n" + conclusion\n'
        '        ),'
    )
    updated = updated.replace(needle,replacement,1)
    ast.parse(updated)
    backup = bundle / "backup_before_apply" / target.name
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        shutil.copy2(target,backup)
    target.write_text(updated,encoding="utf-8")
    print("Updated:",target)
print("Unchanged: web_group_proof.py, Web routes, proof steps, references, punctuation.")
