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
