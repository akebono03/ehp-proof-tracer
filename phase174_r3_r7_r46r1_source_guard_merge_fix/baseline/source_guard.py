"""Read-only verification of R45R1's audited handoff and reviewed search sources."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    git,
    matches_git_blob,
    verify_checkout as verify_r45_checkout,
)

REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    """Permit whole-file CRLF/LF conversions, not content drift."""
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Fail closed on changed HEAD, modified production files or R45 handoff."""
    parent = verify_r45_checkout()
    if parent["local_head"] != REVIEWED_HEAD or parent["remote_head"] != REVIEWED_HEAD:
        raise RuntimeError("R46 requires the exact reviewed merged develop HEAD")
    core_path = ROOT / "phase165_r3_recursive_search.py"
    if not core_path.is_file() or not matches_git_blob(
        core_path.read_bytes(), REVIEWED_SEARCH_BLOB
    ):
        raise RuntimeError("Canonical depth-first search source changed")
    for relative, pin in R45_LOCAL_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or normalized_sha256(file_path.read_bytes()) != pin:
            raise RuntimeError("R45R1 reviewed local handoff changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": parent["local_head"],
        "remote_head": parent["remote_head"],
        "r45r1_local_pins": len(R45_LOCAL_PINS),
        "search_core_pin": REVIEWED_SEARCH_BLOB,
        "tracked_changes": parent["tracked_changes"],
        "production_files_changed": 0,
        "full_pytest": False,
    }
