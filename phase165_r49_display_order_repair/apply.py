"""Replace only the already-installed R49 helper; leave production files untouched."""
from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / "phase165_r49_display_order.py"
DEST = ROOT / SOURCE.name
RENDERER = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"


def main():
    renderer_source = RENDERER.read_text(encoding="utf-8")
    if "finalize_phase165_r49_typed_reason_order" not in renderer_source:
        raise RuntimeError("R49 display bridge was not installed; no files changed")
    if not DEST.exists():
        raise RuntimeError("Existing R49 helper not found; no files changed")
    current = DEST.read_text(encoding="utf-8")
    if "R49: finish typed reason placement" not in current and "R49: place typed reasons" not in current:
        raise RuntimeError("Unexpected R49 helper version; no files changed")
    updated = SOURCE.read_text(encoding="utf-8")
    ast.parse(updated, filename=str(SOURCE))
    if current == updated:
        print("R49 display order repair already installed")
        return
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DEST, BACKUP / DEST.name)
    DEST.write_text(updated, encoding="utf-8")
    print("R49 display order repair installed; previous helper backed up")


if __name__ == "__main__":
    main()
