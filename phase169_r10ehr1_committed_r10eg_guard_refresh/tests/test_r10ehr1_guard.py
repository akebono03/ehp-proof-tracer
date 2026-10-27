"""R10EH-R1 guard-refresh focused tests (no source or proof mutations)."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
ORIGINAL = ROOT / "phase169_r10eh_stem6_10_11_14_audit" / "run.ps1"
REVIEWED = PACKAGE / "payload" / "run_r1.ps1"
ORIGINAL_SHA = "f6a5af06f75121b84b3ff6b77266b36c057ee7f35619c75c6a80f68068159462"
REVIEWED_SHA = "b56d68356c5c7b813bb7cffa7f42ec44045068a350d5df84d88d05fc8ec3c578"


def test_r10ehr1_reviewed_original_runner_is_unchanged():
    assert sha256(ORIGINAL.read_bytes()).hexdigest() == ORIGINAL_SHA


def test_r10ehr1_only_guard_and_source_integrity_are_updated():
    original = ORIGINAL.read_text(encoding="utf-8")
    updated = REVIEWED.read_text(encoding="utf-8")
    assert sha256(REVIEWED.read_bytes()).hexdigest() == REVIEWED_SHA
    assert original.count("463880e69a4bf3a51b07654b74f3ac1c29798176") == 1
    assert original.count("d60770fff1b6e14791db6b952733f4062a64c8eb") == 1
    restored = updated.replace(
        "1a132f382b4fe93b1ab3cb30f5d9178684e9c65a",
        "463880e69a4bf3a51b07654b74f3ac1c29798176",
    ).replace(
        "R10EH-R1 requires reviewed R10EG ancestry",
        "R10EH requires reviewed R10EF ancestry",
    ).replace(
        "3865d1e57923a0d45f0240cc357110e51b20a3e1",
        "d60770fff1b6e14791db6b952733f4062a64c8eb",
    )
    added = (
        "    $LocalTransportBlob = (& git hash-object -- $Target).Trim()\n"
        "    if ($LASTEXITCODE -ne 0 -or $LocalTransportBlob -ne $Known['phase169_r10e1_general_group_transport/transport.py']) {\n"
        "        throw 'R10EH-R1 working transport.py differs from reviewed R10EG blob'\n"
        "    }\n"
    )
    assert restored.replace(added, "") == original


def test_r10ehr1_runner_retains_audit_only_and_focused_checks():
    source = REVIEWED.read_text(encoding="utf-8")
    assert "R10EH_SCOPE=AUDIT_ONLY" in source
    assert "--untracked-files=no" in source
    assert "-m pytest -q -p no:cacheprovider" in source
    assert "phase169_r10eh_stem6_10_11_14_audit.audit" in source
    assert "R10EH_PRODUCTION_FILES_CHANGED=none" in source
    assert "R10EH_FULL_PYTEST_RUN=False" in source
