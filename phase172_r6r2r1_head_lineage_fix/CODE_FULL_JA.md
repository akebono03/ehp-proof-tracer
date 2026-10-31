# Phase 172 R6R2R1 — 変更・追加コード全文

変更対象となる既存ファイルは `phase172_r6r2_document_closeout/install.py` のみ。変更後 import 部分はファイル全文に含めて記載する。追加定数 `ALLOWED_R6_AUDIT_BLOBS` は既存 `TARGETS` 定数の直後、追加関数 `reviewed_head_lineage()` は既存 `preflight()` の直前に置く。変更した `preflight()` は全文を提示する。テストを含むその他のコードはすべて新規追加で、ファイル全文を提示する。

文書5ファイルそのものは、既存 R6R2 `sections.py` の確定済み内容を使い、検証済みの現在の全文に適用される。書き換え直前に更新後の**各ファイル全文**が `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r6r2_document_closeout_*\full_documents/` に保存される。`docs/development_log.md` と `docs/proof_records.md` は追記方針。既存の本番数学コードとクラスの変更はない。

## 既存 `phase172_r6r2_document_closeout/install.py`（修正後・ファイル全文）

```python
"""Phase 172 R6R2: five-document closeout using one already passed R6 gate.

This installer NEVER runs the full pytest suite and NEVER changes production
code. All five *complete* revised documents are saved before optional apply.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from .sections import APPENDS, MARKER, make_revision

ROOT = Path(__file__).resolve().parent.parent
REPORT_NAME = "phase172_r6_20261031_144642_024616Z"
REVIEWED_HEAD = "6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a"
DOC_BLOBS = {
    "README.md": "98fef702205b8a0aea416e6958557657520d7479",
    "docs/design.md": "b0f6e2c77aeb5817127ce2c38d390bfa3ff67433",
    "docs/development_log.md": "afb83495fbaef9dc28ccceb944b758cd9608232a",
    "docs/roadmap.md": "415e8af933c43da99ea0ae987ec7dd9ae1673398",
    "docs/proof_records.md": "1b39992cff566eb3bf7540ff32ede2b262f2056e",
}
REVIEWED_RENDERER_BLOB = "6bfd5e992f6c9ee9441920e10e63e0db4bece289"
TARGETS = ((2, 1), (3, 1), (3, 2), (4, 2), (3, 3))
# The only descendants permitted are the reviewed R6 audit-package additions.
# The R6 evidence continues to refer to REVIEWED_HEAD and is never rewritten.
ALLOWED_R6_AUDIT_BLOBS = {
    "phase172_r6_phase_closeout/AUDIT_PLAN_JA.md": "ff6c29dafe9e59add082e53ed9498acf2b16be00",
    "phase172_r6_phase_closeout/CODE_FULL_JA.md": "12a135d5d60797fbf051681d7f4fd6dd5988506f",
    "phase172_r6_phase_closeout/README.md": "3a95ce8ebaea02bee591578a53505790cfb63714",
    "phase172_r6_phase_closeout/__init__.py": "30d67c049bf8510b101f4a43d99b1724d0387bba",
    "phase172_r6_phase_closeout/audit.py": "815e130736daf6f255c6f8028dc03ea19e6ce78a",
    "phase172_r6_phase_closeout/run.ps1": "24441bf560525ddeab48f03360114de104500588",
    "phase172_r6_phase_closeout/tests/test_gate.py": "d06e0c63dc10b04f259d6b33c11c7544035b4c4e",
}


def command(*args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=timeout,
        check=False,
    )


def checked(*args: str) -> str:
    process = command(*args)
    if process.returncode:
        raise RuntimeError("command failed: " + repr(args) + " " + process.stderr[-1200:])
    return process.stdout.strip()


def read_closeout_report(directory: Path) -> dict[str, object]:
    """Inspect immutable, *previously run* R6 evidence; do not repeat pytest."""
    path = directory / "closeout.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("result") != "PASS_PHASE172_R6_FULL_CLOSEOUT_GATE":
        raise RuntimeError("R6 closeout did not pass")
    if report.get("phase") != "172-R6" or report.get("tracked_unchanged") is not True:
        raise RuntimeError("R6 phase or tracked-state gate is invalid")
    state = report.get("state", {})
    if (state.get("head") != REVIEWED_HEAD
            or state.get("origin_develop") != REVIEWED_HEAD
            or state.get("renderer_state") != "R5_COMMITTED"):
        raise RuntimeError("R6 reviewed HEAD/renderer state differs")
    focused = report.get("focused", [])
    if (not isinstance(focused, list) or len(focused) != 10
            or {row.get("group") for row in focused} != set(range(1, 11))
            or any(row.get("exit_code") != 0 for row in focused)):
        raise RuntimeError("R6 focused test gate is incomplete")
    groups = report.get("public_groups", [])
    if (not isinstance(groups, list) or len(groups) != 5
            or {(row.get("n"), row.get("k")) for row in groups} != set(TARGETS)
            or any(row.get("web_key") != "generic-complete-proof"
                   or row.get("partial") is not False for row in groups)):
        raise RuntimeError("R6 Web gate is incomplete")
    pi63 = next(row for row in groups if (row["n"], row["k"]) == (3, 3))
    if (pi63.get("proof_steps") != 50 or pi63.get("reference_count") != 8
            or pi63.get("open_goals") != 0
            or pi63.get("internal_db_prior_references") != [2, 8]
            or pi63.get("presentation_gate") != "PASS"
            or pi63.get("trust_boundary") != "PASS"):
        raise RuntimeError("R6 pi63 proof/Reference gate is invalid")
    full = report.get("active_full_pytest", {})
    if (full.get("passed") != 3546 or full.get("exit_code") != 0):
        raise RuntimeError("R6 active suite PASS summary is invalid")
    log = (directory / "full_active_pytest.log").read_text(encoding="utf-8")
    if len(re.findall(r"\b3546 passed in 107\.52s", log)) != 1:
        raise RuntimeError("R6 full pytest evidence does not match the report")
    markdown = (directory / "pi_6_3_web_narrative.md").read_text(encoding="utf-8")
    for token in (
        "[R2] 先行データベース結果", "[R8] 先行データベース結果",
        r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.",
        r"\operatorname{ord}(\nu')=4", r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}",
    ):
        if token not in markdown:
            raise RuntimeError("R6 final Web evidence lacks " + token)
    if "DB prior: sphere.csv" in markdown.split("\n証明\n", 1)[0]:
        raise RuntimeError("R5 public locator improvement missing")
    return report


def reviewed_head_lineage(head: str) -> tuple[str, ...]:
    """Accept R6 itself or only the seven reviewed later audit-file additions.

    A subsequent commit cannot change documentation, proof sources, Renderer,
    or any unrelated file. Compare *the complete ancestry diff* instead of
    trusting a message or accepting any descendant. Git blob IDs must match
    independently reviewed content. No checkout/reset/fetch is performed.
    """
    if head == REVIEWED_HEAD:
        return ()
    ancestry = command(
        "git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head,
        timeout=35,
    )
    if ancestry.returncode != 0:
        raise RuntimeError("current HEAD does not descend from the R6 verified commit")
    changes = checked(
        "git", "diff", "--name-status", "--no-renames",
        REVIEWED_HEAD, head, "--",
    )
    rows = changes.splitlines()
    if not rows or len(rows) != len(ALLOWED_R6_AUDIT_BLOBS):
        raise RuntimeError("unexpected commit changes after the R6 verified commit")
    accepted: list[str] = []
    for row in rows:
        if row.count("\t") != 1:
            raise RuntimeError("malformed R6 descendant change record")
        status, path = row.split("\t", 1)
        if (status != "A" or path not in ALLOWED_R6_AUDIT_BLOBS
                or path in accepted):
            raise RuntimeError("unreviewed change after R6 gate: " + row)
        if checked("git", "rev-parse", "HEAD:" + path) != ALLOWED_R6_AUDIT_BLOBS[path]:
            raise RuntimeError("R6 audit file content differs: " + path)
        accepted.append(path)
    if set(accepted) != set(ALLOWED_R6_AUDIT_BLOBS):
        raise RuntimeError("incomplete reviewed R6 audit-package addition")
    return tuple(accepted)


def preflight(directory: Path) -> dict[str, str]:
    if checked("git", "branch", "--show-current") != "develop":
        raise RuntimeError("the develop branch is required")
    head = checked("git", "rev-parse", "HEAD")
    accepted_additions = reviewed_head_lineage(head)
    remote = command("git", "ls-remote", "origin", "refs/heads/develop", timeout=35)
    if remote.returncode or not remote.stdout.strip():
        raise RuntimeError("origin/develop unavailable")
    if remote.stdout.split()[0] != head:
        raise RuntimeError("origin/develop differs from the reviewed HEAD")
    if checked("git", "status", "--porcelain", "-uno"):
        raise RuntimeError("unexpected existing tracked changes")
    if checked("git", "diff", "--cached", "--name-only"):
        raise RuntimeError("the Git index contains changes")
    for path, blob in DOC_BLOBS.items():
        if checked("git", "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("reviewed document Git blob differs: " + path)
        if not (ROOT / path).is_file():
            raise RuntimeError("document is absent: " + path)
    if checked("git", "rev-parse", "HEAD:phase168_r3_5_model_renderer.py") != REVIEWED_RENDERER_BLOB:
        raise RuntimeError("Renderer is not the completed R5 implementation")
    read_closeout_report(directory)
    return {"branch": "develop", "head": head, "remote": head,
            "document_guard": "PASS", "r6_report": str(directory),
            "r6_audit_additions": str(len(accepted_additions))}


def output_dir() -> Path:
    appdata = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    parent = appdata / "EHPProofTracerRecovery"
    parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    directory = parent / ("phase172_r6r2_document_closeout_" + now)
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def revised_documents() -> tuple[dict[str, bytes], dict[str, bytes]]:
    originals: dict[str, bytes] = {}
    updated: dict[str, bytes] = {}
    for path in DOC_BLOBS:
        original = (ROOT / path).read_bytes()
        revision = make_revision(path, original)
        if revision == original or MARKER.encode("utf-8") not in revision:
            raise RuntimeError("document generation did not add Phase 172 closure")
        originals[path] = original
        updated[path] = revision
    return originals, updated


def save_full_documents(output: Path, originals: dict[str, bytes], updated: dict[str, bytes]) -> None:
    """Write FIVE complete replacement files, not truncated diffs."""
    for path in DOC_BLOBS:
        destination = output / "full_documents" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(updated[path])
        original = output / "backup_original" / path
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_bytes(originals[path])
        if destination.read_bytes() != updated[path]:
            raise RuntimeError("failed to verify complete document: " + path)


def run_focused_tests(output: Path) -> None:
    filename = output / "focused_pytest.log"
    process = command(sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                      "-p", "no:cacheprovider",
                      "phase172_r6r2_document_closeout/tests/test_sections.py", timeout=120)
    filename.write_text(process.stdout + "\n" + process.stderr, encoding="utf-8")
    if process.returncode:
        raise RuntimeError("document-only focused pytest failed: " + process.stdout[-1200:])
    print("PHASE172_R6R2_DOCUMENT_TESTS=PASS", flush=True)


def restore(originals: dict[str, bytes]) -> None:
    for path, value in originals.items():
        (ROOT / path).write_bytes(value)


def apply_documents(originals: dict[str, bytes], updated: dict[str, bytes]) -> None:
    """Install reviewed full files, then check all five names and exact bytes."""
    try:
        for path, data in updated.items():
            destination = ROOT / path
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=destination.parent, delete=False,
                prefix=".phase172_r6r2_", suffix=".tmp",
            ) as stream:
                stream.write(data)
                temporary = Path(stream.name)
            try:
                os.replace(temporary, destination)
            finally:
                temporary.unlink(missing_ok=True)
        changed = set(checked("git", "diff", "--name-only").splitlines())
        if changed != set(DOC_BLOBS):
            raise RuntimeError("unexpected changed file set: " + repr(sorted(changed)))
        if command("git", "diff", "--check").returncode:
            raise RuntimeError("git diff --check failed")
        for path, data in updated.items():
            if (ROOT / path).read_bytes() != data:
                raise RuntimeError("complete document bytes differ: " + path)
    except BaseException:
        restore(originals)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report-dir", default=None)
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("choose exactly one of --dry-run or --apply")
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "EHPProofTracerRecovery"
    report_dir = Path(args.report_dir) if args.report_dir else base / REPORT_NAME
    state = preflight(report_dir)
    print("PHASE172_R6R2_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R6R2_HEAD=" + state["head"], flush=True)
    print("PHASE172_R6R2_R6_EVIDENCE=PASS", flush=True)
    print("PHASE172_R6R2_DOC_CONTENT_GUARD=PASS", flush=True)
    output = output_dir()
    originals, updated = revised_documents()
    save_full_documents(output, originals, updated)
    print("PHASE172_R6R2_FULL_DOCUMENTS=" + str(output / "full_documents"), flush=True)
    if args.dry_run:
        print("PHASE172_R6R2_DRY_RUN=PASS", flush=True)
        print("PHASE172_R6R2_SOURCE_CHANGES=0", flush=True)
        return 0
    run_focused_tests(output)
    apply_documents(originals, updated)
    record = {
        "phase": "172-R6R2", "result": "PASS_PHASE172_DOCUMENT_CLOSEOUT",
        "phase_end_gate": "PASS_PHASE172_R6_FULL_CLOSEOUT_GATE",
        "r6_head": REVIEWED_HEAD, "active_full_pytest": {"passed": 3546, "seconds": 107.52},
        "full_suite_executed_in_this_document_step": False,
        "documents": list(DOC_BLOBS),
        "full_documents": str(output / "full_documents"),
    }
    (output / "document_closeout.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE172_R6R2_DOCUMENTS=5", flush=True)
    print("PHASE172_R6R2_FULL_SUITE_EXECUTED=NO", flush=True)
    print("PHASE172_R6R2_RESULT=PASS_PHASE172_DOCUMENT_CLOSEOUT", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 `phase172_r6r2r1_head_lineage_fix/fix.py`（全文）

```python
"""Guarded R6R2 head-lineage correction; then reuse the original doc runner.

No mathematical proof, Renderer, source citations, or Phase 172 full test gate is
changed or run. On failure the previously supplied installer is restored.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase172_r6r2_document_closeout" / "install.py"
PAYLOAD = PACKAGE / "payload" / "install.py"
ORIGINAL_SHA256 = "457a1e68d0c35592293946933de3d0f32f8214ae8cde952a7783751997775d4f"
CORRECTED_SHA256 = "83cd837d58b8204347c5cecbc3b1c33f182e4d85dab7f1d3020231c43d00a281"
R6_REPORT = "phase172_r6_20261031_144642_024616Z"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def command(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, check=False, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)


def run_checked(*args: str, timeout: int = 120) -> str:
    result = command(*args, timeout=timeout)
    output = result.stdout + "\n" + result.stderr
    print(output, end="\n" if not output.endswith("\n") else "", flush=True)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {args!r}")
    return output


def candidate_module():
    """Import complete corrected source for preflight without installing it."""
    spec = importlib.util.spec_from_file_location(
        "phase172_r6r2_document_closeout._reviewed_candidate", PAYLOAD,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("corrected installer cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = ROOT
    return module


def checked_payload() -> tuple[bytes, bytes]:
    if not TARGET.is_file() or not PAYLOAD.is_file():
        raise RuntimeError("original or corrected installer file is missing")
    old, revised = TARGET.read_bytes(), PAYLOAD.read_bytes()
    if digest(old) != ORIGINAL_SHA256:
        raise RuntimeError("installer does not match reviewed original; no changes")
    if digest(revised) != CORRECTED_SHA256:
        raise RuntimeError("corrected payload does not match reviewed bytes")
    return old, revised


def atomic_write(target: Path, data: bytes) -> None:
    """Replace complete source, never a fragment; preserve restoration bytes."""
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=target.parent, delete=False,
        prefix=".phase172_r6r2r1_", suffix=".tmp",
    ) as stream:
        stream.write(data)
        temp = Path(stream.name)
    try:
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def report_dir() -> Path:
    appdata = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    return appdata / "EHPProofTracerRecovery" / R6_REPORT


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("select exactly one of --dry-run and --apply")
    original, revised = checked_payload()
    candidate = candidate_module()
    state = candidate.preflight(report_dir())
    print("PHASE172_R6R2R1_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R6R2R1_HEAD=" + state["head"], flush=True)
    print("PHASE172_R6R2R1_R6_AUDIT_FILES=" + state["r6_audit_additions"], flush=True)
    print("PHASE172_R6R2R1_REVIEWED_R6_EVIDENCE=PASS", flush=True)
    print("PHASE172_R6R2R1_PAYLOAD_GUARD=PASS", flush=True)
    if args.dry_run:
        print("PHASE172_R6R2R1_SOURCE_CHANGES=0", flush=True)
        print("PHASE172_R6R2R1_DRY_RUN=PASS", flush=True)
        return 0
    atomic_write(TARGET, revised)
    try:
        if digest(TARGET.read_bytes()) != CORRECTED_SHA256:
            raise RuntimeError("installer replacement not byte-for-byte exact")
        run_checked(
            sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
            "-p", "no:cacheprovider",
            "phase172_r6r2r1_head_lineage_fix/tests/test_fix.py",
            timeout=120,
        )
        print("PHASE172_R6R2R1_FOCUSED_TESTS=PASS", flush=True)
        # The original guarded full-document installer writes full replacement
        # documents and its output backup; it runs only document-only pytest.
        run_checked(
            sys.executable, "-B", "-m",
            "phase172_r6r2_document_closeout.install", "--apply",
            timeout=180,
        )
    except BaseException:
        atomic_write(TARGET, original)
        if digest(TARGET.read_bytes()) != ORIGINAL_SHA256:
            raise RuntimeError("unable to restore original installer after failure")
        print("PHASE172_R6R2R1_RESTORED_INSTALLER=PASS", flush=True)
        raise
    print("PHASE172_R6R2R1_FULL_SUITE_EXECUTED=NO", flush=True)
    print("PHASE172_R6R2R1_RESULT=PASS_DOCUMENT_CLOSEOUT_CORRECTED", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 `phase172_r6r2r1_head_lineage_fix/tests/test_fix.py`（全文）

```python
"""Focused tests for the corrected commit-lineage and source gates."""
from __future__ import annotations

from subprocess import CompletedProcess

import pytest

from phase172_r6r2r1_head_lineage_fix.fix import (
    CORRECTED_SHA256,
    ORIGINAL_SHA256,
    PAYLOAD,
    candidate_module,
    digest,
)


def prepared(monkeypatch):
    module = candidate_module()
    changes = "\n".join("A\t" + path for path in module.ALLOWED_R6_AUDIT_BLOBS)
    observed = []

    def fake_command(*args, **kwargs):
        observed.append(args)
        return CompletedProcess(args, 0, stdout="", stderr="")

    def fake_checked(*args):
        observed.append(args)
        if args[:3] == ("git", "diff", "--name-status"):
            return changes
        if args[:2] == ("git", "rev-parse"):
            path = args[-1][5:]
            return module.ALLOWED_R6_AUDIT_BLOBS[path]
        raise AssertionError("unexpected Git command: " + repr(args))

    monkeypatch.setattr(module, "command", fake_command)
    monkeypatch.setattr(module, "checked", fake_checked)
    return module, observed


def test_original_verified_r6_commit_requires_no_descendant_diff(monkeypatch):
    module, calls = prepared(monkeypatch)
    assert module.reviewed_head_lineage(module.REVIEWED_HEAD) == ()
    assert calls == []


def test_one_reviewed_r6_audit_commit_is_allowed(monkeypatch):
    module, calls = prepared(monkeypatch)
    accepted = module.reviewed_head_lineage("later-reviewed-commit")
    assert set(accepted) == set(module.ALLOWED_R6_AUDIT_BLOBS)
    assert ("git", "merge-base", "--is-ancestor", module.REVIEWED_HEAD,
            "later-reviewed-commit") in calls


def test_non_descendant_commit_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    monkeypatch.setattr(
        module, "command",
        lambda *args, **kwargs: CompletedProcess(args, 1, stdout="", stderr=""),
    )
    with pytest.raises(RuntimeError, match="does not descend"):
        module.reviewed_head_lineage("unrelated-branch")


def test_unrelated_file_addition_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    lines = lines.replace("phase172_r6_phase_closeout/README.md",
                          "src/unreviewed.py")
    original = module.checked

    def f(*args):
        if args[:3] == ("git", "diff", "--name-status"):
            return lines
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="unreviewed change"):
        module.reviewed_head_lineage("modified-source")


def test_modified_existing_file_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    lines = lines.replace("A\tphase172_r6_phase_closeout/audit.py",
                          "M\tphase172_r6_phase_closeout/audit.py")
    original = module.checked

    def f(*args):
        if args[:3] == ("git", "diff", "--name-status"):
            return lines
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="unreviewed change"):
        module.reviewed_head_lineage("modified-audit-file")


def test_reviewed_audit_file_content_difference_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    original = module.checked

    def f(*args):
        if args[:2] == ("git", "rev-parse"):
            return "0" * 40
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="content differs"):
        module.reviewed_head_lineage("wrong-blob")


def test_missing_or_duplicate_audit_additions_are_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    original = module.checked
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    duplicate = lines.splitlines()
    duplicate[-1] = duplicate[0]

    for changed in ("\n".join(lines.splitlines()[:-1]), "\n".join(duplicate)):
        def f(*args):
            if args[:3] == ("git", "diff", "--name-status"):
                return changed
            return original(*args)
        monkeypatch.setattr(module, "checked", f)
        with pytest.raises(RuntimeError):
            module.reviewed_head_lineage("invalid-additions")


def test_payload_is_a_complete_reviewed_replacement():
    source = PAYLOAD.read_bytes()
    assert digest(source) == CORRECTED_SHA256
    assert ORIGINAL_SHA256 != CORRECTED_SHA256
    assert b"def reviewed_head_lineage" in source
    assert b"def preflight" in source
    assert b"def apply_documents" in source
    assert b"def read_closeout_report" in source
    assert b"from .sections import APPENDS, MARKER, make_revision" in source
```

## 新規 `phase172_r6r2r1_head_lineage_fix/run.ps1`（全文）

```powershell
param(
    [switch]$DryRun,
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
if ($DryRun -eq $Apply) {
    throw 'Choose exactly one of -DryRun and -Apply'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $mode = if ($DryRun) { '--dry-run' } else { '--apply' }
    & python -B -m phase172_r6r2r1_head_lineage_fix.fix $mode
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R6R2R1 correction failed: $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
```

## 新規 `phase172_r6r2r1_head_lineage_fix/__init__.py`（全文）

```python
"""Phase 172 R6R2R1: reviewed descendant HEAD fix, document-only."""
```
