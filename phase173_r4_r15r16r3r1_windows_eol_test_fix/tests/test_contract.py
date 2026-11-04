"""Pure validation that only the platform-specific byte expectation changes."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

from phase173_r4_r15r16r3r1_windows_eol_test_fix import install


def test_corrected_file_replaces_exactly_one_assertion() -> None:
    before = install.BASELINE.read_text(encoding="utf-8")
    after = install.CORRECTED.read_text(encoding="utf-8")
    old = '    assert target.read_bytes() == original + b"# tested patch\\n"\n'
    new = ('    expected_eol = b"\\r\\n" if b"\\r\\n" in original else b"\\n"\n'
           '    assert target.read_bytes() == original + b"# tested patch" + expected_eol\n')
    assert before.count(old) == 1
    assert after == before.replace(old, new)
    assert sha256(before.encode("utf-8")).hexdigest() == install.BASELINE_HASH
    assert sha256(after.encode("utf-8")).hexdigest() == install.CORRECTED_HASH


def test_projection_preserves_existing_newline_style() -> None:
    replacement = b"one\ntwo\n"
    assert install.project(replacement, b"first\n") == replacement
    assert install.project(replacement, b"first\r\n") == b"one\r\ntwo\r\n"


def test_corrected_test_is_python_syntax_valid() -> None:
    source = install.CORRECTED.read_text(encoding="utf-8")
    compile(source, str(Path(install.CORRECTED)), "exec")


def test_guarded_install_and_restore_preserve_git_index(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repo"
    root.mkdir()

    def git(*arguments: str) -> str:
        proc = subprocess.run(
            ["git", *arguments], cwd=root, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout.strip()

    git("init", "-q", "-b", "develop")
    git("config", "user.name", "Test Runner")
    git("config", "user.email", "test@example.org")
    target = root / install.RELATIVE
    target.parent.mkdir(parents=True)
    target.write_bytes(install.BASELINE.read_bytes())
    another = root / "other.txt"
    another.write_text("unchanged\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-qm", "reviewed baseline")
    head = git("rev-parse", "HEAD")
    git("update-ref", "refs/remotes/origin/develop", head)
    another.write_text("staged user content\n", encoding="utf-8")
    git("add", "other.txt")
    index_before = git("write-tree")

    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "REVIEWED_HEAD", head)
    assert install.guard() == "baseline"
    install.install()
    assert target.read_bytes() == install.CORRECTED.read_bytes()
    assert git("write-tree") == index_before
    assert another.read_text(encoding="utf-8") == "staged user content\n"
    install.restore()
    assert target.read_bytes() == install.BASELINE.read_bytes()
    assert git("write-tree") == index_before


def test_staged_test_divergence_is_rejected(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repo"
    root.mkdir()

    def git(*arguments: str) -> str:
        proc = subprocess.run(
            ["git", *arguments], cwd=root, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout.strip()

    git("init", "-q", "-b", "develop")
    git("config", "user.name", "Test Runner")
    git("config", "user.email", "test@example.org")
    target = root / install.RELATIVE
    target.parent.mkdir(parents=True)
    target.write_bytes(install.BASELINE.read_bytes())
    git("add", ".")
    git("commit", "-qm", "reviewed baseline")
    head = git("rev-parse", "HEAD")
    git("update-ref", "refs/remotes/origin/develop", head)
    target.write_bytes(install.CORRECTED.read_bytes())
    git("add", install.RELATIVE.as_posix())
    target.write_bytes(install.BASELINE.read_bytes())
    staged_before = git("write-tree")

    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "REVIEWED_HEAD", head)
    try:
        install.guard()
    except RuntimeError as error:
        assert "staged test differs from pre-install working tree" in str(error)
    else:
        raise AssertionError("divergent staged test was accepted")
    assert git("write-tree") == staged_before
