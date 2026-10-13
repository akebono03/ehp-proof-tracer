"""Replace the R49 display helper without touching the shared renderer."""
from pathlib import Path
import ast
import shutil

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase165_r49_display_order.py"
NEW = PACKAGE / TARGET.name
BACKUP = PACKAGE / "backup_before_apply"


def main() -> None:
    if not TARGET.exists():
        raise RuntimeError("R49 display helper not found; no changes")
    old = TARGET.read_text(encoding="utf-8")
    new = NEW.read_text(encoding="utf-8")
    if old == new:
        print("R50 Delta-reason repair already installed")
        return
    if "def finalize_phase165_r49_typed_reason_order(" not in old:
        raise RuntimeError("Unexpected R49 helper; no changes")
    if "TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO" not in old:
        raise RuntimeError("Missing R49 typed Delta reason; no changes")
    if "After the Reference boundary becomes visible" not in old and "if len(detailed) != 1:" not in old:
        raise RuntimeError("Unexpected previous R49/R50 state; no changes")
    ast.parse(new, filename=NEW.name)
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    TARGET.write_text(new, encoding="utf-8")
    print("R50 typed Delta explanation repaired; previous helper backed up")


if __name__ == "__main__":
    main()
