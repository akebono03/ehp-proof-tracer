"""Adjust prior R10 expectations invalidated by the reviewed R57-R11 order policy."""
from __future__ import annotations

from pathlib import Path
import shutil


def update_test(root: Path, package: Path) -> str:
    target = root / "phase165_r57_r10_proofstep_fidelity" / "test_phase165_r57_r10_proofstep_fidelity.py"
    desired = (package / target.name).read_text(encoding="utf-8")
    if not target.exists():
        raise RuntimeError("R57-R10 regression test missing")
    current = target.read_text(encoding="utf-8")
    if current == desired:
        return "ALREADY_UPDATED"
    required = ("def test_r10_stable_target_is_completed_without_transport_inference():",
                "def test_r10_public_narrative_matches_actual_nontransport_proof():")
    if not all(token in current for token in required):
        raise RuntimeError("R57-R10 test unexpectedly changed; abort")
    backup = target.with_suffix(".r57_r11_before.py.bak")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(desired, encoding="utf-8")
    return "UPDATED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R11 regression:", update_test(package.parent, package))
