"""Offline patch safety tests; do not require the repository or runtime DB."""
from pathlib import Path
import ast
import hashlib
import importlib.util

import pytest


PKG = Path(__file__).resolve().parents[1]


def load_runner():
    spec = importlib.util.spec_from_file_location("phase170_r3_r6_runner", PKG / "runner.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_single_existing_registration_file():
    runner = load_runner()
    assert runner.REGISTRATION == "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py"


def test_previous_completed_pi5_transport_is_unchanged():
    runner = load_runner()
    previous = Path("/mnt/data/phase170_r3_r5_toda52_cyclic_generalization/replacement/phase168_r2_toda52_transport.py")
    if previous.exists():
        assert hashlib.sha256(previous.read_bytes()).hexdigest() == runner.PATCHED_R3R5_SHA256
    assert runner.PREVIOUS_PATCH == "phase168_r2_toda52_transport.py"


def test_complete_replacement_has_checked_registration_call():
    data = (PKG / "replacement" / "phase168_r2_7_4_literature_connection.py").read_text()
    assert "register_source_checked_prop58_pi73(second.snapshot)" in data
    assert "registered.proof_links != base.proof_links" in data
    ast.parse(data)


def test_new_source_module_checks_archive_and_hash():
    data = (PKG / "replacement" / "phase170_r3_r6_prop58_source.py").read_text()
    assert "sha256(text.encode(\"utf-8\"))" in data
    assert "SOURCE_DIGEST" in data
    assert "source_statement_id" in data
    assert "METADATA_ONLY" in data
    ast.parse(data)


def test_new_source_does_not_modify_other_proposition_components():
    data = (PKG / "replacement" / "phase170_r3_r6_prop58_source.py").read_text()
    assert 'if original_assertion.assertion_id == COMPONENT_ID:' in data
    assert 'if record.assertion_id == COMPONENT_ID else record' in data


def test_replacement_has_no_placeholder():
    for name in ("phase170_r3_r6_prop58_source.py", "phase168_r2_7_4_literature_connection.py"):
        data = (PKG / "replacement" / name).read_text()
        assert "..." not in data


@pytest.mark.parametrize("file", ["runner.py", "verify.py", "tests/test_phase170_r3_r6_source.py"])
def test_all_scripts_compile(file):
    compile((PKG / file).read_bytes(), file, "exec")


def test_guard_preserves_r3r5_committed_status():
    runner = load_runner()
    assert runner.REGISTRATION != runner.PREVIOUS_PATCH
    assert runner.HEAD == "970535190e160e9f2ae9e596a3ccb13abb9c913c"
    assert runner.REVIEWED_COMMITTED_R3R5_BLOB == "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"


def test_guard_does_not_run_full_pytest():
    data = (PKG / "runner.py").read_text()
    assert '"-p", "no:cacheprovider"' in data
    assert '"tests",' not in data
