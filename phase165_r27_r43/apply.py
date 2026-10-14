"""Install the additive R27-R43 typed applicability API without touching legacy data."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "toda_typed_applicability.py"
TARGET = ROOT / "toda_typed_applicability.py"
AUDIT = ROOT / "phase165_r27_r43_audit.json"


def install() -> dict:
    content = SOURCE.read_bytes()
    ast.parse(content.decode("utf-8"))
    if TARGET.exists() and TARGET.read_bytes() != content:
        raise RuntimeError("Existing typed applicability module differs: refusing overwrite")
    for required in ("phase165_r8_rule_provider.py", "proof.py", "phase165_r27_r34_typed_lookup.py"):
        if not (ROOT / required).exists():
            raise FileNotFoundError(f"Required common API missing: {required}")
    created = not TARGET.exists()
    if created:
        TARGET.write_bytes(content)
    audit = {
        "phase": "165 R27-R43",
        "status": "CHANGED" if created else "ALREADY_INSTALLED",
        "created_files": [TARGET.name] if created else [],
        "sha256": hashlib.sha256(content).hexdigest(),
        "legacy_catalog_unchanged": True,
        "legacy_group_calculation_unchanged": True,
        "legacy_repository_modules_deleted": [],
        "full_pytest_run": False,
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return audit


if __name__ == "__main__":
    print(json.dumps(install(), ensure_ascii=False, indent=2))
