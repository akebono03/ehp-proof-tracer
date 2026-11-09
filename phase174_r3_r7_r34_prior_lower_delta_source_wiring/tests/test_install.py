"""R34 installer is idempotent and changes one reviewed production anchor."""
from __future__ import annotations

import subprocess

import pytest

from phase174_r3_r7_r34_prior_lower_delta_source_wiring import install


def baseline_source() -> str:
    return subprocess.run(
        ("git", "show", "HEAD:" + install.PRODUCTION),
        cwd=install.ROOT, check=True, capture_output=True,
    ).stdout.decode("utf-8")


def test_patch_is_idempotent_and_contains_only_source_builder():
    base = baseline_source()
    patched = install.patch_source(base)
    assert install.patch_source(patched) == patched
    assert patched.count(install.ADDITION) == 1
    assert patched.replace(install.ANCHOR + "\n" + install.ADDITION,
                           install.ANCHOR) == base


def test_patch_rejects_removed_or_ambiguous_anchor():
    base = baseline_source()
    with pytest.raises(RuntimeError):
        install.patch_source(base.replace(install.ANCHOR, "REPLACED"))
    with pytest.raises(RuntimeError):
        install.patch_source(base + "\n" + install.ANCHOR)


def test_expected_git_blob_is_exactly_reviewed():
    baseline = subprocess.run(
        ("git", "show", "HEAD:" + install.PRODUCTION),
        cwd=install.ROOT, check=True, capture_output=True,
    ).stdout
    revised = install.expected_source_bytes(baseline)
    assert revised != baseline
    assert b"build_cited_lower_delta_sources" in revised
    assert b"register_positioned_prop27" in revised


def test_preflight_after_install_preserves_earlier_phases():
    state = install.preflight()
    assert state["source_guard"] == "PASS"
    assert state["mode"].startswith("INSTALLED")
    assert state["earlier_phases_preserved"] is True
