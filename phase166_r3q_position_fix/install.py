"""Guarded, reversible installation of R3-Q position correction."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = Path(__file__).resolve().parent
TARGET = ROOT / "phase166_r3p_position_binding.py"
SOURCE = BUNDLE / "phase166_r3p_position_binding.py"
BACKUPS = ROOT / "phase166_r3q_position_fix_backups"


def _functions(path: Path) -> set[str]:
    return {node.name for node in ast.parse(path.read_text(encoding="utf-8")).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit("STOP: missing production module")
    original = TARGET.read_text(encoding="utf-8")
    required = (
        'def place_r3p_reference_positions(',
        'PROP51_POSITION_MAP',
        'from phase163_r4_registry_bridge import RegistryBridgeResult',
        'return RegistryBridgeResult(result, bridge.records, bridge.proof_links)',
    )
    if not all(item in original for item in required):
        raise SystemExit("STOP: unexpected production source; no change made")
    if _functions(TARGET) != {"place_r3p_reference_positions"}:
        raise SystemExit("STOP: production module has unexpected functions")
    if '"eta2_hopf_relation": 100' not in original or '"higher_eta_group_relation": 600' not in original:
        raise SystemExit("STOP: reviewed positions differ")
    new = SOURCE.read_text(encoding="utf-8")
    ast.parse(new)
    if original == new:
        print("ALREADY_APPLIED")
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = BACKUPS / stamp
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(TARGET, backup / TARGET.name)
    TARGET.write_text(new, encoding="utf-8")
    (BUNDLE / "last_backup.txt").write_text(str(backup / TARGET.name), encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("FUNCTION: place_r3p_reference_positions")


if __name__ == "__main__":
    main()
