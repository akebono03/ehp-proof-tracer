"""R57-R8 focused test contract correction, without production modifications."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(root: Path, package: Path) -> str:
    target = root / "phase165_r57_r8_general_specialization" / "test_phase165_r57_r8_general_specialization.py"
    replacement = package / "test_phase165_r57_r8_general_specialization.py"
    if not target.is_file():
        raise FileNotFoundError("original R57-R8 tests must be installed first")
    current = target.read_text(encoding="utf-8")
    desired = replacement.read_text(encoding="utf-8")
    ast.parse(current)
    ast.parse(desired)
    if current == desired:
        return "ALREADY_INSTALLED"
    if "test_shared_provider_has_specialization_with_screened_reference" not in current:
        raise RuntimeError("unexpected R57-R8 test file; no changes")
    if "test_inference_rule_derives_only_from_typed_source_step" not in current:
        raise RuntimeError("unexpected R57-R8 test file; no changes")
    if "from phase165_r52_r13_reference_registration import build_adopted_prop51_reference" not in current:
        raise RuntimeError("unexpected test source reference; no changes")
    backup = target.with_suffix(".r57_r8_before_test_contract_fix.py.bak")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(desired, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print("R57-R8 test contract correction:", install(folder.parent, folder))
    print("Production files unchanged; full pytest NOT run")
