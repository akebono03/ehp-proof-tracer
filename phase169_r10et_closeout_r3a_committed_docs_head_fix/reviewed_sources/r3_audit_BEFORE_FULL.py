"""Read-only review of five R10ET documents, source blobs and final R6 evidence.

The report is saved outside the repository. No checkout, reset, add, commit,
production edit or repository-wide pytest is performed by this module.
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
import traceback
from typing import Any

sys.dont_write_bytecode = True

REVIEWED_HEAD = "a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5"
BACKUP_NAME = "r10et_closeout_r2_20261028_183606_606010"
R6_REPORT = (
    "phase169_r10et_r6_residual_definition_dependency_audit/"
    "output/20261028_174644_215/audit.json"
)
REQUIRED_NAMES = {
    "pi_69^43", "pi_56^30", "pi_41^30", "pi_44^30", "pi_46^30",
    "pi_39^30", "pi_3^2", "pi_4^3", "pi_5^4", "pi_4^2",
    "pi_5^3", "pi_6^4", "pi_28^22", "pi_32^22", "pi_23^15",
    "pi_33^24",
}
PROBE_NAMES = {"pi_10^8", "pi_22^13", "pi_24^15"}


def git(root: Path, *args: str, input_bytes: bytes | None = None) -> str:
    env = os.environ.copy()
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"})
    proc = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *args],
        input=input_bytes, capture_output=True, timeout=35, check=False, env=env,
    )
    if proc.returncode:
        raise RuntimeError(
            f"Git {args!r} failed (exit {proc.returncode}): "
            + proc.stderr.decode("utf-8", "replace").strip()
        )
    return proc.stdout.decode("utf-8", "replace").strip()


def review_r6_report(report: dict[str, Any]) -> tuple[int, int]:
    """Fail closed on missing/duplicate/failed proof cases or a missing trust check."""
    if not isinstance(report, dict):
        raise ValueError("R6 report must be a JSON object")
    if not (report.get("source_verified") is True
            and report.get("tracked_unchanged") is True
            and report.get("required_pass") is True
            and report.get("probes_pass") is True
            and report.get("full_pytest_run") is False):
        raise ValueError("R6 report has not passed its original certification")
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 19:
        raise ValueError("R6 report must contain exactly nineteen cases")
    names: set[str] = set()
    required: set[str] = set()
    probes: set[str] = set()
    for item in cases:
        if not isinstance(item, dict) or not isinstance(item.get("case"), str):
            raise ValueError("R6 case is malformed")
        name = item["case"]
        if name in names:
            raise ValueError("R6 case is duplicated: " + name)
        names.add(name)
        (required if item.get("required") is True else probes).add(name)
        if not (item.get("passed") is True
                and item.get("status") == "complete"
                and item.get("trust") == "PASS"
                and item.get("remaining_eligible_cited_steps") == 0
                and item.get("problems") == []):
            raise ValueError("R6 case not verified: " + name)
    if required != REQUIRED_NAMES or probes != PROBE_NAMES:
        raise ValueError("R6 required/probe target set changed")
    pi108 = next(item for item in cases if item["case"] == "pi_10^8")
    if not (pi108.get("canonical_image_steps") == 4
            and pi108.get("eligible_image_steps") == 4
            and len(pi108.get("reference_locators", [])) == 2):
        raise ValueError("R6 pi_10^8 definition/reference regression")
    return len(required), len(probes)


def certify_documents(root: Path, backup: Path) -> list[dict[str, Any]]:
    """Verify all five complete documents against the exact R2A output archive."""
    from phase169_r10et_closeout_r2_documentation.update_docs import (
        APPENDIX_PATHS, DOCUMENT_BLOBS, updated_document,
    )

    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if (manifest.get("head") != REVIEWED_HEAD
            or manifest.get("phase_169_closed") is not False
            or manifest.get("full_pytest_executed") is not False
            or manifest.get("index_modified") is not False):
        raise RuntimeError("Unexpected R2A backup manifest")
    records = manifest.get("documents")
    if not isinstance(records, list) or {x.get("path") for x in records} != set(DOCUMENT_BLOBS):
        raise RuntimeError("R2A manifest has missing or extra documents")
    archive = backup / "updated_five_documents_FULL.zip"
    import zipfile
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or set(z.namelist()) != set(DOCUMENT_BLOBS):
            raise RuntimeError("R2A full-document archive is incomplete or corrupt")
        for path in DOCUMENT_BLOBS:
            if z.read(path) != (backup / "AFTER_FULL" / path).read_bytes():
                raise RuntimeError("Archive and backed-up final document differ: " + path)

    output = []
    appendix_root = root / "phase169_r10et_closeout_r2_documentation" / "appendices"
    for path, expected_blob in DOCUMENT_BLOBS.items():
        record = next(x for x in records if x["path"] == path)
        before = (backup / "BEFORE_FULL" / path).read_bytes()
        after = (backup / "AFTER_FULL" / path).read_bytes()
        current = (root / path).read_bytes()
        appendix = (appendix_root / APPENDIX_PATHS[path]).read_text(encoding="utf-8")
        reproduced = updated_document(path, before, appendix)
        blob = git(root, "hash-object", f"--path={path}", "--stdin", input_bytes=before)
        if (blob != expected_blob
                or record.get("before_git_blob") != blob
                or hashlib.sha256(before).hexdigest() != record.get("before_sha256")
                or hashlib.sha256(after).hexdigest() != record.get("after_sha256")
                or reproduced != after
                or current != after):
            raise RuntimeError("Document bytes or baseline differ: " + path)
        output.append({"path": path, "after_sha256": hashlib.sha256(after).hexdigest()})
    return output


def snapshot(root: Path) -> tuple[str, str, str]:
    return (
        git(root, "rev-parse", "HEAD"),
        git(root, "diff", "--name-only"),
        git(root, "diff", "--cached", "--name-only"),
    )


def execute(root: Path) -> int:
    from phase169_r10et_closeout_r2_documentation.update_docs import (
        DOCUMENT_BLOBS, REVIEWED_SOURCE_BLOBS,
    )

    baseline = snapshot(root)
    if not (root / ".git").exists() or git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop Git repository")
    if baseline[0] != REVIEWED_HEAD:
        raise RuntimeError("Local HEAD differs from reviewed GitHub commit")
    if git(root, "rev-parse", "refs/remotes/origin/develop") != REVIEWED_HEAD:
        raise RuntimeError("origin/develop tracking ref differs")
    remote = git(root, "ls-remote", "origin", "refs/heads/develop")
    if remote != REVIEWED_HEAD + "\trefs/heads/develop":
        raise RuntimeError("Remote develop moved; review the new commit first")
    if baseline[2]:
        raise RuntimeError("Staged changes must be reviewed separately")
    if set(baseline[1].splitlines()) != set(DOCUMENT_BLOBS):
        raise RuntimeError("Tracked unstaged changes must be exactly the five documents")
    for path, expected_blob in REVIEWED_SOURCE_BLOBS.items():
        if git(root, "hash-object", f"--path={path}", path) != expected_blob:
            raise RuntimeError("Production source/test differs: " + path)
    backup = Path(os.environ["LOCALAPPDATA"]).resolve() / "EHPProofTracerRecovery" / BACKUP_NAME
    documents = certify_documents(root, backup)
    r6 = json.loads((root / R6_REPORT).read_text(encoding="utf-8"))
    required, probes = review_r6_report(r6)
    if snapshot(root) != baseline:
        raise RuntimeError("Git HEAD, tracked changes or index changed during audit")
    root_resolved = root.resolve()
    report_dir = backup.parent / ("r10et_closeout_r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    report_dir_resolved = report_dir.resolve()
    if report_dir_resolved == root_resolved or root_resolved in report_dir_resolved.parents:
        raise RuntimeError("Audit output must be outside the repository")
    report_dir.mkdir(parents=True, exist_ok=False)
    report = {
        "mode": "AUDIT_ONLY", "head": REVIEWED_HEAD,
        "documents": documents, "r6_required_pass": required,
        "r6_probes_pass": probes, "source_count": len(REVIEWED_SOURCE_BLOBS),
        "tracked_unchanged": True, "full_pytest_run": False,
        "r10et_complete": True, "phase169_complete": False,
        "decision": "R10ET_DOCUMENT_CLOSED_PHASE169_STILL_OPEN",
    }
    (report_dir / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (report_dir / "audit.md").write_text(
        "# R10ET Closeout R3 — 完了文書・監査根拠の照合\n\n"
        + "- R10ET 文書5件: 全文一致。\n"
        + "- 監査対象の本番実装・テスト8件: GitHub commit と一致。\n"
        + f"- R6 必須: {required}/16 PASS、追加: {probes}/3 PASS。\n"
        + "- Git index と既存差分: 保持。\n"
        + "- Phase 169 全体 pytest・終了判定: 未実施。\n",
        encoding="utf-8",
    )
    print("R10ET_CLOSEOUT_R3_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("R10ET_CLOSEOUT_R3_DOCUMENTS=5/5_PASS")
    print("R10ET_CLOSEOUT_R3_SOURCES=8/8_PASS")
    print(f"R10ET_CLOSEOUT_R3_R6_CASES={required + probes}/19_PASS")
    print("R10ET_CLOSEOUT_R3_INDEX_PRESERVED=True")
    print("R10ET_CLOSEOUT_R3_FULL_PYTEST_NOT_RUN=True")
    print("R10ET_CLOSEOUT_R3_DECISION=R10ET_DOCUMENT_CLOSED_PHASE169_STILL_OPEN")
    print("R10ET_CLOSEOUT_R3_REPORT=" + str(report_dir / "audit.md"))
    print("R10ET_CLOSEOUT_R3_EXIT=0")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args(argv)
    print("R10ET_CLOSEOUT_R3_MODE=AUDIT_ONLY", flush=True)
    try:
        return execute(args.repo.resolve())
    except BaseException:
        print("R10ET_CLOSEOUT_R3_ERROR=" + traceback.format_exc(), flush=True)
        print("R10ET_CLOSEOUT_R3_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
