"""Offline installer contracts for the exact one-file R4-R7R2 change."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r7r2_pi84_prior_selection import install


def test_full_replacement_keeps_original_imports_and_one_function_change() -> None:
    root = Path(__file__).resolve().parents[2]
    original = (root / "phase173_r4_r7_source_first_rule" / "source.py").read_text(
        encoding="utf-8"
    )
    full = install.replacement_bytes().decode("utf-8")
    before = ast.parse(original)
    after = ast.parse(full)
    assert [ast.dump(x) for x in before.body if isinstance(x, (ast.Import, ast.ImportFrom))] == [
        ast.dump(x) for x in after.body if isinstance(x, (ast.Import, ast.ImportFrom))
    ]
    prior = [n for n in before.body if isinstance(n, ast.FunctionDef)]
    changed = [n for n in after.body if isinstance(n, ast.FunctionDef)]
    assert [x.name for x in prior] == [x.name for x in changed] == [
        "screened_source_first_context"
    ]
    assert install.blob_hash(install.normalize(original.encode("utf-8"))) in (
        install.EXPECTED_BLOB, install.REPLACEMENT_BLOB
    )
    assert "reference.locator == \"Proposition 5.8\"" in full
    assert "admitted_db_step(" in full
    assert "selected.assertion_id" in full
    function = changed[0]
    extracted = "\n".join(full.splitlines()[function.lineno-1:function.end_lineno]) + "\n"
    saved = Path(__file__).resolve().parents[1] / "screened_source_first_context_FULL.py.txt"
    assert saved.read_text(encoding="utf-8") == extracted


def test_fixed_payload_hash() -> None:
    proposed = install.replacement_bytes()
    assert install.blob_hash(proposed) == install.REPLACEMENT_BLOB
    assert len(install.REVIEWED_HEAD) == 40
    assert len(install.SOURCE_GUARDS) >= 7


def test_blob_hash_uses_git_object_prefix() -> None:
    from hashlib import sha1
    assert install.blob_hash(b"a\n") != sha1(b"a\n").hexdigest()
    assert install.normalize(b"A\r\nB\r\n") == b"A\nB\n"


def test_preflight_fails_wrong_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    replies = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "not-reviewed",
    }
    monkeypatch.setattr(install, "git", lambda root, *args: replies[args])
    with pytest.raises(RuntimeError, match="unreviewed develop HEAD"):
        install.preflight(tmp_path, remote=False)


def test_preflight_rejects_wrong_committed_blob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    replies = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): install.REVIEWED_HEAD,
    }
    for file_name in install.SOURCE_GUARDS:
        path = tmp_path / file_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")
        replies[("rev-parse", "HEAD:" + file_name)] = "INVALID"
    monkeypatch.setattr(install, "git", lambda root, *args: replies[args])
    with pytest.raises(RuntimeError, match="unreviewed committed source"):
        install.preflight(tmp_path, remote=False)


def test_dryrun_never_writes_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(install, "preflight", lambda root, remote: "NEEDS_INSTALL")
    assert install.install(tmp_path, dry_run=True, remote=False) == "NEEDS_INSTALL"
    assert list(tmp_path.iterdir()) == []


def test_install_is_idempotent_when_already_installed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(install, "preflight", lambda root, remote: "ALREADY_INSTALLED")
    assert install.install(tmp_path, dry_run=False, remote=False) == "ALREADY_INSTALLED"
    assert list(tmp_path.iterdir()) == []
