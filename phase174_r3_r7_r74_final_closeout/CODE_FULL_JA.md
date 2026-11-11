# Phase 174 R74 — 変更対象・コード全文・テスト・終了条件

## 変更対象

今回新規追加するディレクトリは `phase174_r3_r7_r74_final_closeout/` のみ。以下の新規ファイルをそのまま作成する。

- `__init__.py`：新規モジュール。
- `audit.py`：Git／資料／過去レポートの Source Guard、単一回の全体テスト、証拠保存、主要5文書の全文出力。
- `tests/test_audit.py`：新規の限定仕様テスト24件（パラメータ展開を含む）。
- `run.ps1`：DryRun と本実行、限定 pytest、最終 Gate。
- `README.md`：英語の実行説明。
- `updates/README.md`、`updates/design.md`、`updates/development_log.md`、`updates/roadmap.md`、`updates/proof_records.md`：最終 Gate 成功時の追記全文。`audit.py` が各ファイルの既存本文を保持したまま**ファイル全文**を生成し、`output/full_files/` と ZIP に出力する。
- `AUDIT_NOTES_JA.md`：監査仕様、`TEST_RESULTS_JA.md`：本パッケージの作成時テスト。

変更する既存 Python ファイル・クラス・関数・メソッド・import はない。新規関数と import は下記 `audit.py` の完全版に含む。将来 Phase の機能を追加しない。

## 実行する pytest

限定 pytest：

```powershell
python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib phase174_r3_r7_r74_final_closeout/tests/test_audit.py phase174_r3_r7_r73_closeout_documents/tests/test_audit.py
```

全体 pytest（**Phase 174 の最後に一回だけ**）：

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

通常の利用時は `run.ps1` が上記を順に制御するため、全体 pytest を手動で重複実行しない。

## 完了条件と次 Phase 境界

実際の全体 pytest が終了コード0で PASS し、検証済み出典・Git・文書がテスト前後で維持され、主要5文書の全文および最終レポートを保存したときに限り `PASS_R74_PHASE174_FINAL_CLOSEOUT` を出力する。既存の証明木・一般規則・GIVEN・共通表示に数学上の追加変更はない。全体 pytest が失敗した場合はログを保存し、正式終了しない。次 Phase の未完成群の証明拡張は一切先取りしない。

## __init__.py（全文）

```python
"""Phase 174 R74 final audit-only gate and complete documentation output."""
```

## audit.py（全文）

```python
"""Phase 174 R74: one-shot active-suite gate and full-document closeout.

Preflight is read-only. A full pytest is executed only once after all guards
and focused tests pass. On failure, preserve the attempt/log/report and leave
canonical documents untouched. On success, emit and install five full files.
No mathematical inference rules, GIVEN, ProofSteps, or renderers are modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

PACKAGE = "phase174_r3_r7_r74_final_closeout"
R73_HEAD = "12e56cd06a3f896924313c978a628445d90228ed"
MERGED_R73_HEAD = "38788cec179c16fba7bba606ed35aa1e890ee79f"
R72_HEAD = "b66099598177d74e979492f1d04a916e6f0821a8"
R71_HEAD = "01c5246a011b43e10ed85699a6048f117562a748"
PREPARATION_MARKER = "PHASE174_R73_CLOSEOUT_PREPARATION_20261111"
FINAL_MARKER = "PHASE174_FINAL_CLOSEOUT_20261111"
DOC_SHA256 = {
    "README.md": "58ea7516ad035440e4d0bb8ae0eebcbc97648fae4c06899f477bb2f9301ce3f7",
    "docs/design.md": "ed71c80a6707e57b0e46a867904f0cb4850894a24e0a32008e456fc2e28298d8",
    "docs/development_log.md": "1f5510833e77776c24b752fecf9f34f5ce861f4972fb108974333a3c0aebfff3",
    "docs/roadmap.md": "b01a6986f8bbafd27e1acb77aee238dbe50ba3347e22446e6ef5d3a9ab0db49e",
    "docs/proof_records.md": "41979fb47b68b5e014297c990eb4326ba60ee8f3cdd1d85d9cac25f67f9aa293",
}
PINS = {
    "phase174_r3_r7_r71_common_narrative_regression/audit.py": "cdf68bc499395c115526d783ffcdb9b180c50a28",
    "phase174_r3_r7_r72_closeout_preflight/audit.py": "c6f6621ef6cbd121981436d79b79ac18bf73d26a",
    "phase174_r3_r7_r73_closeout_documents/audit.py": "86f5777e5d72a7a577bcb0124e3a9e40b34f60ea",
    "phase174_r3_r7_r73_closeout_documents/tests/test_audit.py": "3d448d0b54345b6d5e43c08b5a6fb20c693190ae",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "tests/conftest.py": "304c7b40eb1041475fb6bc4519d3ef61fd3275e2",
}
TEMPLATES = {
    "README.md": "README.md",
    "docs/design.md": "design.md",
    "docs/development_log.md": "development_log.md",
    "docs/roadmap.md": "roadmap.md",
    "docs/proof_records.md": "proof_records.md",
}
ACTIVE_SUITE = ("-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings",
                "-p", "no:cacheprovider", "tests")


def git_blob_sha(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "--no-pager", *args], cwd=root,
                            text=True, encoding="utf-8", errors="replace",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    if result.returncode != 0:
        raise RuntimeError("R74_GIT_FAILED: " + " ".join(args)
                           + " " + result.stderr.strip())
    return result.stdout.strip()


def ensure_source_pins(root: Path) -> None:
    for name, expected in PINS.items():
        original = (root / name).read_bytes()
        lf = original.replace(b"\r\n", b"\n")
        if b"\r" in lf:
            raise RuntimeError("R74_SOURCE_EOL_INVALID: " + name)
        variants = (original, lf, lf.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(data) for data in variants}:
            raise RuntimeError("R74_SOURCE_PIN_CHANGED: " + name)


def validate_r73_report(report: object) -> None:
    if not isinstance(report, dict) or report.get("phase") != "174-R73":
        raise RuntimeError("R74_R73_REPORT_INVALID")
    if (report.get("head_at_document_write") != R73_HEAD
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("whole_test_suite_executed") is not False
            or report.get("phase174_closed") is not False
            or report.get("production_changes") != []):
        raise RuntimeError("R74_R73_REPORT_SCOPE_CHANGED")
    documents = report.get("documents")
    if not isinstance(documents, list) or len(documents) != 5:
        raise RuntimeError("R74_R73_DOCUMENT_COUNT_CHANGED")
    by_path = {item.get("path"): item for item in documents if isinstance(item, dict)}
    if len(by_path) != 5 or set(by_path) != set(DOC_SHA256):
        raise RuntimeError("R74_R73_DOCUMENT_SET_CHANGED")
    for path, expected in DOC_SHA256.items():
        if by_path[path].get("full_file_sha256") != expected:
            raise RuntimeError("R74_R73_REPORT_HASH_CHANGED: " + path)
        if type(by_path[path].get("full_file_bytes")) is not int:
            raise RuntimeError("R74_R73_REPORT_BYTES_CHANGED: " + path)


def validate_r72_report(report: object) -> None:
    if not isinstance(report, dict) or report.get("phase") != "174-R72":
        raise RuntimeError("R74_R72_REPORT_INVALID")
    if (report.get("local_head") != R72_HEAD
            or report.get("r71_complete_case_count") != 8
            or report.get("r71_focused_pytest_passed") != 81
            or report.get("whole_test_suite_executed") is not False
            or report.get("phase174_closed") is not False):
        raise RuntimeError("R74_R72_SCOPE_CHANGED")
    items = report.get("incomplete_public_cases")
    if not isinstance(items, list) or {
        (x.get("group"), x.get("status"), x.get("web_key"))
        for x in items if isinstance(x, dict)
    } != {
        ("pi_12^4", "SEARCH_FAILED", "generic-partial-proof"),
        ("pi_35^4", "SEARCH_FAILED", "generic-partial-proof"),
    } or len(items) != 2:
        raise RuntimeError("R74_INCOMPLETE_BOUNDARY_CHANGED")


def evidence_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit"


def get_prior_evidence() -> dict[str, str]:
    directory = evidence_dir()
    names = {
        "r72": "phase174_r3_r7_r72_closeout_preflight",
        "r73": "phase174_r3_r7_r73_closeout_documents",
    }
    paths = {key: directory / folder / "report.json"
             for key, folder in names.items()}
    r72 = json.loads(paths["r72"].read_text(encoding="utf-8-sig"))
    r73 = json.loads(paths["r73"].read_text(encoding="utf-8-sig"))
    validate_r72_report(r72)
    validate_r73_report(r73)
    return {key: str(value) for key, value in paths.items()}


def preflight(root: Path) -> dict[str, object]:
    """Require either pristine R73-merged tree or exact pre-merge five-file edit."""
    actual = Path(git(root, "rev-parse", "--show-toplevel")).resolve()
    if actual != root.resolve():
        raise RuntimeError("R74_NOT_AT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R74_NOT_DEVELOP")
    head, remote = git(root, "rev-parse", "HEAD"), git(root, "rev-parse", "origin/develop")
    if head != remote or head not in (R73_HEAD, MERGED_R73_HEAD):
        raise RuntimeError("R74_HEAD_NOT_REVIEWED: " + head + " vs " + remote)
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("R74_STAGED_CHANGES_PRESENT")
    tracked = set(git(root, "diff", "--name-only").splitlines()) - {""}
    expected = set(DOC_SHA256) if head == R73_HEAD else set()
    if tracked != expected:
        raise RuntimeError("R74_TRACKED_CHANGES_UNEXPECTED: " + repr(sorted(tracked)))
    ensure_source_pins(root)
    for name, expected_sha in DOC_SHA256.items():
        raw = (root / name).read_bytes()
        if sha256(raw).hexdigest() != expected_sha:
            raise RuntimeError("R74_R73_DOCUMENT_CHANGED: " + name)
        source = raw.decode("utf-8-sig")
        if (source.count(PREPARATION_MARKER) != 1
                or "PHASE173_FINAL_CLOSEOUT_20261105" not in source
                or FINAL_MARKER in source):
            raise RuntimeError("R74_DOCUMENT_PHASE_BOUNDARY_CHANGED: " + name)
    prior = get_prior_evidence()
    return {"head": head, "origin_develop": remote,
            "tracked_documents": sorted(tracked), "source_pins": len(PINS),
            "r72_report": prior["r72"], "r73_report": prior["r73"],
            "doc_sha256": dict(DOC_SHA256)}


def parse_pytest_summary(output: str, exit_code: int) -> tuple[int, str]:
    """Never turn a nonzero exit or an interrupted run into a passed gate."""
    if type(exit_code) is not int or exit_code != 0:
        raise RuntimeError("R74_FULL_PYTEST_NONZERO_EXIT: " + str(exit_code))
    lines = [line.strip() for line in output.splitlines()
             if re.search(r"\b[0-9]+ passed\b", line)
             and re.search(r"\bin\s+[0-9]", line)]
    if len(lines) != 1:
        raise RuntimeError("R74_PYTEST_SUMMARY_MISSING_OR_AMBIGUOUS")
    summary = lines[0]
    if re.search(r"\b[1-9][0-9]*\s+(failed|error|errors|xpassed)\b", summary):
        raise RuntimeError("R74_PYTEST_SUMMARY_HAS_FAILURES")
    count = int(re.search(r"\b([0-9]+) passed\b", summary).group(1))
    if count < 1:
        raise RuntimeError("R74_PYTEST_PASSED_ZERO")
    return count, summary


def choose_eol(original: bytes) -> bytes:
    return b"\r\n" if original.count(b"\r\n") > original.count(b"\n") // 2 else b"\n"


def render_final_document(name: str, original: bytes, template: str,
                          context: dict[str, str]) -> bytes:
    """Build the entire replacement file while preserving all R73 history."""
    if name not in DOC_SHA256:
        raise ValueError("R74_UNKNOWN_DOCUMENT")
    base_text = original.decode("utf-8-sig")
    if (base_text.count(PREPARATION_MARKER) != 1
            or FINAL_MARKER in base_text
            or "PHASE173_FINAL_CLOSEOUT_20261105" not in base_text):
        raise RuntimeError("R74_INVALID_BASE_DOCUMENT: " + name)
    if template.count(FINAL_MARKER) != 1:
        raise RuntimeError("R74_FINAL_TEMPLATE_MARKER_ERROR")
    if name == "README.md" and "formally closed" not in template:
        raise RuntimeError("R74_README_NOT_ENGLISH")
    if name != "README.md" and "正式終了" not in template:
        raise RuntimeError("R74_JAPANESE_CLOSEOUT_MISSING")
    if not all(k in context for k in ("passed", "summary", "head", "stdout_sha256")):
        raise RuntimeError("R74_CLOSEOUT_CONTEXT_INCOMPLETE")
    # String templating substitutes only values read from actual gate evidence.
    final_section = template
    for key, value in context.items():
        final_section = final_section.replace("{{" + key + "}}", str(value))
    if "{{" in final_section or "}}" in final_section:
        raise RuntimeError("R74_TEMPLATE_UNRESOLVED_PLACEHOLDERS")
    sep = choose_eol(original)
    addition = final_section.strip("\n").replace("\r\n", "\n").replace("\n", sep.decode()).encode("utf-8")
    if name == "README.md":
        marker = b"<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->"
        if original.count(marker) != 1:
            raise RuntimeError("R74_PREPARATION_ANCHOR_NOT_UNIQUE")
        output = original.replace(marker, addition + sep + sep + marker, 1)
        if output.replace(addition + sep + sep, b"", 1) != original:
            raise RuntimeError("R74_README_HISTORY_CHANGED")
    else:
        spacer = sep if original.endswith(b"\n") else sep + sep
        output = original + spacer + addition + sep
        if not output.startswith(original):
            raise RuntimeError("R74_HISTORICAL_DOCUMENT_CHANGED")
    if output.decode("utf-8-sig").count(FINAL_MARKER) != 1:
        raise RuntimeError("R74_FINAL_MARKER_DUPLICATED")
    return output


def write_full_documents(root: Path, package: Path, context: dict[str, str]) -> dict[str, object]:
    """Output five complete files and an archive; only then replace originals."""
    output = package / "output"
    after_dir = output / "full_files"
    before_dir = output / "original_files"
    replacements: dict[str, bytes] = {}
    originals: dict[str, bytes] = {}
    for name, template_name in TEMPLATES.items():
        before = (root / name).read_bytes()
        if sha256(before).hexdigest() != DOC_SHA256[name]:
            raise RuntimeError("R74_DOCUMENT_CHANGED_DURING_GATE: " + name)
        template = (package / "updates" / template_name).read_text(encoding="utf-8")
        originals[name] = before
        replacements[name] = render_final_document(name, before, template, context)
    for name in DOC_SHA256:
        for folder, payload in ((before_dir, originals[name]), (after_dir, replacements[name])):
            target = folder / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            if target.read_bytes() != payload:
                raise RuntimeError("R74_FULL_DOCUMENT_WRITE_INVALID: " + name)
    archive = output / "phase174_r74_final_complete_documents.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in DOC_SHA256:
            zf.write(after_dir / name, arcname=name)
    with zipfile.ZipFile(archive) as zf:
        if set(zf.namelist()) != set(DOC_SHA256):
            raise RuntimeError("R74_ARCHIVE_WRONG_DOCUMENTS")
        for name in DOC_SHA256:
            if zf.read(name) != replacements[name]:
                raise RuntimeError("R74_ARCHIVE_CORRUPT: " + name)
    applied: list[str] = []
    try:
        for name in DOC_SHA256:
            if (root / name).read_bytes() != originals[name]:
                raise RuntimeError("R74_CONCURRENT_DOCUMENT_CHANGE: " + name)
            temporary = (root / name).with_name(Path(name).name + ".r74-tmp")
            temporary.write_bytes(replacements[name])
            os.replace(temporary, root / name)
            applied.append(name)
        for name in DOC_SHA256:
            if (root / name).read_bytes() != replacements[name]:
                raise RuntimeError("R74_APPLIED_CONTENT_MISMATCH: " + name)
    except Exception:
        for name in reversed(applied):
            backup = (root / name).with_name(Path(name).name + ".r74-rollback")
            backup.write_bytes(originals[name])
            os.replace(backup, root / name)
        raise
    return {"archive": str(archive), "documents": [
        {"path": name, "original_sha256": DOC_SHA256[name],
         "final_sha256": sha256(replacements[name]).hexdigest(),
         "final_bytes": len(replacements[name])} for name in DOC_SHA256
    ]}


def report_paths() -> dict[str, Path]:
    base = evidence_dir() / PACKAGE
    return {key: base / name for key, name in {
        "report": "report.json", "attempt": "attempt.json",
        "stdout": "active_suite_stdout.txt", "stderr": "active_suite_stderr.txt",
    }.items()}


def validate_closed_report(root: Path, report: object) -> bool:
    """Recognize an existing successful closeout; never rerun its full suite."""
    if not isinstance(report, dict) or report.get("phase") != "174-R74":
        return False
    if (report.get("gate") != "PASS_R74_PHASE174_FINAL_CLOSEOUT"
            or report.get("full_pytest_exit") != 0
            or type(report.get("full_pytest_passed")) is not int
            or report.get("phase174_formally_closed") is not True):
        return False
    docs = report.get("documents")
    if not isinstance(docs, list) or len(docs) != 5:
        return False
    for item in docs:
        if not isinstance(item, dict) or item.get("path") not in DOC_SHA256:
            return False
        path = root / item["path"]
        if (not path.is_file()
                or sha256(path.read_bytes()).hexdigest() != item.get("final_sha256")):
            return False
    return True


def execute_final(root: Path, package: Path, snapshot: dict[str, object]) -> int:
    paths = report_paths()
    for key in paths:
        if paths[key].exists():
            raise RuntimeError("R74_EXISTING_ATTEMPT_OR_REPORT_REQUIRES_REVIEW: " + key)
    paths["attempt"].parent.mkdir(parents=True, exist_ok=True)
    record = {"phase": "174-R74", "status": "STARTED", "head": snapshot["head"],
              "started_utc": datetime.now(timezone.utc).isoformat(),
              "command": "python " + " ".join(ACTIVE_SUITE)}
    # 'x' guards against two simultaneous full-suite invocations.
    with paths["attempt"].open("x", encoding="utf-8") as handle:
        json.dump(record, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print("PHASE174_R74_FULL_PYTEST=STARTED_ONE_PHASE_END_RUN", flush=True)
    cmd = [sys.executable, *ACTIVE_SUITE]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with paths["stdout"].open("w", encoding="utf-8") as standard_out:
        with paths["stderr"].open("w", encoding="utf-8") as standard_err:
            process = subprocess.run(cmd, cwd=root, stdout=standard_out,
                                     stderr=standard_err, env=env, check=False)
    stdout = paths["stdout"].read_text(encoding="utf-8", errors="replace")
    stderr = paths["stderr"].read_text(encoding="utf-8", errors="replace")
    print("PHASE174_R74_FULL_PYTEST_EXIT=" + str(process.returncode))
    print("PHASE174_R74_PYTEST_OUTPUT_TAIL_BEGIN")
    for line in stdout.splitlines()[-25:]:
        print(line)
    for line in stderr.splitlines()[-15:]:
        print("STDERR: " + line)
    print("PHASE174_R74_PYTEST_OUTPUT_TAIL_END")
    report: dict[str, object] = {
        "phase": "174-R74", "preflight": snapshot,
        "full_pytest_command": "python " + " ".join(ACTIVE_SUITE),
        "full_pytest_exit": process.returncode,
        "full_pytest_stdout": str(paths["stdout"]),
        "full_pytest_stderr": str(paths["stderr"]),
        "full_pytest_stdout_sha256": sha256(paths["stdout"].read_bytes()).hexdigest(),
        "full_pytest_stderr_sha256": sha256(paths["stderr"].read_bytes()).hexdigest(),
        "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": [],
        "completed_public_samples_in_r71": 8,
        "incomplete_named_goals_still_in_r72": ["pi_12^4", "pi_35^4"],
        "full_sentence_semantics_independently_certified": False,
        "phase174_formally_closed": False,
    }
    try:
        count, summary = parse_pytest_summary(stdout + "\n" + stderr, process.returncode)
        report["full_pytest_passed"] = count
        report["full_pytest_summary"] = summary
        refreshed = preflight(root)
        if refreshed != snapshot:
            raise RuntimeError("R74_SOURCE_CHANGED_DURING_PYTEST")
        context = {
            "passed": str(count), "summary": summary, "head": str(snapshot["head"]),
            "stdout_sha256": str(report["full_pytest_stdout_sha256"]),
        }
        artifacts = write_full_documents(root, package, context)
        report.update(artifacts)
        report["phase174_formally_closed"] = True
        report["gate"] = "PASS_R74_PHASE174_FINAL_CLOSEOUT"
        report["completed_utc"] = datetime.now(timezone.utc).isoformat()
        paths["report"].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
        print("PHASE174_R74_FINAL_DOCUMENTS_WRITTEN=5")
        print("PHASE174_R74_FINAL_ARCHIVE=" + str(artifacts["archive"]))
        print("PHASE174_R74_FULL_PYTEST_PASSED=" + str(count))
        print("PHASE174_R74_PHASE_FORMALLY_CLOSED=True")
        print("PHASE174_R74_REPORT=" + str(paths["report"]))
        print("PHASE174_R74_GATE=PASS_R74_PHASE174_FINAL_CLOSEOUT")
        print("(END)")
        return 0
    except Exception as error:
        report["gate"] = "FAIL_R74_REVIEW_REQUIRED"
        report["failure"] = str(error)
        report["full_pytest_passed"] = report.get("full_pytest_passed")
        report["phase174_formally_closed"] = False
        paths["report"].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
        print("PHASE174_R74_PHASE_FORMALLY_CLOSED=False")
        print("PHASE174_R74_REPORT=" + str(paths["report"]))
        print("PHASE174_R74_GATE=FAIL_R74_REVIEW_REQUIRED")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    root = package.parent
    paths = report_paths()
    if paths["report"].is_file():
        prior = json.loads(paths["report"].read_text(encoding="utf-8-sig"))
        if validate_closed_report(root, prior):
            print("PHASE174_R74_GATE=PASS_R74_ALREADY_CLOSED_NO_RERUN")
            print("(END)")
            return 0
        raise RuntimeError("R74_PRIOR_ATTEMPT_EXISTS_REVIEW_LOGS_BEFORE_RETRY")
    snapshot = preflight(root)
    print("PHASE174_R74_SOURCE_GUARD=PASS")
    print("PHASE174_R74_SOURCE_PINS=" + str(snapshot["source_pins"]))
    print("PHASE174_R74_LOCAL_HEAD=" + str(snapshot["head"]))
    print("PHASE174_R74_ORIGIN_DEVELOP=" + str(snapshot["origin_develop"]))
    print("PHASE174_R74_R73_FIVE_DOCUMENTS=PASS")
    print("PHASE174_R74_R72_INCOMPLETE_GOALS=2")
    print("PHASE174_R74_FULL_PYTEST_EXECUTED=False" if args.dry_run else
          "PHASE174_R74_FULL_PYTEST_EXECUTED=PENDING")
    if args.dry_run:
        print("PHASE174_R74_GATE=PASS_R74_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    return execute_final(root, package, snapshot)


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_audit.py（全文）

```python
"""Focused contracts for R74's single-run, fail-closed Phase 174 final gate."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import zipfile

import pytest

from phase174_r3_r7_r74_final_closeout.audit import (
    ACTIVE_SUITE,
    DOC_SHA256,
    FINAL_MARKER,
    MERGED_R73_HEAD,
    PINS,
    PREPARATION_MARKER,
    R72_HEAD,
    R73_HEAD,
    TEMPLATES,
    choose_eol,
    git_blob_sha,
    parse_pytest_summary,
    render_final_document,
    validate_closed_report,
    validate_r72_report,
    validate_r73_report,
    write_full_documents,
)


def sample_r73_report() -> dict[str, object]:
    return {
        "phase": "174-R73", "head_at_document_write": R73_HEAD,
        "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": [], "whole_test_suite_executed": False,
        "phase174_closed": False,
        "documents": [
            {"path": name, "full_file_sha256": digest, "full_file_bytes": 100}
            for name, digest in DOC_SHA256.items()
        ],
    }


def sample_r72_report() -> dict[str, object]:
    return {
        "phase": "174-R72", "local_head": R72_HEAD,
        "r71_complete_case_count": 8,
        "r71_focused_pytest_passed": 81,
        "whole_test_suite_executed": False,
        "phase174_closed": False,
        "incomplete_public_cases": [
            {"group": "pi_12^4", "status": "SEARCH_FAILED",
             "web_key": "generic-partial-proof"},
            {"group": "pi_35^4", "status": "SEARCH_FAILED",
             "web_key": "generic-partial-proof"},
        ],
    }


def sample_doc(eol: bytes = b"\n") -> bytes:
    original = ("# EHP Proof Tracer\n\n"
                "<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->\n\n"
                "<!-- " + PREPARATION_MARKER + " -->\n\n"
                "## Phase 174 R73 preparatory history\n\n"
                "Phase 174 is not formally closed.\n")
    return original.encode("utf-8").replace(b"\n", eol)


def sample_context() -> dict[str, str]:
    return {
        "passed": "3546", "summary": "3546 passed in 92.25s (0:01:32)",
        "head": MERGED_R73_HEAD, "stdout_sha256": "a" * 64,
    }


def get_template(name: str) -> str:
    package = Path(__file__).resolve().parents[1]
    return (package / "updates" / TEMPLATES[name]).read_text(encoding="utf-8")


def test_expected_reviewed_source_pins_count() -> None:
    assert len(PINS) == 8
    assert set(TEMPLATES) == set(DOC_SHA256)
    assert len(DOC_SHA256) == 5
    assert ACTIVE_SUITE[-1] == "tests"
    assert "--import-mode=importlib" not in ACTIVE_SUITE


def test_known_git_blob_sha() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_r73_reviewed_document_report_accepted() -> None:
    validate_r73_report(sample_r73_report())


def test_r73_report_does_not_claim_premature_full_suite() -> None:
    report = sample_r73_report()
    report["whole_test_suite_executed"] = True
    with pytest.raises(RuntimeError, match="R74_R73_REPORT_SCOPE_CHANGED"):
        validate_r73_report(report)


def test_r73_bad_document_hash_rejected() -> None:
    report = sample_r73_report()
    report["documents"][0]["full_file_sha256"] = "bad"
    with pytest.raises(RuntimeError, match="R74_R73_REPORT_HASH_CHANGED"):
        validate_r73_report(report)


def test_r72_incomplete_boundary_accepted() -> None:
    validate_r72_report(sample_r72_report())


def test_r72_promoted_named_goal_rejected() -> None:
    report = sample_r72_report()
    report["incomplete_public_cases"][0]["status"] = "COMPLETE"
    with pytest.raises(RuntimeError, match="R74_INCOMPLETE_BOUNDARY_CHANGED"):
        validate_r72_report(report)


@pytest.mark.parametrize("summary", [
    "3546 passed in 92.25s (0:01:32)",
    "3546 passed, 2 skipped in 92.25s (0:01:32)",
])
def test_parse_real_success_summary(summary: str) -> None:
    assert parse_pytest_summary("[100%]\n" + summary, 0) == (3546, summary)


@pytest.mark.parametrize("output,code", [
    ("3546 passed in 90.11s", 1),
    ("... [100%]", 0),
    ("4 passed in 1s\n5 passed in 2s", 0),
    ("0 passed in 0.1s", 0),
])
def test_non_success_or_ambiguous_pytest_fails(output: str, code: int) -> None:
    with pytest.raises(RuntimeError):
        parse_pytest_summary(output, code)


@pytest.mark.parametrize("name", list(DOC_SHA256))
def test_all_five_document_templates_are_complete_and_preserve_history(name: str) -> None:
    raw = sample_doc()
    result = render_final_document(name, raw, get_template(name), sample_context())
    text = result.decode("utf-8")
    assert FINAL_MARKER in text
    assert text.count(FINAL_MARKER) == 1
    assert text.count(PREPARATION_MARKER) == 1
    assert "3546 passed" in text or "3546 PASS" in text
    assert MERGED_R73_HEAD in text
    assert "{{" not in text
    if name == "README.md":
        assert text.index(FINAL_MARKER) < text.index(PREPARATION_MARKER)
        anchor = "<!-- " + PREPARATION_MARKER + " -->"
        assert text[text.index(anchor):] == raw.decode("utf-8")[raw.decode("utf-8").index(anchor):]
    else:
        assert result.startswith(raw)
    assert len(result) > len(raw)


def test_crlf_document_history_and_newline_are_preserved() -> None:
    original = sample_doc(eol=b"\r\n")
    name = "docs/proof_records.md"
    result = render_final_document(name, original, get_template(name), sample_context())
    assert choose_eol(original) == b"\r\n"
    assert result.startswith(original)
    assert b"\r\n" in result
    assert b"\r\r\n" not in result


def test_missing_preparation_marker_rejected() -> None:
    original = sample_doc().replace(PREPARATION_MARKER.encode(), b"missing")
    with pytest.raises(RuntimeError, match="R74_INVALID_BASE_DOCUMENT"):
        render_final_document("README.md", original, get_template("README.md"), sample_context())


def test_existing_final_marker_rejected() -> None:
    original = sample_doc() + FINAL_MARKER.encode()
    with pytest.raises(RuntimeError, match="R74_INVALID_BASE_DOCUMENT"):
        render_final_document("docs/design.md", original, get_template("docs/design.md"),
                              sample_context())


def test_unresolved_placeholder_rejected() -> None:
    with pytest.raises(RuntimeError, match="R74_TEMPLATE_UNRESOLVED_PLACEHOLDERS"):
        render_final_document("README.md", sample_doc(),
                              get_template("README.md") + "\n{{unknown}}\n",
                              sample_context())


def test_final_archive_contains_five_complete_documents(tmp_path: Path,
                                                        monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r74_final_closeout.audit as module
    monkeypatch.setattr(module, "DOC_SHA256", {
        name: sha256(sample_doc()).hexdigest() for name in DOC_SHA256
    })
    for name in DOC_SHA256:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(sample_doc())
    source_package = Path(__file__).resolve().parents[1]
    package = tmp_path / "phase174_r3_r7_r74_final_closeout"
    for basename in TEMPLATES.values():
        template_path = package / "updates" / basename
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_bytes((source_package / "updates" / basename).read_bytes())
    artifacts = write_full_documents(tmp_path, package, sample_context())
    archive = Path(artifacts["archive"])
    assert archive.is_file()
    with zipfile.ZipFile(archive) as zf:
        assert set(zf.namelist()) == set(DOC_SHA256)
        for name in DOC_SHA256:
            assert zf.read(name) == (tmp_path / name).read_bytes()
    assert len(artifacts["documents"]) == 5


def test_closed_report_does_not_allow_modified_document(tmp_path: Path) -> None:
    for name in DOC_SHA256:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("final", encoding="utf-8")
    report = {
        "phase": "174-R74", "gate": "PASS_R74_PHASE174_FINAL_CLOSEOUT",
        "full_pytest_exit": 0, "full_pytest_passed": 3546,
        "phase174_formally_closed": True,
        "documents": [{"path": name,
                       "final_sha256": sha256(b"final").hexdigest()}
                      for name in DOC_SHA256],
    }
    assert validate_closed_report(tmp_path, report)
    (tmp_path / "README.md").write_text("changed", encoding="utf-8")
    assert not validate_closed_report(tmp_path, report)
```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$package = 'phase174_r3_r7_r74_final_closeout'

python -B -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R74 reviewed-source or documents preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R74_GATE=PASS_R74_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r73_closeout_documents/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R74 focused test contracts failed before full suite' }

python -B -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R74 full active-suite or document gate failed' }

Write-Output 'PHASE174_R74_GATE=PASS_R74_FOCUSED_FULL_SUITE_AND_FIVE_DOCUMENTS'
Write-Output '(END)'
```

## README.md（全文）

```markdown
# Phase 174 R74 — Final Closeout Gate

This package runs the end-of-phase active pytest suite once, only after source, Git, prior evidence, documentation, and focused-test guards pass. A failure or interruption is recorded and never retried automatically.

The reviewed base is either the R73 pre-merge HEAD with exactly five unstaged R73 document edits, or the merged R73 HEAD with no tracked edits. This package does not fetch or alter Git history, the index, production proof code, or mathematical rules. It does not install any document before the full pytest suite passes.

On success it writes five complete Markdown files to `output/full_files/`, retains full originals in `output/original_files/`, creates a five-document ZIP, updates the canonical five documents, and records the suite result outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r74_final_closeout/`. It does not assume that a focused pytest result implies full-suite success.

Run `run.ps1 -DryRun` and then `run.ps1` using Windows PowerShell from the repository root. A prior attempt/report blocks reruns unless a verified successful report already describes the current final documents; then the script reports that it is already closed without launching tests again.
```

## updates/README.md（全文）

```markdown
<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->

## Current status — Phase 174 formally closed (2026-11-11)

Phase 174 is formally closed **only for its reviewed source-first typed proof-search, shared narrative, and active test-suite scope**. The final R74 gate ran the active `tests/` pytest suite once: **{{passed}} passed**, summary `{{summary}}`. The recorded local `develop` HEAD at the gate was `{{head}}`; the preserved stdout SHA-256 is `{{stdout_sha256}}`. A gate report, stdout/stderr, and five complete final Markdown files are preserved by the R74 package.

The public typed proof for $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ completes using general inference rules with 7 references. The public typed proof for $\pi_{12}^{7}=0$ completes using one previously adopted database group result with 3 references, without replaying its earlier proof. Both return `generic-complete-proof`.

R70/R70R1 improved the generic, verified ProofStep-backed explanation without new mathematical inference rules or GIVEN assertions. R71 checked eight complete public proof narratives (81 focused tests passed); R72 preserved the `SEARCH_FAILED` named-generator status for $\pi_{12}^{4}$ and $\pi_{35}^{4}$ (38 focused tests passed); R73 prepared and installed the five documentation updates (33 focused tests passed). These earlier scoped checks are not reported as new full-suite executions. The first successful proof search remains the stopping condition; proof uniqueness is not checked.

This closeout does **not** certify all source literature, every proof sentence, arbitrary homotopy groups, the unfinished named-generator goals, or a browser-pixel/MathJax rendering audit. The R73 closeout-preparation section below is historical and does not override this final status.

---
```

## updates/design.md（全文）

```markdown
<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->

## Phase 174 正式終了 — 現行設計の検証境界（2026-11-11）

Phase 174 の終了監査 R74 において、現行アクティブ `tests/` に対する全体 pytest を Phase 末尾に1回実行し、**{{passed}} PASS**（`{{summary}}`）を確認した。検証時の `develop` HEAD は `{{head}}`。標準出力の SHA-256 は `{{stdout_sha256}}`。これは保存された R74 の実行証拠に基づく記録であり、未実施の全テストや出典の全面的な真偽を保証しない。

現行の公開証明経路は、Source-first（出典優先）の型付き Backward Search（後向き探索）→ Verified Proof Tree（検証済み証明木）→ 単一 `ProofNarrativeModel`（証明文章モデル）→ 共通 Renderer（表示器）→ Web である。First Successful Proof Search（最初の成功で終了）を維持し、唯一性検査は行わない。個々の $(n,k)$ や生成元に専用の数学的証明・Narrative（叙述）を加えない。

R70/R70R1 の一般的な表示変換は、合成・結合法則・零像について実際の型付き ProofStep（証明段階）の根祖先と引用を確認した場合にのみ文章を集約する。不確実な証拠では変換をしない。零群に至る $E=0$ と $H$ の単射性についての文章は、既存の4前提一般規則の説明であり、新たな独立 ProofStep ではない。

R71 は完成8群の公開状態と Reference（出典）を回帰検査した。R72 は $\pi_{12}^{4}$、$\pi_{35}^{4}$ の記名生成元 Goal（証明目標）が未完成のままであることを確認した。表示で未完成を完成扱いに変えない。今回の終了は、これらの特定の証明・実装・アクティブテストに限る。出典文献の全命題、任意の群、全文章の独立数学検証、ブラウザ画素品質は対象外とする。
```

## updates/development_log.md（全文）

```markdown
<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->

## 2026-11-11 — Phase 174 R74 最終 Gate：正式終了の実行記録

R70R1 の共通 Narrative（証明叙述）修正後、R71 の Source Guard 9件・限定 pytest 81 PASS・完成8群の公開回帰、R72 の Source Guard 10件・限定 pytest 38 PASS・未完成2群の `SEARCH_FAILED` 維持、R73 の Source Guard 6件・限定 pytest 33 PASS・主要5文書の全文出力を経た。R71〜R73 は数学的規則・GIVEN・本番コードの新規追加を行っていない。

R74 は Phase 末尾の全体 pytest を1回だけ実行した。結果は **{{passed}} PASS**、実際の要約は `{{summary}}`、検査時 HEAD は `{{head}}`、stdout SHA-256 は `{{stdout_sha256}}`。失敗した場合に自動で全体 pytest を再実行しない設計にし、実行前の attempt、stdout/stderr、report と Git／文書検査を保存する。全体テストの通過を最終 Closeout（正式終了）の必要条件とした。

正式終了後の公開完成例は $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$（Reference 7件）と $\pi_{12}^{7}=0$（Reference 3件）。前者は一般推論規則の連鎖に基づき、後者は先行のデータベース群結果を再証明せず利用する。検証済み Proof Tree の叙述を共通 Renderer で生成し、群専用の証明や新規 GIVEN の結論登録は追加していない。

**Phase 174 正式終了。** 未完成の $\pi_{12}^{4}$、$\pi_{35}^{4}$ を完成と扱わず、数学的に未検証の一般命題を認証したとは記載しない。過去の Phase 173・R73 の未完成時点の記録は履歴として残す。次 Phase の実装とテストは別の計画として監査・実施する。
```

## updates/roadmap.md（全文）

```markdown
<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->

## Phase 174 正式終了と次 Phase の境界（2026-11-11）

R74 で Phase 末尾のアクティブ `tests/` 全体 pytest **{{passed}} PASS**（`{{summary}}`）を確認し、HEAD `{{head}}` に結び付けた証拠（stdout SHA-256: `{{stdout_sha256}}`）を保存した。R71 完成8群の表示回帰、R72 未完成2群の境界、R73 主要5文書の全文整備と合わせて、**Phase 174 は正式終了**とする。

**次 Phase の作業候補（未実装）**：未完成の $\pi_{12}^{4}$ と $\pi_{35}^{4}$ の記名生成元 Goal や、出典付き数学的推論の不足を個別に監査する。さらに広い範囲の登録群については、群構造の既知性と証明の完成を区別して Scope（範囲）を先に確定する。今回の Closeout に未来 Phase の規則を先取りしない。

将来の Phase でも Source-first、First Successful Proof Search、唯一性検査なし、共通 Verified Proof Tree → `ProofNarrativeModel` → Renderer → Web を維持する。個別群専用 Narrative・結論直接 GIVEN の追加を避け、数学的に妥当な一般規則だけを検討する。全体 pytest はそれぞれの Phase 末尾に実施する。
```

## updates/proof_records.md（全文）

```markdown
<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->

## 2026-11-11 — Phase 174 正式終了時の証明・回帰記録

R74 の Phase 末尾アクティブ `tests/` 全体 pytest は **{{passed}} PASS**（`{{summary}}`）。監査対象 HEAD は `{{head}}`、保存 stdout SHA-256 は `{{stdout_sha256}}`。R71 の Reference 件数と 8群完成証明、R72 の未完成2群（`SEARCH_FAILED`）を終了条件の根拠として引き継ぎ、R74 の1回の全体テストを通過した。

### 一般規則による完成証明（出典7件）

$$
\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\},\qquad
E(\nu_5\eta_8^2)=\nu_6\eta_9^2=0.
$$

したがって EHP 完全性より $H:\pi_{11}^{6}\to\pi_{11}^{11}$ は単射。さらに検証済みの出典付き一般推論により、

$$
\ker(\Delta:\pi_{11}^{11}\to\pi_9^5)=\mathbb Z\{2\iota_{11}\},\qquad
H(\Delta(\iota_{13}))=\pm 2\iota_{11}.
$$

ゆえに $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$。公開結果は `generic-complete-proof` である。

### 先行群の再証明を伴わない零群の完成（出典3件）

先行データベース結果 $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ を採用し、$\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$ は全射。EHP 完全性より

$$
\operatorname{Im}\Delta=\ker E=\pi_{11}^{6},\qquad
\ker H=\operatorname{Im}E=0.
$$

$H:\pi_{12}^{7}\to\pi_{12}^{13}$ は単射で、$\pi_{12}^{13}=0$ なので $\pi_{12}^{7}=0$ が従う。公開結果は `generic-complete-proof`。表示中の $E=0$、$H$ 単射の説明は既存の一般零群規則から導かれる Narrative であり、新規独立 ProofStep の追加ではない。

**認定範囲の制限：** 文献一般命題の全数学的証明や未完成群の生成元の決定、証明文章のすべての独立確認を完了したとは扱わない。R73 の終了前記録と旧 Phase 173 の未完成例は履歴として保持し、R74 によって後から時点を改変しない。
```
