# Phase 171 Closeout R2R4 — 変更コード全文

変更対象: `phase171_closeout_r2r3_mixed_line_ending_fix/install.py`。import 変更なし。追加定数 `REVIEWED_R2_BASE_SHA256` は既存 `REVIEWED_OLD_SHA256` の直前。変更関数 `preflight` はモジュール内の既存位置。以下にモジュール全文を掲載。

## 既存ファイル：修正後全文

```python

"""Phase 171 R2R3: guarded historical-byte-preserving document writer fix."""
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
REVIEWED_OLD_SHA256 = {
    "update_docs.py": "b8e11ea6f762ca7fc6699cc45a7878f448ab966fc1eee316ad1e63f7f8e65dae",
    "tests/test_document_writer.py": "5ce255360fcdafd1498bbec6f4fefb8fa862e2c5f792b686f266aa98aadadf65",
}
REVIEWED_R2_BASE_SHA256 = {
    # R2R1 and R2R3 restore these exact originals after a failed write.
    "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
    "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
}
EXPECTED_NEW_SHA256 = {
    "update_docs.py": "8b39e61e57d171b2bf451137fd28730fca283364f726740a0cb543b808fd05d1",
    "tests/test_document_writer.py": "d0da01d85904e496ac9297275b2108cbd00be1fb0bdf887ae5badb00114a0b1e",
}
BASE = "3e74849bf90bc115c16503ddd46d49996baa0856"
DOCUMENT_BLOBS = {
    "README.md": "cc65eea3ae9e4bf1e7d67d74550eda4f4f8b4024",
    "docs/design.md": "6f4a65431cf0e4ba2c517b521654e732568f45db",
    "docs/development_log.md": "64484312f89636c00e6d7dac670d719e81016eca",
    "docs/roadmap.md": "f6b48da7a853200c8b9323baff77731002d43026",
    "docs/proof_records.md": "0f4289bccca3558632f621596e04199e44360576",
}
SECTIONS = {
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
TEST_BLOB = "f98557eef6f2dd720c4b74ff28b8469e668df2f4"
R1R1_TEST = "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py"


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".phase171_r2r3_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def preflight() -> tuple[dict[Path, bytes], dict[Path, bytes], bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("local HEAD and origin/develop differ")
    try:
        git("merge-base", "--is-ancestor", BASE, "HEAD")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("local HEAD not descended from reviewed base") from exc
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if head != BASE:
        delta = set(filter(None, git("diff", "--name-only", BASE, "HEAD", "--").splitlines()))
        if any(not (p.startswith("phase171_closeout_r2_documentation_full_output/")
                    or p.startswith("phase171_closeout_r2r")) for p in delta):
            raise RuntimeError("unreviewed committed changes after base")
    if git("rev-parse", "HEAD:" + R1R1_TEST) != TEST_BLOB:
        raise RuntimeError("semantic R1R1 test blob changed")
    for relative, blob in DOCUMENT_BLOBS.items():
        if git("rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("reviewed document blob changed: " + relative)
    for name, expected in SECTIONS.items():
        if sha((R2 / "sections" / name).read_bytes()) != expected:
            raise RuntimeError("reviewed document section changed: " + name)
    if not (R2 / "run.ps1").is_file():
        raise RuntimeError("original R2 runner missing")
    if not (ROOT / "phase171_closeout_r2r1_committed_head_guard" / "run.ps1").is_file():
        raise RuntimeError("R2R1 runner missing")
    before = {}
    corrected = {}
    states = []
    for relative, asset in REPLACEMENTS.items():
        path = R2 / relative
        original = path.read_bytes()
        patch = (HERE / asset).read_bytes()
        if sha(patch) != EXPECTED_NEW_SHA256[relative]:
            raise RuntimeError("replacement source checksum mismatch: " + relative)
        actual = sha(original)
        if actual == REVIEWED_R2_BASE_SHA256[relative]:
            states.append("R2_BASE")
        elif actual == REVIEWED_OLD_SHA256[relative]:
            states.append("R2R1")
        elif actual == EXPECTED_NEW_SHA256[relative]:
            states.append("NEW")
        else:
            raise RuntimeError("unreviewed R2 source: " + relative)
        before[path] = original
        corrected[path] = patch
    if len(set(states)) != 1:
        raise RuntimeError("mixed state of R2 source and tests")
    unexpected = set(filter(None, git("diff", "--name-only", "HEAD", "--").splitlines())) - set(DOCUMENT_BLOBS)
    if unexpected:
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    print("PHASE171_CLOSEOUT_R2R3_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R3_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R2R3_ALREADY_CORRECTED=" + str(states[0] == "NEW"), flush=True)
    return before, corrected, states[0] == "NEW"


def report_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    output = base / ("phase171_closeout_r2r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    return output


def invoke(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n", flush=True)
    if proc.stderr:
        print(proc.stderr, flush=True)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    before, corrected, already = preflight()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R3_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    output = report_dir()
    doc_before = {ROOT / doc: (ROOT / doc).read_bytes() for doc in DOCUMENT_BLOBS}
    for path, data in {**before, **doc_before}.items():
        atomic_write(output / "BEFORE" / path.relative_to(ROOT), data)
    changed = []
    report = {"phase": "171_CLOSEOUT_R2R3", "head": git("rev-parse", "HEAD"),
              "full_pytest": False, "already_corrected": already}
    try:
        for path, data in corrected.items():
            if path.read_bytes() != data:
                atomic_write(path, data)
                changed.append(path)
        code, result = invoke([
            sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
            "--disable-warnings", "-p", "no:cacheprovider",
            str(HERE / "tests" / "test_install.py"),
            "phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py",
        ])
        report["repair_pytest_exit"] = code
        if code:
            raise RuntimeError("R2R3 safety and regression pytest failed")
        code, result = invoke([sys.executable, "-B", str(R2 / "update_docs.py"), "--dry-run"])
        report["r2_dry_run_exit"] = code
        if code:
            raise RuntimeError("R2 document preflight failed")
        code, result = invoke([sys.executable, "-B", str(R2 / "update_docs.py")])
        report["r2_exit"] = code
        if code:
            raise RuntimeError("R2 full-document write or focused pytest failed")
        if any(path.read_bytes() != value for path, value in corrected.items()):
            raise RuntimeError("source changed during R2 focused tests")
        report["result"] = "PASS_FIVE_DOCUMENTS_PENDING_PHASE_END"
        print("PHASE171_CLOSEOUT_R2R3_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END", flush=True)
        return 0
    except Exception as exc:
        for path in reversed(changed):
            atomic_write(path, before[path])
        for path, data in doc_before.items():
            if path.read_bytes() != data:
                atomic_write(path, data)
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["result"] = "FAIL_RESTORED"
        print("PHASE171_CLOSEOUT_R2R3_RESULT=FAIL_RESTORED", flush=True)
        return 1
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R3_REPORT=" + str(output / "audit.json"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規実行スクリプト：全文

```python

"""Phase 171 R2R4: repair R2R3 content guard for restored original R2 files.

The only persistent code edit is R2R3/install.py. The reviewed R2R3
installer subsequently owns the five document outputs and their rollback.
"""
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
R2R3 = ROOT / "phase171_closeout_r2r3_mixed_line_ending_fix"
TARGET = R2R3 / "install.py"
REVIEWED_HEAD = "3e74849bf90bc115c16503ddd46d49996baa0856"
REVIEWED_OLD_INSTALL = "71016ec5e80c55b353d131922d27ffcb3ef68bc48572ed090060512670f74a0b"
REVIEWED_NEW_INSTALL = "12b26ec3a0591a6498e9f9953b640c31d9a5104f829dc136a9cba091ef4fdbbd"
REVIEWED_PAIRS = {
    "R2_BASE": {
        "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
        "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
    },
    "R2R1": {
        "update_docs.py": "b8e11ea6f762ca7fc6699cc45a7878f448ab966fc1eee316ad1e63f7f8e65dae",
        "tests/test_document_writer.py": "5ce255360fcdafd1498bbec6f4fefb8fa862e2c5f792b686f266aa98aadadf65",
    },
    "R2R3": {
        "update_docs.py": "8b39e61e57d171b2bf451137fd28730fca283364f726740a0cb543b808fd05d1",
        "tests/test_document_writer.py": "d0da01d85904e496ac9297275b2108cbd00be1fb0bdf887ae5badb00114a0b1e",
    },
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def write_atomic(path: Path, contents: bytes) -> None:
    fd, temp = tempfile.mkstemp(prefix=".phase171_r2r4_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(contents)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def detect_reviewed_pair() -> str:
    actual = {name: sha((R2 / name).read_bytes()) for name in REVIEWED_PAIRS["R2_BASE"]}
    for state, expected in REVIEWED_PAIRS.items():
        if actual == expected:
            return state
    raise RuntimeError("unreviewed or mixed R2 writer/test source bytes: " + str(actual))


def preflight() -> tuple[bytes, bytes, bool, str]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if head != REVIEWED_HEAD or git("rev-parse", "origin/develop") != head:
        raise RuntimeError("unreviewed HEAD or origin/develop")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if git("diff", "--name-only", "HEAD", "--"):
        raise RuntimeError("unexpected tracked changes before R2 closeout")
    original = TARGET.read_bytes()
    correction = (HERE / "replacements" / "install.py").read_bytes()
    state = detect_reviewed_pair()
    if sha(correction) != REVIEWED_NEW_INSTALL:
        raise RuntimeError("R2R4 replacement installer integrity failure")
    if sha((HERE / "reviewed_originals" / "install.py").read_bytes()) != REVIEWED_OLD_INSTALL:
        raise RuntimeError("R2R4 inspected installer source integrity failure")
    before_hash = sha(original)
    if before_hash not in {REVIEWED_OLD_INSTALL, REVIEWED_NEW_INSTALL}:
        raise RuntimeError("unreviewed R2R3 installer content")
    for name, expected in REVIEWED_PAIRS["R2_BASE"].items():
        if sha((HERE / "reviewed_originals" / name).read_bytes()) != expected:
            raise RuntimeError("R2R4 inspected original R2 source changed: " + name)
    if not (R2R3 / "run.ps1").is_file():
        raise RuntimeError("R2R3 runner missing")
    print("PHASE171_CLOSEOUT_R2R4_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R4_R2_SOURCE_STATE=" + state, flush=True)
    print("PHASE171_CLOSEOUT_R2R4_ALREADY_CORRECTED=" + str(before_hash == REVIEWED_NEW_INSTALL), flush=True)
    print("PHASE171_CLOSEOUT_R2R4_CONTENT_GUARD=PASS", flush=True)
    return original, correction, before_hash == REVIEWED_NEW_INSTALL, state


def run(command: list[str]) -> int:
    result = subprocess.run(command, cwd=ROOT,
                            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace")
    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
    return result.returncode


def output_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    directory = base / ("phase171_closeout_r2r4_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    original, correction, already, state = preflight()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R4_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    output = output_dir()
    (output / "BEFORE_R2R3_installer.py").write_bytes(original)
    report = {"phase": "171_CLOSEOUT_R2R4", "head": REVIEWED_HEAD,
              "source_state": state, "already_corrected": already, "full_pytest": False}
    success = False
    try:
        if original != correction:
            write_atomic(TARGET, correction)
        # This extra test covers the original R2 pair that caused the regression.
        code = run([sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                    "--disable-warnings", "-p", "no:cacheprovider",
                    str(HERE / "tests" / "test_repair.py")])
        report["guard_pytest_exit"] = code
        if code:
            raise RuntimeError("R2R4 guard pytest failed")
        code = run([sys.executable, "-B", str(TARGET), "--dry-run"])
        report["r2r3_dry_run_exit"] = code
        if code:
            raise RuntimeError("R2R3 preflight after guard repair failed")
        code = run([sys.executable, "-B", str(TARGET)])
        report["r2r3_exit"] = code
        if code:
            raise RuntimeError("R2R3 full-document update failed")
        if TARGET.read_bytes() != correction:
            raise RuntimeError("R2R3 installer modified unexpectedly")
        expected_docs = {"README.md", "docs/design.md", "docs/development_log.md",
                         "docs/roadmap.md", "docs/proof_records.md"}
        tracked = set(filter(None, git("diff", "--name-only", "HEAD", "--").splitlines()))
        if tracked != expected_docs:
            raise RuntimeError("expected exactly five changed documents; found " + str(sorted(tracked)))
        success = True
        report["result"] = "PASS_FIVE_DOCUMENTS_PENDING_PHASE_END"
        print("PHASE171_CLOSEOUT_R2R4_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "FAIL_RESTORED_R2R4_INSTALLER"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE171_CLOSEOUT_R2R4_ERROR=" + str(exc), flush=True)
        return 1
    finally:
        if not success and TARGET.read_bytes() != original:
            write_atomic(TARGET, original)
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R4_REPORT=" + str(output / "audit.json"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規安全検査：import・全テスト関数全文

```python

"""Safety regression checks for the restored-source guard and its runner."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_closeout_r2r4_restored_source_guard import repair as g
from phase171_closeout_r2r3_mixed_line_ending_fix import install as r


def _hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def test_all_reviewed_replacements_match_exact_hashes():
    assert _hash((g.HERE / 'reviewed_originals/install.py').read_bytes()) == g.REVIEWED_OLD_INSTALL
    assert _hash((g.HERE / 'replacements/install.py').read_bytes()) == g.REVIEWED_NEW_INSTALL
    for name, expected in g.REVIEWED_PAIRS['R2_BASE'].items():
        assert _hash((g.HERE / 'reviewed_originals' / name).read_bytes()) == expected


def test_r2r4_installer_is_only_r2r3_guard_extension():
    old = (g.HERE / 'reviewed_originals/install.py').read_text(encoding='utf-8')
    new = (g.HERE / 'replacements/install.py').read_text(encoding='utf-8')
    assert 'REVIEWED_R2_BASE_SHA256' not in old
    assert 'REVIEWED_R2_BASE_SHA256' in new
    assert new.count('states.append("R2_BASE")') == 1
    assert new.count('states.append("R2R1")') == 1
    assert old.count('states.append("OLD")') == 1
    assert new.count('states.append("NEW")') == 1
    assert 'if len(set(states)) != 1:' in new


def test_power_shell_runner_uses_explicit_argument_variable():
    runner = (g.HERE / 'run.ps1').read_text(encoding='utf-8')
    assert '& python @PythonArguments' in runner
    assert '"--dry-run"' in runner
    assert '& python @Args' not in runner


def _prepare_guard_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    root = tmp_path / 'repo'
    r2 = root / 'phase171_closeout_r2_documentation_full_output'
    r2r3 = root / 'phase171_closeout_r2r3_mixed_line_ending_fix'
    for name in g.REVIEWED_PAIRS['R2_BASE']:
        path = r2 / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((g.HERE / 'reviewed_originals' / name).read_bytes())
    target = r2r3 / 'install.py'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((g.HERE / 'reviewed_originals/install.py').read_bytes())
    (r2r3 / 'run.ps1').write_text('# reviewed runner\n', encoding='utf-8')
    monkeypatch.setattr(g, 'ROOT', root)
    monkeypatch.setattr(g, 'R2', r2)
    monkeypatch.setattr(g, 'R2R3', r2r3)
    monkeypatch.setattr(g, 'TARGET', target)

    def fake_git(*args):
        if args == ('branch', '--show-current'):
            return 'develop'
        if args in (('rev-parse', 'HEAD'), ('rev-parse', 'origin/develop')):
            return g.REVIEWED_HEAD
        if args in (('diff', '--cached', '--name-only', '--'), ('diff', '--name-only', 'HEAD', '--')):
            return ''
        raise AssertionError(args)

    monkeypatch.setattr(g, 'git', fake_git)
    return r2, target


def test_repaired_guard_accepts_exact_restored_r2_original_pair(tmp_path, monkeypatch):
    r2, target = _prepare_guard_fixture(tmp_path, monkeypatch)
    before, after, already, state = g.preflight()
    assert state == 'R2_BASE'
    assert not already
    assert before == (g.HERE / 'reviewed_originals/install.py').read_bytes()
    target.write_bytes(after)
    _, _, already, state = g.preflight()
    assert already and state == 'R2_BASE'


def test_guard_rejects_mixed_base_and_intermediate_r2_pair(tmp_path, monkeypatch):
    r2, _ = _prepare_guard_fixture(tmp_path, monkeypatch)
    intermediate = r.HERE / 'reviewed_originals' / 'tests' / 'test_document_writer.py'
    (r2 / 'tests' / 'test_document_writer.py').write_bytes(intermediate.read_bytes())
    with pytest.raises(RuntimeError, match='unreviewed or mixed'):
        g.preflight()


def test_guard_rejects_unknown_r2_writer(tmp_path, monkeypatch):
    r2, _ = _prepare_guard_fixture(tmp_path, monkeypatch)
    (r2 / 'update_docs.py').write_text('unexpected edit\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='unreviewed or mixed'):
        g.preflight()


def test_guard_rejects_unreviewed_existing_r2r3_installer(tmp_path, monkeypatch):
    _, target = _prepare_guard_fixture(tmp_path, monkeypatch)
    target.write_text('unreviewed installer\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='unreviewed R2R3 installer'):
        g.preflight()


def test_guard_rejects_unreviewed_git_tracked_change(tmp_path, monkeypatch):
    _prepare_guard_fixture(tmp_path, monkeypatch)
    original = g.git
    def git(*args):
        if args == ('diff', '--name-only', 'HEAD', '--'):
            return 'phase165_r52_r9_shared_math.py'
        return original(*args)
    monkeypatch.setattr(g, 'git', git)
    with pytest.raises(RuntimeError, match='unexpected tracked changes'):
        g.preflight()


def test_patched_r2r3_preflight_accepts_original_restored_r2_source(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    r2 = root / 'phase171_closeout_r2_documentation_full_output'
    r2r1 = root / 'phase171_closeout_r2r1_committed_head_guard'
    for relative in r.REPLACEMENTS:
        destination = r2 / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((g.HERE / 'reviewed_originals' / relative).read_bytes())
    for name in r.SECTIONS:
        path = r2 / 'sections' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((r.HERE / 'reviewed_sections' / name).read_bytes())
    (r2 / 'run.ps1').write_text('# fixture\n', encoding='utf-8')
    r2r1.mkdir(parents=True)
    (r2r1 / 'run.ps1').write_text('# fixture\n', encoding='utf-8')
    monkeypatch.setattr(r, 'ROOT', root)
    monkeypatch.setattr(r, 'R2', r2)

    def git(*args):
        if args == ('branch', '--show-current'):
            return 'develop'
        if args in (('rev-parse', 'HEAD'), ('rev-parse', 'origin/develop')):
            return r.BASE
        if args == ('merge-base', '--is-ancestor', r.BASE, 'HEAD'):
            return ''
        if args == ('rev-parse', 'HEAD:' + r.R1R1_TEST):
            return r.TEST_BLOB
        if len(args) == 2 and args[0] == 'rev-parse' and args[1].startswith('HEAD:'):
            return r.DOCUMENT_BLOBS[args[1][5:]]
        if args in (('diff', '--cached', '--name-only', '--'), ('diff', '--name-only', 'HEAD', '--')):
            return ''
        raise AssertionError(args)

    monkeypatch.setattr(r, 'git', git)
    original_source = r.preflight()
    assert original_source[2] is False
    assert len(original_source[0]) == 2
    for file, content in original_source[1].items():
        file.write_bytes(content)
    assert r.preflight()[2] is True


def test_r2r3_preflight_preserves_previous_r2r1_acceptance(tmp_path, monkeypatch):
    from phase171_closeout_r2r3_mixed_line_ending_fix.tests.test_install import _fixture
    r2 = _fixture(tmp_path, monkeypatch)
    original = r.preflight()
    assert original[2] is False
    for path, content in original[1].items():
        path.write_bytes(content)
    assert r.preflight()[2] is True


def test_r2r3_preflight_refuses_two_different_reviewed_states(tmp_path, monkeypatch):
    from phase171_closeout_r2r3_mixed_line_ending_fix.tests.test_install import _fixture
    r2 = _fixture(tmp_path, monkeypatch)
    original = (g.HERE / 'reviewed_originals' / 'update_docs.py').read_bytes()
    (r2 / 'update_docs.py').write_bytes(original)
    with pytest.raises(RuntimeError, match='mixed state'):
        r.preflight()

```

## PowerShell Runner：全文

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
    $PythonArguments = @("-B", (Join-Path $PSScriptRoot "repair.py"))
    if ($DryRun) {
        $PythonArguments += "--dry-run"
    }
    & python @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 171 Closeout R2R4 failed with exit $LASTEXITCODE"
    }
}
finally {
    Set-Location $Previous
}

```
