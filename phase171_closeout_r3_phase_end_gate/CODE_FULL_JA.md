# Phase 171 Closeout R3 — 新規コード・新規テスト全文

対象は新規 `closeout.py` の関数 `git`, `git_blob_bytes`, `tracked_paths`, `reviewed_commit_changes`, `load_r2_writer`, `preflight`, `pytest_pass_count`, `run_full_suite`, `closure_sections`, `closure_documents`, `atomic_write`, `save_report`, `export_docs`, `run`, `main` である。既存の本番クラス・関数の変更はない。以下に、新規ファイルの **import を含む全文** を示す。省略はない。

## closeout.py

```python
"""Phase 171 final closeout: a single active-suite pytest and five complete documents.

Only after the active test suite passes and unchanged proof/source code is checked,
append the closing record to the five reviewed R2 documents.  Never rewrite
historical document bytes, change production modules, or run a full suite twice
when resuming an already verified run.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEWED_HEAD = "3e74849bf90bc115c16503ddd46d49996baa0856"
BRANCH = "develop"
R2_DIRECTORY = "phase171_closeout_r2_documentation_full_output"
R2_WRITER = f"{R2_DIRECTORY}/update_docs.py"
R2_WRITER_SHA256 = "8b39e61e57d171b2bf451137fd28730fca283364f726740a0cb543b808fd05d1"
R2_MARKER = "PHASE171_CLOSEOUT_R2_REVIEWED_20261031"
FINAL_MARKER = "PHASE171_FINAL_CLOSEOUT_20261031"
TEST_R1R1 = "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py"
SOURCE_BLOBS = {
    TEST_R1R1: "f98557eef6f2dd720c4b74ff28b8469e668df2f4",
    "phase168_r3_5_model_renderer.py": "94996b403f1c01f81319824565db422463714f02",
    "phase171_r20r12_verified_cyclic_narrative/projection.py": "73babd53daf6ec088e12b723a905ba40523f8120",
    "phase171_r20r13_eta_sentence_layout/projection.py": "4c1ef57ed0a20d551ae24c80d4b7ddbbb7df9c31",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py": "881d5a5cdc77220be42615236ed99ff3ec6ee164",
}
BASE_DOC_BLOBS = {
    "README.md": "cc65eea3ae9e4bf1e7d67d74550eda4f4f8b4024",
    "docs/design.md": "6f4a65431cf0e4ba2c517b521654e732568f45db",
    "docs/development_log.md": "64484312f89636c00e6d7dac670d719e81016eca",
    "docs/roadmap.md": "f6b48da7a853200c8b9323baff77731002d43026",
    "docs/proof_records.md": "0f4289bccca3558632f621596e04199e44360576",
}
ALLOWED_COMMITTED_PREFIXES = (
    "phase171_closeout_r2_documentation_full_output/",
    "phase171_closeout_r2r1_committed_head_guard/",
    "phase171_closeout_r2r2_runner_splat_fix/",
    "phase171_closeout_r2r3_mixed_line_ending_fix/",
    "phase171_closeout_r2r4_restored_source_guard/",
    "phase171_closeout_r3_phase_end_gate/",
)
ACTIVE_ARGS = ("-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "tests")


def git(*args: str, root: Path = ROOT) -> str:
    run = subprocess.run(("git", *args), cwd=root, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if run.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + run.stderr.decode("utf-8", "replace").strip())
    return run.stdout.decode("utf-8", "replace").strip()


def git_blob_bytes(revision: str, relative: str, *, root: Path = ROOT) -> bytes:
    run = subprocess.run(("git", "show", revision + ":" + relative), cwd=root,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode:
        raise RuntimeError("unable to read committed document: " + relative)
    return run.stdout


def tracked_paths(root: Path = ROOT) -> set[str]:
    data = git("-c", "core.quotePath=false", "diff", "--name-only", "HEAD", "--", root=root)
    return set(filter(None, data.splitlines()))


def reviewed_commit_changes(base: str, head: str, root: Path = ROOT) -> set[str]:
    if base == head:
        return set()
    git("merge-base", "--is-ancestor", base, head, root=root)
    changed = set(filter(None, git("-c", "core.quotePath=false", "diff", "--name-only", base, head, "--", root=root).splitlines()))
    allowed = set(BASE_DOC_BLOBS)
    disallowed = {p for p in changed if p not in allowed and not p.startswith(ALLOWED_COMMITTED_PREFIXES)}
    if disallowed:
        raise RuntimeError("unexpected committed files: " + ", ".join(sorted(disallowed)))
    return changed


def load_r2_writer(root: Path = ROOT):
    file = root / R2_WRITER
    if not file.is_file() or sha256(file.read_bytes()).hexdigest() != R2_WRITER_SHA256:
        raise RuntimeError("reviewed R2 document writer missing or changed")
    spec = importlib.util.spec_from_file_location("phase171_closeout_reviewed_r2_writer", file)
    if spec is None or spec.loader is None:
        raise RuntimeError("R2 writer could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preflight(root: Path = ROOT) -> dict:
    """Audit exactly the reviewed proof code and fully reviewed R2 documents."""
    branch = git("branch", "--show-current", root=root)
    head = git("rev-parse", "HEAD", root=root)
    print("PHASE171_CLOSEOUT_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_CLOSEOUT_R3_HEAD=" + head, flush=True)
    if branch != BRANCH:
        raise RuntimeError("develop branch required")
    changes = reviewed_commit_changes(REVIEWED_HEAD, head, root)
    if git("rev-parse", "origin/develop", root=root) != head:
        raise RuntimeError("origin/develop does not match local HEAD")
    if git("diff", "--cached", "--name-only", "--", root=root):
        raise RuntimeError("staged changes must be empty")
    tracked = tracked_paths(root)
    if not tracked.issubset(BASE_DOC_BLOBS):
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(tracked - BASE_DOC_BLOBS.keys())))
    for path, blob in SOURCE_BLOBS.items():
        if git("rev-parse", "HEAD:" + path, root=root) != blob:
            raise RuntimeError("reviewed source Git blob changed: " + path)
        if not (root / path).is_file():
            raise RuntimeError("missing reviewed source: " + path)
        if git("hash-object", path, root=root) != blob:
            raise RuntimeError("reviewed source worktree differs: " + path)
    r2 = load_r2_writer(root)
    prior_docs: dict[str, bytes] = {}
    for path, blob in BASE_DOC_BLOBS.items():
        if git("rev-parse", REVIEWED_HEAD + ":" + path, root=root) != blob:
            raise RuntimeError("reviewed Phase 170 doc baseline mismatch: " + path)
        original = git_blob_bytes(REVIEWED_HEAD, path, root=root)
        expected = r2.updated_document(path, original)
        actual = (root / path).read_bytes()
        if r2.lf_text(actual) != r2.lf_text(expected):
            raise RuntimeError("unexpected content in Phase 171 R2 document: " + path)
        if FINAL_MARKER in r2.lf_text(actual):
            raise RuntimeError("Phase 171 has already been closed: " + path)
        if path == "README.md" and r2.lf_text(actual).count(R2_MARKER) != 1:
            raise RuntimeError("Phase 171 R2 README heading is missing")
        prior_docs[path] = actual
    if not (root / "tests").is_dir():
        raise RuntimeError("active tests/ directory missing")
    print("PHASE171_CLOSEOUT_R3_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R3_DOCUMENTS=5", flush=True)
    print("PHASE171_CLOSEOUT_R3_TRACKED_BEFORE=" + ",".join(sorted(tracked)), flush=True)
    return {
        "branch": branch, "head": head,
        "reviewed_head": REVIEWED_HEAD,
        "committed_delta": sorted(changes),
        "tracked_before": sorted(tracked),
        "document_sha256": {p: sha256(b).hexdigest() for p, b in prior_docs.items()},
        "reviewed_source_blobs": dict(SOURCE_BLOBS),
        "document_bytes": prior_docs,
    }


def pytest_pass_count(output: str, exit_code: int) -> tuple[int, str]:
    """Reject a zero-exit pytest invocation with no recognizable pass summary."""
    if exit_code != 0:
        raise RuntimeError("active pytest returned nonzero exit status")
    matches = re.findall(r"(?m)^([^\n]*\b([0-9]+) passed\b[^\n]*)$", output)
    if not matches:
        raise RuntimeError("active pytest has no pass-count summary")
    last, number = matches[-1]
    if int(number) <= 0 or re.search(r"\b(?:failed|error|errors)\b", last, re.IGNORECASE):
        raise RuntimeError("active pytest summary is not a full pass")
    return int(number), last.strip()


def run_full_suite(root: Path, log_path: Path) -> tuple[int, str, int]:
    env = os.environ.copy()
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    command = [sys.executable, *ACTIVE_ARGS]
    print("PHASE171_CLOSEOUT_R3_FULL_PYTEST_START", flush=True)
    print("PHASE171_CLOSEOUT_R3_COMMAND=python " + " ".join(ACTIVE_ARGS), flush=True)
    proc = subprocess.Popen(command, cwd=root, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                            errors="replace", bufsize=1)
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            log.flush()
            print(line, end="", flush=True)
    code = proc.wait()
    print("PHASE171_CLOSEOUT_R3_FULL_PYTEST_EXIT=" + str(code), flush=True)
    output = log_path.read_text(encoding="utf-8")
    if code:
        summary = "FULL_SUITE_FAILED_EXIT_" + str(code)
        print("PHASE171_CLOSEOUT_R3_FULL_PYTEST_SUMMARY=" + summary, flush=True)
        return 0, summary, code
    count, summary = pytest_pass_count(output, code)
    print("PHASE171_CLOSEOUT_R3_FULL_PYTEST_SUMMARY=" + summary, flush=True)
    return count, summary, code


def closure_sections(count: int, summary: str, *, date: str = "2026-10-31") -> dict[str, str]:
    if count < 1 or "passed" not in summary:
        raise ValueError("closure sections require a verified pytest pass summary")
    text = f"{count:,} PASS（{summary}、終了コード0）"
    readme = f"""<!-- {FINAL_MARKER} -->

## Current status — Phase 171 closed ({date})

Phase 171 is complete for the reviewed public proof of $\\pi_6^3=\\mathbb Z/4\\{{\\nu'\\}}$. The verified search has `complete`, `open_goals=0`, eight source-linked references, and a `generic-complete-proof` Web narrative. The mathematical basis is the EHP short exact sequence and the independently certified relation $2\\nu'=E(\\eta_2^3)\\ne0$, establishing that $\\nu'$ has order four.

The single phase-end active `tests/` suite reported **{count:,} passed** (pytest summary: `{summary}`, exit code 0). Phase 171 R1R1 and R2R4 focused gates had already passed, and this closeout kept production code and historical proof sources unchanged. The archived full five-document outputs and gate JSON preserve the reviewed result. Previous R2 text stating that the phase-end test was pending is a historical pre-closure record.

Phase 172 may separately review display duplication and `DB prior` wording; these are not mathematical proof prerequisites. The result does not certify arbitrary $n\\ge3$ groups or unchecked literature.

"""
    design = f"""

<!-- {FINAL_MARKER} -->

## Phase 171 — 最終終了 Gate（{date}）

Phase 171 終了時に現行アクティブ `tests/` の全体 pytest を1回実行し、**{text}** を確認した。R2 文書5ファイルは元の内容に対して審査済みの追加のみであり、この正式終了節も既存本文のバイト列を保存して追加した。数理的な Proof Tree、Backward Search、Reference、Renderer の本番実装を変更していない。

完成認定対象は登録済み $\\pi_6^3=\\mathbb Z/4\\{{\\nu'\\}}$ の Proof Tree と公開 Web 経路に限る。Phase 172 の表示改善候補を Phase 171 の完成条件に混入させない。
"""
    dev = f"""

<!-- {FINAL_MARKER} -->

## {date} — Phase 171 正式終了 Gate

R1 の限定 pytest（87 PASS、1 FAIL）で歴史的な28ステップ固定値を検出し、R1R1 では数学的な探索結果を変更せず証明の保全を検査する方式に修正した（88 PASS、追加安全検査5 PASS）。文書更新の R2R4 は5文書を作成し、11 PASS、24 PASS、56 PASS の限定テストを確認した。

最終 Gate は、審査済み5文書と5件のソースの Git blob、R1R1 のコミット済みテスト、予期しない追跡済み差分がないことを事前に確認した。Phase 末尾に `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を1回実行し、**{text}**。終了後も本番コードの内容が不変であることを監査し、5文書の全文・実行ログ・監査 JSON をリポジトリ外に保存した。

Phase 171 の終了を認定する。Phase 172 は重複表示や `DB prior` 文言の監査とし、未証明の `GIVEN` を追加しない。
"""
    roadmap = f"""

<!-- {FINAL_MARKER} -->

## Phase 171 正式終了／Phase 172 の境界（{date}）

Phase 171 は $\\pi_6^3=\\mathbb Z/4\\{{\\nu'\\}}$ の公開完成証明、出典8件、未解決目標0件、限定回帰を確認し、終了時の現行アクティブ `tests/` 全体 pytest **{text}** により正式に Closeout した。以前の「Gate 待ち」は R2 時点の履歴記録であり、本節を最新の状態とする。

Phase 172 は完成済み証明の表示改善を別途監査する。$E(\\eta_5)=\\eta_6$ の重複、長い Hopf 表示、全射性説明の重複、`DB prior` 表記の扱いは数学的な新前提の追加と区別する。未登録群全体の完成はこの Phase 171 の認定範囲に含めない。
"""
    proof = f"""

<!-- {FINAL_MARKER} -->

## {date} — Phase 171 完成証明の正式終了記録

登録済み $\\pi_6^3=\\mathbb Z/4\\{{\\nu'\\}}$ の根拠は、$E$ の単射性・$H$ の全射性による EHP 短完全列、$|\\pi_6^3|=4$、$2\\nu'=E(\\eta_2^3)\\ne0$、生成元 $\\nu'$ の位数4である。公開 Backward Search は `complete`、`open_goals=0`、Web `generic-complete-proof`、Reference 8件を保持する。

R1R1 の限定回帰88 PASS と文書更新 R2R4 の限定回帰56 PASS の後、Phase 終了 Gate で現行アクティブ `tests/` の pytest **{text}** を確認した。証明木・引用採用規則・本番 Renderer に追加変更はなく、既存結果の利用に際して先行証明を再実行する要件も加えていない。前節の「全体 pytest 未実施」は R2 時点の履歴であり、本節が正式終了時点の記録となる。

証明完成の認定はこの目標群と既存 Trust Boundary に限定する。他の任意の群の証明や原著の全面的な正しさは主張しない。
"""
    return {"README.md": readme, "docs/design.md": design,
            "docs/development_log.md": dev, "docs/roadmap.md": roadmap,
            "docs/proof_records.md": proof}


def closure_documents(before: dict[str, bytes], sections: dict[str, str]) -> dict[str, bytes]:
    if set(before) != set(BASE_DOC_BLOBS) or set(sections) != set(BASE_DOC_BLOBS):
        raise ValueError("all five reviewed documents must be supplied")
    output: dict[str, bytes] = {}
    for path, source in before.items():
        if FINAL_MARKER.encode("ascii") in source:
            raise ValueError("final closure marker already exists: " + path)
        if R2_MARKER.encode("ascii") not in source and path == "README.md":
            raise ValueError("R2 marker is missing from README")
        newline = b"\n"
        index = source.rfind(b"\n")
        if index >= 0:
            begin = index
            while begin > 0 and source[begin - 1] == 13:
                begin -= 1
            newline = source[begin:index + 1]
        body = sections[path].replace("\r\n", "\n").encode("utf-8").replace(b"\n", newline)
        if body.count(FINAL_MARKER.encode("ascii")) != 1:
            raise ValueError("invalid final closure marker")
        if path == "README.md":
            anchor = ("<!-- " + R2_MARKER + " -->").encode("ascii")
            if source.count(anchor) != 1:
                raise ValueError("README Phase 171 R2 insertion point missing")
            split = source.index(anchor)
            revised = source[:split] + body + source[split:]
            if not revised.endswith(source[split:]):
                raise AssertionError("historical README suffix changed")
        else:
            revised = source + body
            if not revised.startswith(source):
                raise AssertionError("historical document bytes changed")
        if revised.count(FINAL_MARKER.encode("ascii")) != 1:
            raise ValueError("final section was not inserted exactly once")
        output[path] = revised
    return output


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".phase171_closeout_", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def save_report(path: Path, report: dict) -> None:
    data = json.dumps(report, ensure_ascii=False, indent=2, default=str).encode("utf-8") + b"\n"
    atomic_write(path, data)


def export_docs(dest: Path, docs: dict[str, bytes]) -> Path:
    for path, data in docs.items():
        atomic_write(dest / "FULL_DOCUMENTS" / path, data)
    archive = dest / "PHASE171_FINAL_FIVE_FULL_DOCUMENTS.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in docs.items():
            z.writestr(path, data)
    return archive


def run(root: Path, *, dry_run: bool, resume_report: Path | None) -> int:
    report_root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    report_root.mkdir(parents=True, exist_ok=True)
    output = report_root / ("phase171_closeout_r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report_path = output / "closeout.json"
    report: dict = {"phase": "171_CLOSEOUT_R3", "dry_run": dry_run,
                    "full_pytest": False, "result": "STARTED",
                    "active_command": ["python", *ACTIVE_ARGS]}
    result_code = 2
    previous: dict | None = None
    try:
        prior = preflight(root)
        before = prior.pop("document_bytes")
        report["preflight"] = prior
        report["documents_before_sha256"] = prior["document_sha256"]
        if dry_run:
            report["result"] = "PASS_DRY_RUN"
            print("PHASE171_CLOSEOUT_R3_RESULT=PASS_DRY_RUN", flush=True)
            result_code = 0
        else:
            if resume_report is not None:
                previous = json.loads(resume_report.read_text(encoding="utf-8-sig"))
                if (previous.get("phase") != "171_CLOSEOUT_R3"
                        or previous.get("pytest_exit") != 0
                        or previous.get("full_suite_verified") is not True
                        or previous.get("preflight", {}).get("head") != prior["head"]
                        or previous.get("documents_before_sha256") != prior["document_sha256"]):
                    raise RuntimeError("resume evidence does not match reviewed repository state")
                count = previous["pytest_passed"]
                summary = previous["pytest_summary"]
                if type(count) is not int or count < 1 or "passed" not in summary:
                    raise RuntimeError("resume evidence contains no verified pytest summary")
                report["resume_report"] = str(resume_report)
                print("PHASE171_CLOSEOUT_R3_PYTEST=REUSE_VERIFIED_REPORT", flush=True)
            else:
                count, summary, exit_code = run_full_suite(root, output / "full_pytest.log")
                report["full_pytest"] = True
                report["pytest_exit"] = exit_code
                report["pytest_summary"] = summary
                report["pytest_passed"] = count
                report["full_suite_verified"] = exit_code == 0
                save_report(report_path, report)
                if exit_code:
                    raise RuntimeError("the active full pytest did not pass")
            # Verify the test run did not alter tracked code or the reviewed R2 documents.
            after_suite = preflight(root)
            after_bytes = after_suite.pop("document_bytes")
            if {p: sha256(b).hexdigest() for p, b in after_bytes.items()} != prior["document_sha256"]:
                raise RuntimeError("documents changed during the full suite")
            if after_suite["tracked_before"] != prior["tracked_before"] or after_suite["head"] != prior["head"]:
                raise RuntimeError("tracked changes or HEAD changed during the full suite")
            sections = closure_sections(count, summary)
            final_docs = closure_documents(before, sections)
            for path, data in before.items():
                atomic_write(output / "BEFORE_FULL_DOCUMENTS" / path, data)
            changed: list[str] = []
            try:
                for path, data in final_docs.items():
                    atomic_write(root / path, data)
                    changed.append(path)
                for path, data in final_docs.items():
                    if (root / path).read_bytes() != data:
                        raise RuntimeError("document unexpectedly changed after applying final status: " + path)
                final_tracked = tracked_paths(root)
                if final_tracked != set(BASE_DOC_BLOBS):
                    raise RuntimeError("unexpected Git paths after final document update")
                if git("diff", "--cached", "--name-only", "--", root=root):
                    raise RuntimeError("new staged changes after closeout")
                archive = export_docs(output, final_docs)
                report["final_doc_sha256"] = {p: sha256(b).hexdigest() for p, b in final_docs.items()}
                report["full_document_archive"] = str(archive)
                report["tracked_after"] = sorted(final_tracked)
                report["result"] = "PHASE171_CLOSED_FULL_SUITE_PASS"
                report["full_suite_verified"] = True
                report["pytest_exit"] = 0
                report["pytest_passed"] = count
                report["pytest_summary"] = summary
                result_code = 0
                print("PHASE171_CLOSEOUT_R3_FULL_DOCUMENTS=" + str(archive), flush=True)
                print("PHASE171_CLOSEOUT_R3_RESULT=" + report["result"], flush=True)
            except Exception:
                for path in reversed(changed):
                    atomic_write(root / path, before[path])
                raise
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-4000:]
        if report.get("full_suite_verified") is True:
            report["result"] = "FULL_SUITE_PASS_DOCUMENT_CLOSEOUT_FAILED"
        else:
            report["result"] = "REFUSED_OR_FAILED"
        print("PHASE171_CLOSEOUT_R3_ERROR=" + report["error"], flush=True)
        result_code = 1
    finally:
        report["report_path"] = str(report_path)
        save_report(report_path, report)
        print("PHASE171_CLOSEOUT_R3_REPORT=" + str(report_path), flush=True)
        print("PHASE171_CLOSEOUT_R3_FINAL=" + str(report["result"]), flush=True)
    return result_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume-report", type=Path)
    args = parser.parse_args()
    # ROOT is derived from the package itself; reject an arbitrary other worktree.
    if args.root.resolve() != ROOT.resolve():
        raise SystemExit("--root must be the containing repository")
    return run(ROOT, dry_run=args.dry_run,
               resume_report=args.resume_report.resolve() if args.resume_report else None)


if __name__ == "__main__":
    raise SystemExit(main())

```

## run.ps1

```powershell
param(
    [switch]$DryRun,
    [string]$ResumeReport = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonUtf8 = $env:PYTHONUTF8
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $PythonArguments = @('-B', (Join-Path $PSScriptRoot 'closeout.py'), '--root', $Root)
    if ($DryRun) {
        $PythonArguments += '--dry-run'
    }
    if ($ResumeReport -ne '') {
        $PythonArguments += @('--resume-report', $ResumeReport)
    }
    & python @PythonArguments
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "Phase 171 final closeout did not pass: exit $ExitCode"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}

```

## tests/test_closeout.py

```python
"""Isolated tests for Phase 171 final gate; full active pytest is never run here."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace
import zipfile

import pytest

from phase171_closeout_r3_phase_end_gate import closeout as c


def test_active_command_runs_exactly_the_reviewed_active_tests():
    assert c.ACTIVE_ARGS == (
        "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings",
        "-p", "no:cacheprovider", "tests",
    )


@pytest.mark.parametrize("output,code", [
    ("3546 passed in 34.94s\n", 0),
    ("================ 3546 passed in 34.94s ================\n", 0),
    ("3600 passed, 3 skipped in 51.2s\n", 0),
])
def test_pytest_pass_count_accepts_valid_summaries(output, code):
    count, summary = c.pytest_pass_count(output, code)
    assert count >= 3546
    assert "passed" in summary


@pytest.mark.parametrize("output,code", [
    ("3546 passed in 34.94s\n", 1),
    ("1 failed, 3546 passed in 34.94s\n", 0),
    ("no tests ran in 0.2s\n", 0),
    ("0 passed in 0.2s\n", 0),
    ("100 errors, 3546 passed\n", 0),
])
def test_pytest_pass_count_refuses_false_completion(output, code):
    with pytest.raises(RuntimeError):
        c.pytest_pass_count(output, code)


def test_five_language_appropriate_final_sections():
    sections = c.closure_sections(3551, "3551 passed in 29.4s")
    assert set(sections) == set(c.BASE_DOC_BLOBS)
    assert "Current status — Phase 171 closed" in sections["README.md"]
    assert "Phase 171 正式終了" in sections["docs/development_log.md"]
    for path, value in sections.items():
        assert value.count(c.FINAL_MARKER) == 1
        assert "3551 passed" in value
        assert "Phase 171" in value
        assert "pytest" in value
        if path != "README.md":
            assert "正式終了" in value or "終了" in value


def fake_before_docs() -> dict[str, bytes]:
    docs = {}
    for relative in c.BASE_DOC_BLOBS:
        if relative == "README.md":
            docs[relative] = (
                "# EHP Proof Tracer\n\n<!-- " + c.R2_MARKER + " -->\n\n"
                "## Phase 171 — pending\n\n# Phase 170 record\n"
            ).encode("utf-8")
        elif relative == "docs/design.md":
            docs[relative] = ("# Original\r\r\n\r\nHistory.\r\r\n\r\n## Phase 171 pending\r\n").encode("utf-8")
        else:
            docs[relative] = ("# 過去の本文\n\n## Phase 171 pending\n").encode("utf-8")
    return docs


def test_final_documents_preserve_every_historical_byte():
    before = fake_before_docs()
    sections = c.closure_sections(3563, "3563 passed in 55.3s")
    output = c.closure_documents(before, sections)
    assert set(output) == set(before)
    for path, original in before.items():
        updated = output[path]
        assert updated != original
        assert updated.count(c.FINAL_MARKER.encode("ascii")) == 1
        if path == "README.md":
            assert updated.startswith(b"# EHP Proof Tracer\n\n")
            index = updated.index(("<!-- " + c.R2_MARKER).encode("ascii"))
            assert updated[index:] == original[len(b"# EHP Proof Tracer\n\n"):]
        else:
            assert updated.startswith(original)
    assert b"History.\r\r\n" in output["docs/design.md"]
    assert b"\r\n<!-- " + c.FINAL_MARKER.encode("ascii") in output["docs/design.md"]


def test_second_final_update_refused():
    before = fake_before_docs()
    sections = c.closure_sections(3555, "3555 passed in 12.1s")
    first = c.closure_documents(before, sections)
    with pytest.raises(ValueError, match="already exists"):
        c.closure_documents(first, sections)


def test_missing_document_refused():
    before = fake_before_docs()
    before.pop("docs/design.md")
    with pytest.raises(ValueError, match="five"):
        c.closure_documents(before, c.closure_sections(1, "1 passed"))


def test_readme_marker_missing_refused():
    before = fake_before_docs()
    before["README.md"] = b"# README\n"
    with pytest.raises(ValueError, match="R2 marker"):
        c.closure_documents(before, c.closure_sections(1, "1 passed"))


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          text=True, encoding="utf-8")
    return proc.stdout.strip()


class FakeR2:
    @staticmethod
    def lf_text(data: bytes) -> str:
        return re.sub(r"\r+\n", "\n", data.decode("utf-8-sig"))

    @staticmethod
    def updated_document(path: str, original: bytes) -> bytes:
        if path == "README.md":
            return original.replace(b"# EHP Proof Tracer\n\n", (
                "# EHP Proof Tracer\n\n<!-- " + c.R2_MARKER + " -->\n\n"
            ).encode("utf-8"), 1)
        return original + b"\n## Phase 171 pending\n"


@pytest.fixture
def reviewed_repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    bare = tmp_path / "origin.git"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "develop", str(root)], check=True)
    git(root, "config", "user.name", "test")
    git(root, "config", "user.email", "test@example.invalid")
    for path in c.BASE_DOC_BLOBS:
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(
            b"# EHP Proof Tracer\n\n# Prior history\n" if path == "README.md"
            else b"# Past\n\nHistory\n"
        )
    for path in c.SOURCE_BLOBS:
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(b"# reviewed source\n")
    (root / "tests").mkdir()
    git(root, "add", ".")
    git(root, "commit", "-qm", "reviewed baseline")
    baseline = git(root, "rev-parse", "HEAD")
    git(root, "remote", "add", "origin", str(bare))
    git(root, "push", "-q", "-u", "origin", "develop")
    monkeypatch.setattr(c, "REVIEWED_HEAD", baseline)
    monkeypatch.setattr(c, "SOURCE_BLOBS", {
        path: git(root, "rev-parse", "HEAD:" + path) for path in c.SOURCE_BLOBS
    })
    monkeypatch.setattr(c, "BASE_DOC_BLOBS", {
        path: git(root, "rev-parse", "HEAD:" + path) for path in c.BASE_DOC_BLOBS
    })
    monkeypatch.setattr(c, "load_r2_writer", lambda root: FakeR2)
    for path in c.BASE_DOC_BLOBS:
        file = root / path
        file.write_bytes(FakeR2.updated_document(path, file.read_bytes()))
    return root


def test_preflight_allows_exactly_the_five_r2_documents(reviewed_repo):
    audit = c.preflight(reviewed_repo)
    assert set(audit["tracked_before"]) == set(c.BASE_DOC_BLOBS)
    assert audit["head"] == c.REVIEWED_HEAD
    assert all(audit["document_bytes"].values())


def test_preflight_refuses_dirty_production_source(reviewed_repo):
    source = next(iter(c.SOURCE_BLOBS))
    (reviewed_repo / source).write_text("# unreviewed source\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unexpected tracked changes"):
        c.preflight(reviewed_repo)


def test_preflight_refuses_unexpected_tracked_path(reviewed_repo):
    file = reviewed_repo / "extra.py"
    file.write_text("x = 1\n", encoding="utf-8")
    git(reviewed_repo, "add", "extra.py")
    with pytest.raises(RuntimeError, match="staged"):
        c.preflight(reviewed_repo)


def test_preflight_refuses_unreviewed_document_change(reviewed_repo):
    doc = reviewed_repo / "docs/roadmap.md"
    doc.write_bytes(doc.read_bytes() + b"\nunknown addition\n")
    with pytest.raises(RuntimeError, match="unexpected content"):
        c.preflight(reviewed_repo)


def test_preflight_accepts_committed_five_docs_in_descendant(reviewed_repo):
    git(reviewed_repo, "add", "README.md", "docs")
    git(reviewed_repo, "commit", "-qm", "commit reviewed R2 docs")
    git(reviewed_repo, "push", "-q", "origin", "develop")
    audit = c.preflight(reviewed_repo)
    assert audit["tracked_before"] == []
    assert set(audit["committed_delta"]) == set(c.BASE_DOC_BLOBS)


def test_preflight_refuses_unrelated_committed_code(reviewed_repo):
    source = next(iter(c.SOURCE_BLOBS))
    (reviewed_repo / source).write_text("# changed source\n", encoding="utf-8")
    git(reviewed_repo, "add", source)
    git(reviewed_repo, "commit", "-qm", "unreviewed code")
    git(reviewed_repo, "push", "-q", "origin", "develop")
    with pytest.raises(RuntimeError, match="unexpected committed files"):
        c.preflight(reviewed_repo)


def test_dry_run_runs_no_full_suite_and_changes_no_docs(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    monkeypatch.setattr(c, "run_full_suite", lambda *args: pytest.fail("full suite invoked in dry-run"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    assert c.run(reviewed_repo, dry_run=True, resume_report=None) == 0
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}


def test_successful_end_gate_writes_five_full_docs(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    calls = []
    def fake_full(root, output):
        calls.append(True)
        return 3555, "3555 passed in 39.12s", 0
    monkeypatch.setattr(c, "run_full_suite", fake_full)
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 0
    assert len(calls) == 1
    assert all(c.FINAL_MARKER in (reviewed_repo / p).read_text(encoding="utf-8") for p in c.BASE_DOC_BLOBS)
    folders = list((tmp_path / "local" / "EHPProofTracerRecovery").glob("phase171_closeout_r3_*/"))
    assert len(folders) == 1
    folder = folders[0]
    with zipfile.ZipFile(folder / "PHASE171_FINAL_FIVE_FULL_DOCUMENTS.zip") as z:
        assert set(z.namelist()) == set(c.BASE_DOC_BLOBS)
        for path in c.BASE_DOC_BLOBS:
            assert z.read(path) == (reviewed_repo / path).read_bytes()


def test_failed_end_gate_never_changes_documents(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    def fake_fail(root, output):
        raise RuntimeError("pytest failed")
    monkeypatch.setattr(c, "run_full_suite", fake_fail)
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 1
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}


def test_windows_runner_passes_named_arguments():
    runner = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "& python @PythonArguments" in runner
    assert "& python @Args" not in runner
    assert "if ($DryRun)" in runner
    assert "'--resume-report'" in runner


def test_nonzero_full_suite_stores_exit_and_does_not_close(reviewed_repo, tmp_path, monkeypatch):
    import json
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    monkeypatch.setattr(c, "run_full_suite", lambda root, output: (0, "FULL_SUITE_FAILED_EXIT_1", 1))
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 1
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    reports = list((tmp_path / "local" / "EHPProofTracerRecovery").glob("phase171_closeout_r3_*/closeout.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["pytest_exit"] == 1
    assert report["full_suite_verified"] is False
    assert report["result"] == "REFUSED_OR_FAILED"


def test_resume_a_verified_gate_without_second_full_suite(reviewed_repo, tmp_path, monkeypatch):
    import json
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    baseline = c.preflight(reviewed_repo)
    report_file = tmp_path / "verified.json"
    report_file.write_text(json.dumps({
        "phase": "171_CLOSEOUT_R3", "pytest_exit": 0,
        "full_suite_verified": True, "pytest_passed": 3561,
        "pytest_summary": "3561 passed in 40.31s",
        "preflight": {"head": baseline["head"]},
        "documents_before_sha256": baseline["document_sha256"],
    }), encoding="utf-8")
    monkeypatch.setattr(c, "run_full_suite", lambda *args: pytest.fail("full suite attempted twice"))
    assert c.run(reviewed_repo, dry_run=False, resume_report=report_file) == 0
    assert all(c.FINAL_MARKER.encode("ascii") in (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS)

```

