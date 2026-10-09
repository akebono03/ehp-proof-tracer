"""Apply R5 minimum route change, with exact old-code anchors and backups."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
source = root / "web_group_proof.py"
original = source.read_text(encoding="utf-8-sig")
needle = '''      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )'''
replacement = '''      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )
      if n == 3 and k == 2:
        from phase162_web_narrative_integration import (
          build_phase162_web_validated_isomorphism_markdown,
        )
        validated_markdown = (
          build_phase162_web_validated_isomorphism_markdown()
        )
        markdown = (
          markdown.rstrip()
          + "\\n\\n---\\n\\n"
          + "## 懸垂同型の検証済み証明\\n\\n"
          + validated_markdown
        )'''
if original.count(replacement) == 1:
    print("Already applied: web_group_proof.py")
elif original.count(needle) != 1:
    raise RuntimeError("Expected exact narrative route not found; no files modified")
else:
    shutil.copy2(source, source.with_suffix(".py.phase162_r5_backup"))
    source.write_text(original.replace(needle, replacement), encoding="utf-8")
    print("Updated: web_group_proof.py")
# Include the complete modified function for inspection, without truncation.
current = source.read_text(encoding="utf-8")
start = current.index("def build_standard_web_group_proof_view(")
Path(__file__).with_name("CHANGED_FUNCTION_FULL.txt").write_text(
    current[start:], encoding="utf-8"
)
for relative in (
    "phase162_web_narrative_integration.py",
    "tests/test_phase162_r5_web_integration.py",
):
    destination = root / relative
    if destination.exists():
        shutil.copy2(destination, destination.with_suffix(destination.suffix + ".phase162_r5_backup"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).parent / "files" / relative, destination)
    print("Updated:", relative)
