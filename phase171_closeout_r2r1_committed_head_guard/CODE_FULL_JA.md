# Phase 171 Closeout R2R1 — 変更コード全文

変更対象（置換単位）：`phase171_closeout_r2_documentation_full_output/update_docs.py` と `phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py`。

`update_docs.py`：定数 `R1R1_COMMITTED_BLOB` を追加し、`current_files()`・`main()` を関数全体で置換。import は変更なし。

`test_document_writer.py`：末尾へ `_make_committed_r1r1_fixture()`、`test_later_commit_with_reviewed_r1r1_and_same_documents_is_accepted()`、`test_unreviewed_production_commit_after_base_is_rejected()` を追加。import は変更なし。

新規：`phase171_closeout_r2r1_committed_head_guard/install.py`、`run.ps1`、`tests/test_install.py`、`__init__.py`、`tests/__init__.py`。

以下には各完全版の内容を省略せず提示する。文書5件（README と docs 以下4件）の本文は前回 R2 パッケージから変更せず、R2 成功時に5文書それぞれの全文を復元可能な ZIP として出力する。

## replacements/update_docs.py

```python
"""Phase 171 Closeout R2: guarded five-document full-file writer.

The reviewed repository files are read from the user's checked-out worktree.
All five complete revised files are exported. No full pytest is invoked.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_HEAD = "e814ec939652807d464fd76051d34a9da40328f8"
DOC_BLOBS = {
    "README.md": "cc65eea3ae9e4bf1e7d67d74550eda4f4f8b4024",
    "docs/design.md": "6f4a65431cf0e4ba2c517b521654e732568f45db",
    "docs/development_log.md": "64484312f89636c00e6d7dac670d719e81016eca",
    "docs/roadmap.md": "f6b48da7a853200c8b9323baff77731002d43026",
    "docs/proof_records.md": "0f4289bccca3558632f621596e04199e44360576",
}
SECTIONS = {
    "README.md": "readme.md",
    "docs/design.md": "design.md",
    "docs/development_log.md": "development_log.md",
    "docs/roadmap.md": "roadmap.md",
    "docs/proof_records.md": "proof_records.md",
}
SECTION_SHA256 = {
    # Filled at package build; these hashes protect reviewed document additions.
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
README_ANCHOR = "<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->"
MARKER = "PHASE171_CLOSEOUT_R2_REVIEWED_20261031"
R1R1_TEST = "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py"
R1R1_EXPECTED = "27ab6eb0a481eeb71ccf11603df4c7cbc8d2397380ca01f7d264d44f3fab2c84"
R1R1_SOURCE_BLOB = "b2b21c4fa35181fc0df45c3ef5af8433e147f891"
R1R1_COMMITTED_BLOB = "f98557eef6f2dd720c4b74ff28b8469e668df2f4"
FOCUSED = (
    "phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py",
    "phase170_r3_r12_document_closeout/tests/test_document_contract.py",
    "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py",
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.rstrip("\r\n")


def lf_text(data: bytes) -> str:
    value = data.decode("utf-8-sig")
    value = value.replace("\r\n", "\n")
    if "\r" in value:
        raise ValueError("unknown line endings")
    return value


def section_text(name: str) -> str:
    file = HERE / "sections" / name
    data = file.read_bytes()
    if hashlib.sha256(data).hexdigest() != SECTION_SHA256[name]:
        raise RuntimeError("reviewed section hash changed: " + name)
    return lf_text(data)


def updated_document(relative: str, original: bytes) -> bytes:
    if relative not in DOC_BLOBS:
        raise ValueError("unreviewed document path")
    text = lf_text(original)
    section = section_text(SECTIONS[relative])
    if MARKER in text:
        raise ValueError("Phase 171 documentation marker already exists")
    if "Phase 171" not in section or "pytest" not in section:
        raise ValueError("reviewed Phase 171 section contract failed")
    if relative == "README.md":
        anchor = README_ANCHOR + "\n"
        if text.count(anchor) != 1 or not section.startswith("<!-- " + MARKER + " -->"):
            raise ValueError("README insertion anchor missing or ambiguous")
        changed = text.replace(anchor, section + anchor, 1)
    else:
        if not (section.startswith("\n## ") or section.startswith("\n\n## ")):
            raise ValueError("append-only section marker missing")
        changed = text + section
    if changed.count(MARKER) != (1 if relative == "README.md" else 0):
        raise ValueError("Phase 171 marker count invalid")
    if relative != "README.md" and not changed.startswith(text):
        raise ValueError("historical document prefix was modified")
    raw = changed.encode("utf-8")
    if b"\r\n" in original:
        raw = raw.replace(b"\n", b"\r\n")
    if original.startswith(b"\xef\xbb\xbf"):
        raw = b"\xef\xbb\xbf" + raw
    if relative != "README.md" and not raw.startswith(original):
        raise ValueError("historical bytes not preserved")
    return raw


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp = tempfile.mkstemp(prefix=".phase171_r2_", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def current_files() -> tuple[dict[str, bytes], dict[str, bytes], set[str]]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if head != EXPECTED_HEAD:
        try:
            git("merge-base", "--is-ancestor", EXPECTED_HEAD, "HEAD")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("local HEAD is not descended from reviewed base") from exc
        committed_delta = {
            path for path in git(
                "diff", "--name-only", EXPECTED_HEAD, "HEAD", "--"
            ).splitlines() if path
        }
        allowed_delta = {
            path for path in committed_delta
            if path == R1R1_TEST
            or path.startswith("phase171_closeout_r1_preflight_audit/")
            or path.startswith("phase171_closeout_r1r1_r3z_semantic_guard/")
        }
        if committed_delta != allowed_delta:
            raise RuntimeError(
                "unreviewed committed paths after reviewed base HEAD: "
                + ", ".join(sorted(committed_delta - allowed_delta))
            )
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("local HEAD and origin/develop must match")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes present")
    committed_test_blob = git("rev-parse", "HEAD:" + R1R1_TEST)
    if committed_test_blob not in {R1R1_SOURCE_BLOB, R1R1_COMMITTED_BLOB}:
        raise RuntimeError("historical R3Z test baseline is not reviewed")
    test_file = ROOT / R1R1_TEST
    if hashlib.sha256(lf_text(test_file.read_bytes()).encode("utf-8")).hexdigest() != R1R1_EXPECTED:
        raise RuntimeError("R1R1 semantic test fix has not been installed or differs")
    before: dict[str, bytes] = {}
    after: dict[str, bytes] = {}
    for relative, blob in DOC_BLOBS.items():
        if git("rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("reviewed GitHub document blob changed: " + relative)
        source = (ROOT / relative).read_bytes()
        before[relative] = source
        committed = subprocess.run(["git", "show", "HEAD:" + relative],
                                   cwd=ROOT, capture_output=True, check=True).stdout
        if lf_text(source) != lf_text(committed):
            try:
                expected = updated_document(relative, committed)
            except Exception:
                expected = b""
            if lf_text(source) != lf_text(expected):
                raise RuntimeError("unreviewed document worktree content: " + relative)
        after[relative] = updated_document(relative, committed)
        normalized_after = lf_text(after[relative]).encode("utf-8")
        adjusted = normalized_after.replace(b"\n", b"\r\n") if b"\r\n" in source else normalized_after
        after[relative] = (b"\xef\xbb\xbf" + adjusted) if source.startswith(b"\xef\xbb\xbf") else adjusted
    tracked = {p for p in git("diff", "--name-only", "HEAD", "--").splitlines() if p}
    unexpected = tracked - {R1R1_TEST, *DOC_BLOBS}
    if unexpected:
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    if committed_test_blob == R1R1_SOURCE_BLOB and R1R1_TEST not in tracked:
        raise RuntimeError("R1R1 reviewed test change must remain in worktree")
    for relative in DOC_BLOBS:
        if relative in tracked and before[relative] != after[relative]:
            raise RuntimeError("pre-existing unreviewed document change: " + relative)
    missing = [p for p in FOCUSED if not (ROOT / p).is_file()]
    if missing:
        raise RuntimeError("missing focused test files: " + ", ".join(missing))
    return before, after, tracked


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    folder = base / "EHPProofTracerRecovery" / ("phase171_closeout_r2_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run_focused() -> dict[str, object]:
    command = [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
               "--disable-warnings", "-p", "no:cacheprovider", *FOCUSED]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(command, cwd=ROOT, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace")
    print(proc.stdout, flush=True)
    return {"command": command, "exit_code": proc.returncode, "output": proc.stdout}


def export_full_documents(folder: Path, documents: dict[str, bytes]) -> Path:
    complete = folder / "FULL_DOCUMENTS"
    for relative, content in documents.items():
        atomic_write(complete / relative, content)
    archive = folder / "PHASE171_R2_FIVE_FULL_DOCUMENTS.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as stream:
        for relative, content in documents.items():
            stream.writestr(relative, content)
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    before, after, tracked = current_files()
    head = git("rev-parse", "HEAD")
    print("PHASE171_CLOSEOUT_R2_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2_REVIEWED_BASE=" + EXPECTED_HEAD, flush=True)
    print("PHASE171_CLOSEOUT_R2_DOCS=" + ",".join(DOC_BLOBS), flush=True)
    print("PHASE171_CLOSEOUT_R2_TRACKED_BEFORE=" + ",".join(sorted(tracked)), flush=True)
    print("PHASE171_CLOSEOUT_R2_FOCUSED_FILES=" + str(len(FOCUSED)), flush=True)
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    destination = output_directory()
    for relative, value in before.items():
        atomic_write(destination / "BEFORE_FULL_DOCUMENTS" / relative, value)
    changed: list[str] = []
    report: dict[str, object] = {
        "phase": "171_CLOSEOUT_R2",
        "head": head,
        "reviewed_base": EXPECTED_HEAD,
        "full_pytest": False,
        "document_paths": list(DOC_BLOBS),
        "tracked_before": sorted(tracked),
    }
    try:
        for relative, content in after.items():
            target = ROOT / relative
            if target.read_bytes() != content:
                atomic_write(target, content)
                changed.append(relative)
        result = run_focused()
        report["focused"] = result
        if result["exit_code"]:
            raise RuntimeError("focused pytest failed")
        for relative, content in after.items():
            if (ROOT / relative).read_bytes() != content:
                raise RuntimeError("document unexpectedly changed after pytest: " + relative)
        expected_tracked = set(tracked) | set(DOC_BLOBS)
        current_tracked = set(git("diff", "--name-only", "HEAD", "--").splitlines())
        if current_tracked != expected_tracked:
            raise RuntimeError("unreviewed tracked change after tests")
        if git("diff", "--cached", "--name-only", "--"):
            raise RuntimeError("unexpected staged changes")
        archive = export_full_documents(destination, after)
        report["full_document_archive"] = str(archive)
        report["changed_documents"] = changed
        report["result"] = "PASS_FIVE_FULL_DOCUMENTS_PENDING_FULL_SUITE"
        print("PHASE171_CLOSEOUT_R2_FULL_DOCUMENTS=" + str(archive), flush=True)
        print("PHASE171_CLOSEOUT_R2_RESULT=" + str(report["result"]), flush=True)
        return 0
    except Exception as exc:
        for relative in reversed(changed):
            atomic_write(ROOT / relative, before[relative])
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["restored_documents"] = changed
        report["result"] = "FAILED_DOCUMENTS_RESTORED"
        print("PHASE171_CLOSEOUT_R2_RESULT=FAILED_DOCUMENTS_RESTORED", flush=True)
        return 1
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        output = destination / "audit.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2_REPORT=" + str(output), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
```

## replacements/tests/test_document_writer.py

```python
"""Pure checks for history-safe full-document replacement and source boundaries."""
from __future__ import annotations

import pytest

from phase171_closeout_r2_documentation_full_output.update_docs import (
    DOC_BLOBS,
    MARKER,
    README_ANCHOR,
    updated_document,
    section_text,
    SECTIONS,
)


@pytest.mark.parametrize("relative", tuple(DOC_BLOBS))
def test_generates_complete_documents_without_erasing_history(relative: str):
    if relative == "README.md":
        old = ("# EHP Proof Tracer\n\n" + README_ANCHOR
               + "\n\n## Phase 170 historical content\n").encode("utf-8")
    else:
        old = ("# 昔の記録\n\n歴史的な説明を保持する。\n" + relative + "\n").encode("utf-8")
    new = updated_document(relative, old)
    assert new != old
    assert b"Phase 171" in new
    if relative == "README.md":
        assert new.startswith(b"# EHP Proof Tracer\n\n")
        assert new.endswith(b"## Phase 170 historical content\n")
        assert new.count(MARKER.encode("ascii")) == 1
    else:
        assert new.startswith(old)
        assert old in new
        assert "Phase 171" in section_text(SECTIONS[relative])


def test_readme_fails_closed_without_reviewed_anchor():
    with pytest.raises(ValueError, match="anchor"):
        updated_document("README.md", b"# Not the reviewed README\n")


def test_duplicate_document_update_is_refused():
    old = ("# EHP Proof Tracer\n" + README_ANCHOR + "\n").encode("utf-8")
    updated = updated_document("README.md", old)
    with pytest.raises(ValueError, match="already exists"):
        updated_document("README.md", updated)


def test_crlf_and_bom_preserved_for_append_only_document():
    old = b"\xef\xbb\xbf" + "# 日本語記録\r\n\r\n過去の本文。\r\n".encode("utf-8")
    new = updated_document("docs/proof_records.md", old)
    assert new.startswith(old)
    assert b"\r\n" in new
    assert b"\n" not in new.replace(b"\r\n", b"")


def test_other_paths_refused():
    with pytest.raises(ValueError, match="unreviewed"):
        updated_document("README_OTHER.md", b"# Not reviewed\n")


def test_no_phase_end_full_pytest_claim():
    for relative in DOC_BLOBS:
        content = section_text(SECTIONS[relative])
        assert "Phase 171" in content
        assert "pytest" in content
        assert "88" in content
    readme = section_text("readme.md")
    assert "has **not** yet been run" in readme


def test_guarded_full_document_end_to_end_on_local_fixture(tmp_path, monkeypatch):
    """A fixture repository exercises Git guards, byte retention and complete ZIP."""
    import hashlib
    import os
    from pathlib import Path
    import subprocess
    import zipfile
    from phase171_closeout_r2_documentation_full_output import update_docs as module

    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    subprocess.run(["git", "init", "-b", "develop", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "test"], check=True)
    originals = {}
    for relative in DOC_BLOBS:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "README.md":
            source = ("# EHP Proof Tracer\n\n" + README_ANCHOR + "\n## Historical\n").encode("utf-8")
        else:
            source = ("# 過去の文書\n\n" + relative + "\n").encode("utf-8")
        path.write_bytes(source)
        originals[relative] = source
    test_file = repo / module.R1R1_TEST
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_bytes(b"# historical test\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "baseline"], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "-u", "origin", "develop"], check=True)
    def repo_git(*args):
        return subprocess.run(["git", "-C", str(repo), *args],
                              check=True, capture_output=True, text=True).stdout.strip()
    reviewed_head = repo_git("rev-parse", "HEAD")
    blobs = {relative: repo_git("rev-parse", "HEAD:" + relative) for relative in DOC_BLOBS}
    old_test_sha = repo_git("rev-parse", "HEAD:" + module.R1R1_TEST)
    revised = b"# semantic proof preservation test\n"
    test_file.write_bytes(revised)
    monkeypatch.setattr(module, "ROOT", repo)
    monkeypatch.setattr(module, "EXPECTED_HEAD", reviewed_head)
    monkeypatch.setattr(module, "DOC_BLOBS", blobs)
    monkeypatch.setattr(module, "R1R1_SOURCE_BLOB", old_test_sha)
    monkeypatch.setattr(module, "R1R1_EXPECTED", hashlib.sha256(revised).hexdigest())
    monkeypatch.setattr(module, "FOCUSED", ())
    monkeypatch.setattr(module, "run_focused", lambda: {"exit_code": 0, "output": "fixture pass"})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    monkeypatch.setattr("sys.argv", ["update_docs.py"])
    assert module.main() == 0
    changed = set(repo_git("diff", "--name-only", "HEAD", "--").splitlines())
    assert changed == set(DOC_BLOBS) | {module.R1R1_TEST}
    for relative in DOC_BLOBS:
        actual = (repo / relative).read_bytes()
        assert actual == module.updated_document(relative, originals[relative])
        if relative != "README.md":
            assert actual.startswith(originals[relative])
    archives = list((tmp_path / "localappdata" / "EHPProofTracerRecovery").glob("*/PHASE171_R2_FIVE_FULL_DOCUMENTS.zip"))
    assert len(archives) == 1
    with zipfile.ZipFile(archives[0]) as handle:
        for relative in DOC_BLOBS:
            assert handle.read(relative) == (repo / relative).read_bytes()
    assert module.main() == 0


def _make_committed_r1r1_fixture(tmp_path, monkeypatch):
    """Prepare two local commits: reviewed docs, then an R1R1-only correction."""
    import hashlib
    from pathlib import Path
    import subprocess
    from phase171_closeout_r2_documentation_full_output import update_docs as module

    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    subprocess.run(["git", "init", "-b", "develop", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "test"], check=True)
    for relative in module.DOC_BLOBS:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "README.md":
            data = ("# EHP Proof Tracer\n\n" + README_ANCHOR + "\n## Historical\n").encode("utf-8")
        else:
            data = ("# 既存記録\n\n" + relative + "\n").encode("utf-8")
        path.write_bytes(data)
    test_file = repo / module.R1R1_TEST
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_bytes(b"# old R3Z assertion\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "reviewed base"], check=True)

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repo), *args], check=True,
            capture_output=True, text=True, encoding="utf-8",
        ).stdout.strip()

    reviewed_head = git("rev-parse", "HEAD")
    blobs = {path: git("rev-parse", "HEAD:" + path) for path in module.DOC_BLOBS}
    old_test_blob = git("rev-parse", "HEAD:" + module.R1R1_TEST)
    revised = b"# corrected semantic R3Z test\n"
    test_file.write_bytes(revised)
    audit_file = repo / "phase171_closeout_r1_preflight_audit" / "run.ps1"
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    audit_file.write_text("# audited wrapper\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "commit R1R1"], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "-u", "origin", "develop"], check=True)
    monkeypatch.setattr(module, "ROOT", repo)
    monkeypatch.setattr(module, "EXPECTED_HEAD", reviewed_head)
    monkeypatch.setattr(module, "DOC_BLOBS", blobs)
    monkeypatch.setattr(module, "R1R1_SOURCE_BLOB", old_test_blob)
    monkeypatch.setattr(module, "R1R1_COMMITTED_BLOB", git("rev-parse", "HEAD:" + module.R1R1_TEST))
    monkeypatch.setattr(module, "R1R1_EXPECTED", hashlib.sha256(revised).hexdigest())
    monkeypatch.setattr(module, "FOCUSED", ())
    return repo, git, module


def test_later_commit_with_reviewed_r1r1_and_same_documents_is_accepted(tmp_path, monkeypatch):
    repo, git, module = _make_committed_r1r1_fixture(tmp_path, monkeypatch)
    before, after, tracked = module.current_files()
    assert tracked == set()
    assert git("rev-parse", "HEAD") != module.EXPECTED_HEAD
    assert len(before) == len(after) == 5
    for path in module.DOC_BLOBS:
        assert (repo / path).read_bytes() == before[path]
        assert after[path].startswith(before[path]) or path == "README.md"
    assert all((repo / path).read_bytes() == before[path] for path in module.DOC_BLOBS)


def test_unreviewed_production_commit_after_base_is_rejected(tmp_path, monkeypatch):
    repo, git, module = _make_committed_r1r1_fixture(tmp_path, monkeypatch)
    production = repo / "phase165_r52_r9_shared_math.py"
    production.write_text("# not an audited Phase 171 closeout change\n", encoding="utf-8")
    import subprocess
    subprocess.run(["git", "-C", str(repo), "add", "phase165_r52_r9_shared_math.py"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "unreviewed source edit"], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "origin", "develop"], check=True)
    with pytest.raises(RuntimeError, match="unreviewed committed paths"):
        module.current_files()
```

## install.py

```python
"""Phase 171 Closeout R2R1: guarded replacement of an R2-only HEAD check."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R2 = ROOT / "phase171_closeout_r2_documentation_full_output"
REPLACEMENTS = {
    "update_docs.py": "replacements/update_docs.py",
    "tests/test_document_writer.py": "replacements/tests/test_document_writer.py",
}
OLD_HASHES = {
    "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
    "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
}
SECTIONS = {
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
DOCUMENTS = (
    "README.md", "docs/design.md", "docs/development_log.md",
    "docs/roadmap.md", "docs/proof_records.md",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="._phase171_r2r1_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def inspect() -> tuple[str, dict[Path, bytes], dict[Path, bytes], bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("HEAD must match local origin/develop")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if not (R2 / "run.ps1").is_file():
        raise RuntimeError("original R2 runner missing")
    before: dict[Path, bytes] = {}
    replacement: dict[Path, bytes] = {}
    states: list[str] = []
    for relative, source in REPLACEMENTS.items():
        path = R2 / relative
        asset = HERE / source
        existing = path.read_bytes()
        corrected = asset.read_bytes()
        current_hash = sha(existing)
        if current_hash == OLD_HASHES[relative]:
            states.append("OLD")
        elif current_hash == sha(corrected):
            states.append("CORRECTED")
        else:
            raise RuntimeError("unreviewed R2 source content: " + relative)
        before[path] = existing
        replacement[path] = corrected
    if len(set(states)) != 1:
        raise RuntimeError("mixed R2 correction states refused")
    for name, expected in SECTIONS.items():
        value = (R2 / "sections" / name).read_bytes()
        if sha(value) != expected:
            raise RuntimeError("unreviewed Phase 171 document section: " + name)
    for document in DOCUMENTS:
        if not (ROOT / document).is_file():
            raise RuntimeError("missing document: " + document)
    print("PHASE171_CLOSEOUT_R2R1_BRANCH=develop", flush=True)
    print("PHASE171_CLOSEOUT_R2R1_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R1_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R2R1_ALREADY_CORRECTED=" + str(states[0] == "CORRECTED"), flush=True)
    return head, before, replacement, states[0] == "CORRECTED"


def record_root() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    folder = base / ("phase171_closeout_r2r1_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, before, replacement, already = inspect()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R1_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    destination = record_root()
    doc_before = {ROOT / doc: (ROOT / doc).read_bytes() for doc in DOCUMENTS}
    for path, content in before.items():
        relative = path.relative_to(ROOT)
        atomic_write(destination / "BEFORE" / relative, content)
    changed: list[Path] = []
    report: dict[str, object] = {
        "phase": "171_CLOSEOUT_R2R1",
        "head": head,
        "full_pytest": False,
        "already_corrected": already,
        "patch_paths": [str(path.relative_to(ROOT)) for path in before],
    }
    result_code = 1
    try:
        for path, content in replacement.items():
            if before[path] != content:
                atomic_write(path, content)
                changed.append(path)
        proc = subprocess.run(
            [sys.executable, "-B", str(R2 / "update_docs.py")],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n", flush=True)
        report["r2_exit_code"] = proc.returncode
        if proc.returncode:
            raise RuntimeError("corrected R2 full-document writer failed")
        if any(path.read_bytes() != content for path, content in replacement.items()):
            raise RuntimeError("corrected R2 source changed unexpectedly")
        report["result"] = "PASS_R2_DOCUMENTS_PENDING_PHASE_END_FULL_SUITE"
        print("PHASE171_CLOSEOUT_R2R1_RESULT=" + str(report["result"]), flush=True)
        result_code = 0
    except Exception as exc:
        for path in reversed(changed):
            atomic_write(path, before[path])
        for path, original in doc_before.items():
            if path.read_bytes() != original:
                atomic_write(path, original)
        report["result"] = "FAIL_RESTORED"
        report["error"] = str(exc)
        print("PHASE171_CLOSEOUT_R2R1_RESULT=FAIL_RESTORED", flush=True)
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        output = destination / "audit.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R1_REPORT=" + str(output), flush=True)
    return result_code


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

```powershell
param(
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Previous = (Get-Location).Path
try {
    Set-Location $Root
    $env:PYTHONUTF8 = "1"
    $env:PYTHONDONTWRITEBYTECODE = "1"
    if (-not $DryRun) {
        & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider `
          (Join-Path $PSScriptRoot "tests\test_install.py")
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 Closeout R2R1 installer guard tests failed"
        }
    }
    $PythonArguments = @("-B", (Join-Path $PSScriptRoot "install.py"))
    if ($DryRun) {
        $PythonArguments += "--dry-run"
    }
    & python @Args
    $Result = $LASTEXITCODE
    if ($Result -ne 0) {
        throw "Phase 171 Closeout R2R1 failed with exit $Result"
    }
}
finally {
    Set-Location $Previous
}
```

## tests/test_install.py

```python
"""Isolated guards for exact R2 script replacement, without project mathematics."""
from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from phase171_closeout_r2r1_committed_head_guard import install


@pytest.fixture
def worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root = tmp_path / "repo"
    r2 = root / "phase171_closeout_r2_documentation_full_output"
    r2.mkdir(parents=True)
    for relative in install.REPLACEMENTS:
        target = r2 / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        reviewed_name = Path(relative).name
        (target).write_bytes(
            (install.HERE / "reviewed_originals" / reviewed_name).read_bytes()
        )
    for name in install.SECTIONS:
        section = r2 / "sections" / name
        section.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(install.HERE.parent / "phase171_closeout_r2_documentation_full_output" / "sections" / name,
                     section)
    (r2 / "run.ps1").write_text("# reviewed launcher", encoding="utf-8")
    for relative in install.DOCUMENTS:
        document = root / relative
        document.parent.mkdir(parents=True, exist_ok=True)
        document.write_text("# existing document\n", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", root)
    monkeypatch.setattr(install, "R2", r2)
    monkeypatch.setattr(install, "git", lambda *args: {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "committed-r1r1",
        ("rev-parse", "origin/develop"): "committed-r1r1",
        ("diff", "--cached", "--name-only", "--"): "",
    }[args])
    return root, r2


@pytest.mark.parametrize("corrected", [False, True])
def test_only_whole_reviewed_old_or_corrected_states_pass(worktree, corrected):
    _, r2 = worktree
    if corrected:
        for relative, asset in install.REPLACEMENTS.items():
            (r2 / relative).write_bytes((install.HERE / asset).read_bytes())
    head, before, replacement, already = install.inspect()
    assert head == "committed-r1r1"
    assert len(before) == len(replacement) == 2
    assert already is corrected


def test_unknown_and_mixed_install_states_are_refused(worktree):
    _, r2 = worktree
    (r2 / "update_docs.py").write_bytes(b"unreviewed source")
    with pytest.raises(RuntimeError, match="unreviewed R2 source"):
        install.inspect()
    (r2 / "update_docs.py").write_bytes((install.HERE / install.REPLACEMENTS["update_docs.py"]).read_bytes())
    with pytest.raises(RuntimeError, match="mixed R2 correction states"):
        install.inspect()


def test_unreviewed_document_section_is_refused(worktree):
    _, r2 = worktree
    (r2 / "sections" / "readme.md").write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unreviewed Phase 171 document section"):
        install.inspect()
```
