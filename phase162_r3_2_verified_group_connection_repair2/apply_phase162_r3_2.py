"""Phase 162 R3-2 installer: match the actual escaped Web heading literal."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
bundle = Path(__file__).resolve().parent
integration = root / "phase162_web_narrative_integration.py"
web = root / "web_group_proof.py"
if not integration.is_file() or not web.is_file():
    raise SystemExit("Existing Web integration files are required")

previous = integration.read_text(encoding="utf-8-sig")
source = web.read_text(encoding="utf-8-sig")
replacement = (bundle / "phase162_web_narrative_integration.py").read_text(encoding="utf-8")

api = "def build_phase162_web_validated_isomorphism_markdown()"
if api not in previous or api not in replacement:
    raise SystemExit("Unexpected local integration API; refusing replacement")
if "build_phase162_web_validated_isomorphism_markdown" not in source:
    raise SystemExit("Lower-panel Web hook absent; refusing replacement")

old_heading = "## 懸垂同型の検証済み証明"
new_heading = "## 群構造の検証済み証明"

# The real Web source holds a Python string literal with backslash-n escapes.
# Count only the literal heading, never the entire Markdown value.
if source.count(old_heading) == 1 and source.count(new_heading) == 0:
    updated_web = source.replace(old_heading, new_heading, 1)
elif source.count(old_heading) == 0 and source.count(new_heading) == 1:
    updated_web = source
else:
    raise SystemExit("Unexpected lower-panel heading state; refusing replacement")

# Require the heading to be within the existing n=3, k=2 hook's region.
hook = source.find('if n == 3 and k == 2:')
if hook == -1 or old_heading not in source[hook:] and new_heading not in source[hook:]:
    raise SystemExit("Expected heading adjacent to lower-panel hook; refusing replacement")

backup = bundle / "backup_before_apply"
backup.mkdir(exist_ok=True)
shutil.copy2(integration, backup / integration.name)
shutil.copy2(web, backup / web.name)

integration.write_text(replacement, encoding="utf-8")
if updated_web != source:
    web.write_text(updated_web, encoding="utf-8")
    print("Updated lower-panel heading in web_group_proof.py")
else:
    print("Lower-panel heading already updated in web_group_proof.py")
print("Updated phase162_web_narrative_integration.py")
print("Backups:", backup)
