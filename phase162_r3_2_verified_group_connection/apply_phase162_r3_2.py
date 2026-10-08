"""R3-2 installer: safeguard the existing local Web entrypoint before changes."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
bundle = Path(__file__).resolve().parent
integration = root / "phase162_web_narrative_integration.py"
web = root / "web_group_proof.py"
if not integration.is_file() or not web.is_file():
    raise SystemExit("The existing Web integration files are required")
previous = integration.read_text(encoding="utf-8-sig")
if "def build_phase162_web_validated_isomorphism_markdown()" not in previous:
    raise SystemExit("Unexpected local integration API; refusing replacement")
if "def _compose_phase162_group_conclusion(" not in previous:
    raise SystemExit("Unexpected local legacy integration; refusing replacement")
source = web.read_text(encoding="utf-8-sig")
old = '"## 懸垂同型の検証済み証明\n\n"'
new = '"## 群構造の検証済み証明\n\n"'
if source.count(old) != 1:
    raise SystemExit("Expected exactly one lower-panel label; refusing replacement")
if "build_phase162_web_validated_isomorphism_markdown" not in source:
    raise SystemExit("Lower-panel Web hook absent; refusing replacement")
replacement = (bundle / "phase162_web_narrative_integration.py").read_text(encoding="utf-8")
backup = bundle / "backup_before_apply"
backup.mkdir(exist_ok=True)
shutil.copy2(integration, backup / integration.name)
shutil.copy2(web, backup / web.name)
integration.write_text(replacement, encoding="utf-8")
web.write_text(source.replace(old,new,1),encoding="utf-8")
print("Updated: phase162_web_narrative_integration.py")
print("Updated lower-panel label only: web_group_proof.py")
print("Backup:",backup)
