"""Preflight guards for the reviewed, committed R3-R5 Git HEAD."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_runner():
    source = Path(__file__).resolve().parents[1] / "runner.py"
    spec = importlib.util.spec_from_file_location("phase170_r3_r6_head_sync_runner", source)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_mock_repo(tmp_path, runner, monkeypatch, *, head=None, staged="", dirty="", blob=None):
    previous = tmp_path / runner.PREVIOUS_PATCH
    registration = tmp_path / runner.REGISTRATION
    previous.write_bytes(b"reviewed-R3-R5-content")
    registration.parent.mkdir(parents=True, exist_ok=True)
    registration.write_bytes(b"reviewed-source-registration")
    calls = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): head if head is not None else runner.HEAD,
        ("diff", "--cached", "--name-only"): staged,
        ("diff", "--name-only"): dirty,
        ("rev-parse", f"HEAD:{runner.PREVIOUS_PATCH}"): blob if blob is not None else runner.REVIEWED_COMMITTED_R3R5_BLOB,
        ("rev-parse", f"HEAD:{runner.REGISTRATION}"): runner.ORIGINAL_REGISTRATION_BLOB,
        ("diff", "--", runner.REGISTRATION): "",
    }
    def fake_git(root, *args):
        assert root == tmp_path
        return calls[args]
    class FakeSha256:
        def hexdigest(self):
            return runner.PATCHED_R3R5_SHA256
    monkeypatch.setattr(runner, "git", fake_git)
    monkeypatch.setattr(runner.hashlib, "sha256", lambda raw: FakeSha256())
    return calls


def test_preflight_accepts_exact_reviewed_committed_r3r5(tmp_path, monkeypatch):
    runner = load_runner()
    make_mock_repo(tmp_path, runner, monkeypatch)
    result = runner.preflight(tmp_path)
    assert result["head"] == "970535190e160e9f2ae9e596a3ccb13abb9c913c"
    assert result["committed_r3r5_blob"] == "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"


@pytest.mark.parametrize("head", [
    "32377a9fa4dde75ee0366c7460287354a137536f",
    "f" * 40,
])
def test_preflight_rejects_unreviewed_head(tmp_path, monkeypatch, head):
    runner = load_runner()
    make_mock_repo(tmp_path, runner, monkeypatch, head=head)
    with pytest.raises(RuntimeError, match="unreviewed Git branch or HEAD"):
        runner.preflight(tmp_path)


@pytest.mark.parametrize("field", ["staged", "dirty", "blob"])
def test_preflight_rejects_dirty_or_unreviewed_r3r5(tmp_path, monkeypatch, field):
    runner = load_runner()
    changes = {"staged": "phase168_r2_toda52_transport.py",
               "dirty": "phase168_r2_toda52_transport.py",
               "blob": "0" * 40}
    kwargs = {field: changes[field]}
    make_mock_repo(tmp_path, runner, monkeypatch, **kwargs)
    with pytest.raises(RuntimeError):
        runner.preflight(tmp_path)


def test_head_sync_does_not_change_math_sources(tmp_path):
    runner = load_runner()
    package = Path(__file__).resolve().parents[1]
    assert runner.PREVIOUS_PATCH == "phase168_r2_toda52_transport.py"
    assert runner.REGISTRATION == "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py"
    assert runner.NEW_SOURCE == "phase170_r3_r6_prop58_source.py"
    assert (package / "replacement" / runner.NEW_SOURCE).is_file()
    assert (package / "replacement" / "phase168_r2_7_4_literature_connection.py").is_file()
