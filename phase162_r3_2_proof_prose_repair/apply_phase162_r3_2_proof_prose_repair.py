"""Install the proof prose repair, preserving the upper Group proof."""
from pathlib import Path
import shutil

bundle = Path(__file__).resolve().parent
root = bundle.parent
checks = (
    ("phase162_r3_narrative_connection.py", "def render_phase162_r3_narrative("),
    ("tests/test_phase162_r3_narrative_connection.py", "def test_r3_final_claim_is_derived_from_proof_root("),
)
for relative, token in checks:
    existing = root / relative
    incoming = bundle / relative
    if not existing.is_file() or not incoming.is_file():
        raise SystemExit(f"Missing required local file: {relative}")
    if token not in existing.read_text(encoding="utf-8-sig"):
        raise SystemExit(f"Unexpected local implementation: {relative}")

web = root / "web_group_proof.py"
integration = root / "phase162_web_narrative_integration.py"
if not web.is_file() or not integration.is_file():
    raise SystemExit("Phase 162 lower Web panel is missing")
if "## 群構造の検証済み証明" not in web.read_text(encoding="utf-8-sig"):
    raise SystemExit("R3-2 lower panel is not installed; refusing unrelated replacement")
if "render_phase162_r3_narrative(" not in integration.read_text(encoding="utf-8-sig"):
    raise SystemExit("R3-2 Web integration is not connected")

backup = bundle / "backup_before_apply"
for relative, _ in checks:
    existing = root / relative
    incoming = bundle / relative
    destination = backup / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(existing, destination)
    existing.write_text(incoming.read_text(encoding="utf-8-sig"), encoding="utf-8")
    print("Updated:", relative)
print("Untouched: web_group_proof.py, phase162_web_narrative_integration.py")
print("Backup directory:", backup)
