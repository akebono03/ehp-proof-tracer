"""Source-independent preflight and mathematical identity contract tests."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import subprocess

import pytest

from phase171_r2g_nu_prime_registered_identity import install


def source_fixture(*, newline: str = "\n") -> bytes:
    source = (
        "from __future__ import annotations\n"
        "from collections import namedtuple\n\n"
        + install.ORIGINAL_FUNCTION + "\n\n"
        + "def unrelated():\n    return 42\n"
    )
    return source.replace("\n", newline).encode("utf-8")


def test_installer_changes_one_full_function_only() -> None:
    before = source_fixture()
    state, after = install.proposed_bytes(before)
    assert state == "NEEDS_PATCH"
    assert install.REPLACEMENT_FUNCTION in after.decode("utf-8")
    assert after.decode("utf-8").replace(install.REPLACEMENT_FUNCTION, install.ORIGINAL_FUNCTION) == before.decode("utf-8")
    assert after.decode("utf-8").endswith("def unrelated():\n    return 42\n")
    ast.parse(after)
    assert install.proposed_bytes(after) == ("ALREADY_PATCHED", after)


def test_installer_preserves_crlf() -> None:
    state, after = install.proposed_bytes(source_fixture(newline="\r\n"))
    assert state == "NEEDS_PATCH"
    assert b"\r\n" in after
    assert b"\n" not in after.replace(b"\r\n", b"")


def test_installer_rejects_unknown_function() -> None:
    changed = source_fixture().replace(b"if identifier == 2:", b"if identifier == 99:")
    with pytest.raises(RuntimeError, match="differs"):
        install.proposed_bytes(changed)


def test_installer_rejects_missing_and_duplicate_function() -> None:
    with pytest.raises(RuntimeError, match="exactly once"):
        install.proposed_bytes(b"def unrelated():\n    return 1\n")
    duplicate = source_fixture() + b"\n" + install.ORIGINAL_FUNCTION.encode("utf-8") + b"\n"
    with pytest.raises(RuntimeError, match="exactly once"):
        install.proposed_bytes(duplicate)


def test_installer_rejects_mixed_newlines() -> None:
    with pytest.raises(RuntimeError, match="mixed newlines"):
        install.proposed_bytes(source_fixture(newline="\r\n") + b"\n")


def test_new_alias_has_complete_source_and_can_run_with_typed_mock() -> None:
    @dataclass(frozen=True)
    class Symbol:
        family: str
        index: int | None = None
        decoration: str | None = None

    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int
        generator: Symbol

    @dataclass(frozen=True)
    class Suspension:
        expression: object

    @dataclass(frozen=True)
    class IteratedSuspension:
        expression: object
        exponent: int

    namespace = {
        "HomotopyElement": HomotopyElement,
        "Suspension": Suspension,
        "IteratedSuspension": IteratedSuspension,
    }
    exec(compile(install.REPLACEMENT_FUNCTION, "<reviewed R2G function>", "exec"), namespace)
    recognized = namespace["_factor_identity"]
    records = {3: {"n": "3", "k": "3", "kinds": "1",
                   "latex": r"\nu'", "display": "ν'"}}
    r2e = HomotopyElement("ν′", 3, 6, 3, Symbol("ν", decoration="′"))
    assert recognized(r2e, records) == (3, 3, 6, 3)
    assert recognized(HomotopyElement("ν′", 3, 7, 3, r2e.generator), records) is None
    assert recognized(HomotopyElement("ν′", 3, 6, 3, Symbol("ν")), records) is None
    assert recognized(Suspension(r2e), records) == (3, 4, 7, 4)
    records[3]["latex"] = r"\nu"
    assert recognized(r2e, records) is None


def test_preflight_preserves_unrelated_local_changes_and_rejects_target_edit(monkeypatch, tmp_path: Path) -> None:
    def git(*arguments: str) -> str:
        process = subprocess.run(
            ("git",) + arguments, cwd=tmp_path, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return process.stdout.strip()

    git("init", "-q")
    git("config", "user.email", "r2g@example.invalid")
    git("config", "user.name", "R2G Test")
    git("branch", "-M", "develop")
    target = tmp_path / install.RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source_fixture())
    unrelated = tmp_path / "other_tracked.py"
    unrelated.write_text("x = 1\n", encoding="utf-8")
    git("add", "--", ".")
    git("commit", "-qm", "unit baseline")
    blob = git("rev-parse", "HEAD:" + install.RELATIVE)
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "EXPECTED_HEAD_BLOB", blob)
    unrelated.write_text("x = 2\n", encoding="utf-8")
    (tmp_path / "phase171_r2f_untracked").mkdir()
    state, original, proposed = install.preflight()
    assert state == "NEEDS_PATCH"
    assert proposed != original
    assert unrelated.read_text(encoding="utf-8") == "x = 2\n"
    target.write_bytes(original + b"\n# local edit\n")
    with pytest.raises(RuntimeError, match="local tracked changes"):
        install.preflight()


def test_preflight_rejects_unknown_committed_blob(monkeypatch, tmp_path: Path) -> None:
    def git(*arguments: str) -> str:
        process = subprocess.run(
            ("git",) + arguments, cwd=tmp_path, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return process.stdout.strip()

    git("init", "-q")
    git("config", "user.email", "r2g@example.invalid")
    git("config", "user.name", "R2G Test")
    git("branch", "-M", "develop")
    target = tmp_path / install.RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source_fixture())
    git("add", "--", ".")
    git("commit", "-qm", "unit baseline")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "EXPECTED_HEAD_BLOB", "0" * 40)
    with pytest.raises(RuntimeError, match="unreviewed committed"):
        install.preflight()
