"""EOL-safe one-function patch and Git-blob pin unit tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r12_hopf_conclusion import install


def _fixture(tmp_path: Path, eol: bytes = b"\n") -> Path:
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(install.REVIEWED.replace(b"\n", eol))
    return tmp_path


def test_pinned_baseline_and_one_function_replacement(tmp_path: Path) -> None:
    assert install.git_blob_sha(install.REVIEWED) == install.REVIEWED_GIT_BLOB
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    assert plan.new_bytes.startswith(install.REVIEWED[:-len(install.BASE)])
    assert plan.new_bytes.endswith(install.FULL)
    install.apply_patch(root, plan)
    assert install.plan_patch(root).status == "ALREADY_APPLIED"


def test_crlf_byte_preservation_and_rerun(tmp_path: Path) -> None:
    root = _fixture(tmp_path, b"\r\n")
    plan = install.plan_patch(root)
    install.apply_patch(root, plan)
    result = (root / install.TARGET).read_bytes()
    assert b"\r\r\n" not in result
    assert result.count(b"\r\n") == result.count(b"\n")
    assert install.plan_patch(root).status == "ALREADY_APPLIED"


def test_unreviewed_target_and_bad_endings_refused(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes().replace(b"No goal,", b"New goal,"))
    with pytest.raises(RuntimeError, match="R3R12_UNREVIEWED_TARGET_REFUSED"):
        install.plan_patch(root)
    target.write_bytes(install.REVIEWED.replace(b"\n", b"\r\n") + b"# LF\n")
    with pytest.raises(RuntimeError, match="R3R12_MIXED_EOL"):
        install.plan_patch(root)


def test_concurrent_edit_refused(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes() + b"# external edit\n")
    with pytest.raises(RuntimeError, match="R3R12_TARGET_CHANGED_SINCE_PREFLIGHT"):
        install.apply_patch(root, plan)


def test_reviewed_source_contains_no_prior_r3r12_hook() -> None:
    reviewed = install.REVIEWED.decode("utf-8")
    assert "project_verified_hopf_lift_conclusion" not in reviewed
    assert reviewed.count("def project_verified_source_and_hopf_summary(") == 1


def test_full_function_contains_only_one_postprocessor_call() -> None:
    full = install.FULL.decode("utf-8")
    baseline = install.BASE.decode("utf-8")
    assert "project_verified_hopf_lift_conclusion(summary, model)" in full
    assert "project_verified_hopf_lift_conclusion" not in baseline
    assert "_verified_hopf_chain_lines(normalized, model, scope)" in full
