"""Phase 174 R73: full-document output and guarded documentation-only installation.

R73 is not the Phase 174 final gate. Historical documents are preserved byte for
byte outside a single README insertion or an append-only section per other file.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

PACKAGE = "phase174_r3_r7_r73_closeout_documents"
BASE_HEAD = "b66099598177d74e979492f1d04a916e6f0821a8"
R72_AUDIT_BLOB = "c6f6621ef6cbd121981436d79b79ac18bf73d26a"
PREPARATION_MARKER = "PHASE174_R73_CLOSEOUT_PREPARATION_20261111"
PHASE173_MARKER = "PHASE173_FINAL_CLOSEOUT_20261105"
DOC_BLOBS = {
    "README.md": "1b8550ea20670e177bfd008b5878a5a3518d1b3f",
    "docs/design.md": "a2a1f3c72f3626b9090d34f1158a5f9a5d8a7642",
    "docs/development_log.md": "8c7d3b5e83071ec7265e468f5c10f6d337603f4e",
    "docs/roadmap.md": "481745c727dc9081f684af0d256cc6599f18c610",
    "docs/proof_records.md": "55b2751857465616996d0d9eb73b6eb5ec650e18",
}
TEMPLATES = {
    "README.md": "README.md",
    "docs/design.md": "design.md",
    "docs/development_log.md": "development_log.md",
    "docs/roadmap.md": "roadmap.md",
    "docs/proof_records.md": "proof_records.md",
}


def git(root: Path, *args: str, allow_failure: bool = False) -> str:
    """Run a read-only Git command at the repository root."""
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if result.returncode and not allow_failure:
        raise RuntimeError("R73_GIT_COMMAND_FAILED: " + " ".join(args)
                              + " " + result.stderr.strip())
    return result.stdout.strip()


def git_blob_sha(raw: bytes) -> str:
    """Compute a real Git blob identity, never a newline-normalized guess."""
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def require_r72_audit_source(root: Path) -> None:
    """Pin the R72 audit module that generated the prior structured record."""
    path = root / "phase174_r3_r7_r72_closeout_preflight" / "audit.py"
    raw = path.read_bytes()
    lf = raw.replace(b"\r\n", b"\n")
    if b"\r" in lf:
        raise RuntimeError("R73_R72_SOURCE_MIXED_EOL")
    variants = (raw, lf, lf.replace(b"\n", b"\r\n"))
    if R72_AUDIT_BLOB not in {git_blob_sha(value) for value in variants}:
        raise RuntimeError("R73_R72_AUDIT_SOURCE_CHANGED")


def validate_r72_report(report: object) -> None:
    """Accept the actual focused R72 evidence; do not relabel it a full suite."""
    if not isinstance(report, dict) or report.get("phase") != "174-R72":
        raise RuntimeError("R73_R72_REPORT_INVALID_PHASE")
    if (report.get("local_head") != BASE_HEAD
            or report.get("origin_develop") != BASE_HEAD
            or report.get("r71_complete_case_count") != 8
            or report.get("r71_focused_pytest_passed") != 81
            or report.get("r71_focused_pytest_is_user_reported") is not True
            or report.get("whole_test_suite_executed") is not False
            or report.get("phase174_closed") is not False
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("production_changes") != []):
        raise RuntimeError("R73_R72_REPORT_SCOPE_CHANGED")
    incomplete = report.get("incomplete_public_cases")
    if not isinstance(incomplete, list) or len(incomplete) != 2:
        raise RuntimeError("R73_R72_INCOMPLETE_SET_CHANGED")
    if {(entry.get("group"), entry.get("status"), entry.get("web_key"))
        for entry in incomplete if isinstance(entry, dict)} != {
            ("pi_12^4", "SEARCH_FAILED", "generic-partial-proof"),
            ("pi_35^4", "SEARCH_FAILED", "generic-partial-proof"),
        }:
        raise RuntimeError("R73_R72_INCOMPLETE_CONTRACT_CHANGED")
    if set(report.get("missing_phase174_closeout_records", ())) != set(DOC_BLOBS):
        raise RuntimeError("R73_R72_FIVE_DOCUMENT_GAPS_CHANGED")


def read_r72_report() -> dict[str, object]:
    """Read R72's saved actual-run report from the current Windows account."""
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    path = folder / "EHPProofTracerAudit" / "phase174_r3_r7_r72_closeout_preflight" / "report.json"
    if not path.is_file():
        raise RuntimeError("R73_R72_REPORT_NOT_FOUND: " + str(path))
    report = json.loads(path.read_text(encoding="utf-8"))
    validate_r72_report(report)
    return report


def choose_eol(original: bytes) -> bytes:
    """Preserve the historical byte stream; select only new section line ends."""
    return b"\r\n" if original.count(b"\r\n") > original.count(b"\n") // 2 else b"\n"


def render_full_document(name: str, original: bytes, section: str) -> bytes:
    """Return the COMPLETE final file, not a patch or truncated excerpt."""
    if name not in TEMPLATES:
        raise ValueError("R73_UNKNOWN_DOCUMENT")
    decoded = original.decode("utf-8-sig")
    if (not decoded.lstrip().startswith("# EHP Proof Tracer")
            or PHASE173_MARKER not in decoded
            or PREPARATION_MARKER in decoded
            or "PHASE174_FINAL_CLOSEOUT" in decoded):
        raise RuntimeError("R73_BASE_DOCUMENT_UNEXPECTED: " + name)
    if (section.count(PREPARATION_MARKER) != 1
            or "Phase 174" not in section
            or "pytest" not in section
            or "正式終了していない" not in section and name != "README.md"
               and "正式終了前" not in section and "終了前" not in section):
        raise RuntimeError("R73_TEMPLATE_CONTRACT_FAILED: " + name)
    if name == "README.md" and "not formally closed" not in section:
        raise RuntimeError("R73_README_MUST_REMAIN_ENGLISH")
    eol = choose_eol(original)
    addition = section.replace("\r\n", "\n").strip("\n").replace("\n", eol.decode()).encode("utf-8")
    if name == "README.md":
        anchor = b"<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->"
        if original.count(anchor) != 1:
            raise RuntimeError("R73_README_ANCHOR_NOT_UNIQUE")
        result = original.replace(anchor, addition + eol + eol + anchor, 1)
        if result.replace(addition + eol + eol, b"", 1) != original:
            raise RuntimeError("R73_README_HISTORY_DID_NOT_SURVIVE")
    else:
        separator = eol if original.endswith(b"\n") else eol + eol
        result = original + separator + addition + eol
        if not result.startswith(original):
            raise RuntimeError("R73_APPEND_HISTORY_DID_NOT_SURVIVE")
    if result.count(PREPARATION_MARKER.encode("ascii")) != 1:
        raise RuntimeError("R73_DOCUMENT_MARKER_DUPLICATED")
    result.decode("utf-8-sig")
    return result


def require_reviewed_tree(root: Path) -> tuple[str, str]:
    """Allow a descendant of R72 only while the five reviewed blobs remain."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream = git(root, "rev-parse", "origin/develop")
    if branch != "develop" or upstream != head:
        raise RuntimeError("R73_UNREVIEWED_BRANCH_OR_UPSTREAM")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_HEAD, head], cwd=root,
        capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R73_UNREVIEWED_HEAD_LINEAGE")
    for name, reviewed in DOC_BLOBS.items():
        blob = git(root, "rev-parse", "HEAD:" + name)
        if blob != reviewed:
            raise RuntimeError("R73_UNREVIEWED_DOCUMENT_BLOB: " + name)
    return head, upstream


def tracked_changes(root: Path) -> tuple[str, ...]:
    """Reject staged changes and any unrelated tracked worktree edits."""
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("R73_STAGED_CHANGES_PRESENT")
    changes = tuple(line.strip() for line in git(root, "diff", "--name-only").splitlines()
                    if line.strip())
    if any(path not in DOC_BLOBS for path in changes):
        raise RuntimeError("R73_UNRELATED_TRACKED_CHANGES")
    return changes


def planned_files(root: Path, package: Path) -> dict[str, tuple[bytes, bytes]]:
    """Build five full-file candidates from the user's exact checked-out docs."""
    plans: dict[str, tuple[bytes, bytes]] = {}
    for name, template in TEMPLATES.items():
        original = (root / name).read_bytes()
        text = (package / "updates" / template).read_text(encoding="utf-8")
        plans[name] = (original, render_full_document(name, original, text))
    return plans


def apply_complete_documents(root: Path, package: Path,
                             plans: dict[str, tuple[bytes, bytes]]) -> Path:
    """Write complete output files, preserve exact baselines and install five docs."""
    output = package / "output"
    originals_dir = output / "original_files"
    full_dir = output / "full_files"
    originals_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)
    for name, (original, changed) in plans.items():
        before = originals_dir / name
        after = full_dir / name
        before.parent.mkdir(parents=True, exist_ok=True)
        after.parent.mkdir(parents=True, exist_ok=True)
        before.write_bytes(original)
        after.write_bytes(changed)
        if after.read_bytes() != changed or before.read_bytes() != original:
            raise RuntimeError("R73_FULL_DOCUMENT_OUTPUT_MISMATCH: " + name)
    archive = output / "phase174_r73_complete_documents.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in DOC_BLOBS:
            bundle.write(full_dir / name, arcname=name)
    for name, (original, changed) in plans.items():
        current = root / name
        if current.read_bytes() != original:
            raise RuntimeError("R73_SOURCE_CHANGED_DURING_PREPARATION: " + name)
        if not changed:
            raise RuntimeError("R73_EMPTY_DOCUMENT")
    installed: list[str] = []
    try:
        for name, (_, changed) in plans.items():
            current = root / name
            temporary = current.with_name(current.name + ".r73-tmp")
            temporary.write_bytes(changed)
            os.replace(temporary, current)
            installed.append(name)
    except OSError:
        for name in reversed(installed):
            current = root / name
            temporary = current.with_name(current.name + ".r73-rollback")
            temporary.write_bytes(plans[name][0])
            os.replace(temporary, current)
        raise
    for name, (_, changed) in plans.items():
        if (root / name).read_bytes() != changed:
            raise RuntimeError("R73_INSTALLED_DOCUMENT_CHANGED: " + name)
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    root = package.parent
    head, upstream = require_reviewed_tree(root)
    require_r72_audit_source(root)
    prior = read_r72_report()
    changes = tracked_changes(root)
    print("PHASE174_R73_SOURCE_GUARD=PASS")
    print("PHASE174_R73_SOURCE_PINS=" + str(len(DOC_BLOBS) + 1))
    print("PHASE174_R73_HEAD=" + head)
    print("PHASE174_R73_ORIGIN_DEVELOP=" + upstream)
    print("PHASE174_R73_R72_PREVIOUS_COMPLETE_CASES=" + str(prior["r71_complete_case_count"]))
    print("PHASE174_R73_PRODUCTION_CHANGES=0")

    output = package / "output"
    full_dir = output / "full_files"
    previously_installed = bool(changes) or all(
        PREPARATION_MARKER.encode("ascii") in (root / name).read_bytes()
        for name in DOC_BLOBS
    )
    if previously_installed:
        if set(changes) != set(DOC_BLOBS):
            raise RuntimeError("R73_INCONSISTENT_APPLIED_DOCUMENT_SET")
        for name in DOC_BLOBS:
            target = full_dir / name
            if not target.is_file() or target.read_bytes() != (root / name).read_bytes():
                raise RuntimeError("R73_APPLIED_FILE_NOT_OWNED_BY_PACKAGE: " + name)
        print("PHASE174_R73_DOC_STATUS=ALREADY_APPLIED")
        print("PHASE174_R73_GATE=PASS_R73_ALREADY_APPLIED")
        print("(END)")
        return 0

    plans = planned_files(root, package)
    for name, (_, changed) in plans.items():
        print("PHASE174_R73_PLANNED_DOCUMENT=" + name + ":" + str(len(changed))
              + "_BYTES:SHA256_" + sha256(changed).hexdigest())
    if args.dry_run:
        print("PHASE174_R73_DOC_STATUS=PATCH_REQUIRED")
        print("PHASE174_R73_FULL_PYTEST_EXECUTED=False")
        print("PHASE174_R73_PHASE_CLOSED=False")
        print("PHASE174_R73_GATE=PASS_R73_READ_ONLY_DRYRUN")
        print("(END)")
        return 0

    archive = apply_complete_documents(root, package, plans)
    record = {
        "phase": "174-R73",
        "head_at_document_write": head,
        "documents": [
            {"path": name, "baseline_git_blob": DOC_BLOBS[name],
             "full_file_sha256": sha256(changed).hexdigest(),
             "full_file_bytes": len(changed)}
            for name, (_, changed) in plans.items()
        ],
        "full_documents_archive": str(archive),
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 0,
        "whole_test_suite_executed": False,
        "phase174_closed": False,
    }
    report = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("PHASE174_R73_FULL_DOCUMENTS_WRITTEN=" + str(len(plans)))
    print("PHASE174_R73_ARCHIVE=" + str(archive))
    print("PHASE174_R73_REPORT=" + str(report))
    print("PHASE174_R73_NEW_GIVEN=0")
    print("PHASE174_R73_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R73_FULL_PYTEST_EXECUTED=False")
    print("PHASE174_R73_PHASE_CLOSED=False")
    print("PHASE174_R73_GATE=PASS_R73_COMPLETE_DOCUMENTS_PRE_FINAL")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
