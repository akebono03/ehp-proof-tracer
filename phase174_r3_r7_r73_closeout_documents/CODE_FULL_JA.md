# Phase 174 R73 — 追加コードと5文書の新節全文

以下は今回追加するコード・テスト・スクリプト・Markdown 新節の全文。既存本番ソースの関数・クラス・import は変更しない。主要5文書の更新後全文は、実行時に `output/full_files/` へ出力する。


## `audit.py`

```python
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
```


## `tests/test_audit.py`

```python
"""Isolated R73 documentation-only full-file output contracts."""
from __future__ import annotations

from pathlib import Path
import zipfile

import pytest

from phase174_r3_r7_r73_closeout_documents.audit import (
    BASE_HEAD,
    DOC_BLOBS,
    PACKAGE,
    PHASE173_MARKER,
    R72_AUDIT_BLOB,
    PREPARATION_MARKER,
    TEMPLATES,
    apply_complete_documents,
    choose_eol,
    git_blob_sha,
    render_full_document,
    require_r72_audit_source,
    validate_r72_report,
)


def sample_document(name: str, *, eol: bytes = b"\n") -> bytes:
    original = ("# EHP Proof Tracer\n\n<!-- " + PHASE173_MARKER + " -->"
                + "\n\n## Historical Phase 173\n\nPast text stays.\n")
    if name == "README.md":
        return original.encode().replace(b"\n", eol)
    return original.encode().replace(b"\n", eol)


def get_template(name: str) -> str:
    package = Path(__file__).resolve().parents[1]
    return (package / "updates" / TEMPLATES[name]).read_text(encoding="utf-8")


def example_r72_report() -> dict[str, object]:
    return {
        "phase": "174-R72", "local_head": BASE_HEAD,
        "origin_develop": BASE_HEAD, "r71_complete_case_count": 8,
        "r71_focused_pytest_passed": 81,
        "r71_focused_pytest_is_user_reported": True,
        "whole_test_suite_executed": False, "phase174_closed": False,
        "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": [],
        "incomplete_public_cases": [
            {"group": "pi_12^4", "status": "SEARCH_FAILED",
             "web_key": "generic-partial-proof"},
            {"group": "pi_35^4", "status": "SEARCH_FAILED",
             "web_key": "generic-partial-proof"},
        ],
        "missing_phase174_closeout_records": list(DOC_BLOBS),
    }


@pytest.mark.parametrize("name", list(DOC_BLOBS))
def test_all_five_outputs_are_complete_and_preserve_history(name: str) -> None:
    original = sample_document(name)
    output = render_full_document(name, original, get_template(name))
    assert output.count(PREPARATION_MARKER.encode()) == 1
    assert PHASE173_MARKER.encode() in output
    if name == "README.md":
        assert output.replace(
            get_template(name).strip().encode() + b"\n\n", b"", 1,
        ) == original
    else:
        assert output.startswith(original)
    assert len(output) > len(original)


def test_readme_insertion_is_before_historical_phase173_record() -> None:
    original = sample_document("README.md")
    output = render_full_document("README.md", original,
                                  get_template("README.md"))
    assert output.index(PREPARATION_MARKER.encode()) < output.index(PHASE173_MARKER.encode())


def test_crlf_document_preserved_exactly() -> None:
    original = sample_document("docs/design.md", eol=b"\r\n")
    output = render_full_document("docs/design.md", original,
                                  get_template("docs/design.md"))
    assert choose_eol(original) == b"\r\n"
    assert output.startswith(original)
    assert b"\r\n" in output


def test_duplicate_preparation_marker_rejected() -> None:
    name = "docs/proof_records.md"
    original = sample_document(name) + PREPARATION_MARKER.encode()
    with pytest.raises(RuntimeError, match="R73_BASE_DOCUMENT_UNEXPECTED"):
        render_full_document(name, original, get_template(name))


def test_missing_prior_phase_record_rejected() -> None:
    with pytest.raises(RuntimeError, match="R73_BASE_DOCUMENT_UNEXPECTED"):
        render_full_document("README.md", b"# EHP Proof Tracer\n",
                             get_template("README.md"))


def test_new_documents_do_not_claim_a_final_closeout() -> None:
    for name in DOC_BLOBS:
        section = get_template(name)
        assert "PHASE174_FINAL_CLOSEOUT" not in section
        assert section.count(PREPARATION_MARKER) == 1
        assert "pytest" in section


def test_r72_prior_report_is_focused_only() -> None:
    validate_r72_report(example_r72_report())


def test_r72_report_rejects_fabricated_full_suite() -> None:
    report = example_r72_report()
    report["whole_test_suite_executed"] = True
    with pytest.raises(RuntimeError, match="R73_R72_REPORT_SCOPE_CHANGED"):
        validate_r72_report(report)


def test_r72_report_rejects_promoted_incomplete_goal() -> None:
    report = example_r72_report()
    report["incomplete_public_cases"][0]["status"] = "COMPLETE"
    with pytest.raises(RuntimeError, match="R73_R72_INCOMPLETE_CONTRACT_CHANGED"):
        validate_r72_report(report)


def test_full_file_archive_contains_five_complete_documents(tmp_path: Path) -> None:
    root = tmp_path
    package = root / PACKAGE
    package.mkdir(parents=True)
    plans = {}
    for name in DOC_BLOBS:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        source = sample_document(name)
        path.write_bytes(source)
        plans[name] = (source, render_full_document(name, source, get_template(name)))
    archive = apply_complete_documents(root, package, plans)
    assert archive.is_file()
    assert sorted(DOC_BLOBS) == sorted(
        zipfile.ZipFile(archive).namelist())
    with zipfile.ZipFile(archive) as bundle:
        for name, (_, result) in plans.items():
            assert bundle.read(name) == result
            assert (root / name).read_bytes() == result
            assert (package / "output" / "full_files" / name).read_bytes() == result
            assert (package / "output" / "original_files" / name).read_bytes() != result


def test_known_git_blob_hash() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_reviewed_tree_rejects_diverged_origin(monkeypatch: pytest.MonkeyPatch,
                                              tmp_path: Path) -> None:
    import phase174_r3_r7_r73_closeout_documents.audit as module

    def fake_git(root: Path, *args: str, allow_failure: bool = False) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return BASE_HEAD
        if args == ("rev-parse", "origin/develop"):
            return "f" * 40
        raise AssertionError("Unexpected git invocation")

    monkeypatch.setattr(module, "git", fake_git)
    with pytest.raises(RuntimeError, match="R73_UNREVIEWED_BRANCH_OR_UPSTREAM"):
        module.require_reviewed_tree(tmp_path)


def test_tracked_changes_rejects_unrelated_edit(monkeypatch: pytest.MonkeyPatch,
                                                tmp_path: Path) -> None:
    import phase174_r3_r7_r73_closeout_documents.audit as module

    def fake_git(root: Path, *args: str, allow_failure: bool = False) -> str:
        if args == ("diff", "--cached", "--name-only"):
            return ""
        if args == ("diff", "--name-only"):
            return "toda_group_proof_narrative_renderer.py"
        raise AssertionError("Unexpected git invocation")

    monkeypatch.setattr(module, "git", fake_git)
    with pytest.raises(RuntimeError, match="R73_UNRELATED_TRACKED_CHANGES"):
        module.tracked_changes(tmp_path)


def test_guard_rejects_wrong_document_templates() -> None:
    original = sample_document("docs/design.md")
    with pytest.raises(RuntimeError, match="R73_TEMPLATE_CONTRACT_FAILED"):
        render_full_document("docs/design.md", original,
                             "## Phase 174\nNo phase marker or pytest result.\n")


def test_r72_audit_source_pin_rejects_changed_bytes(tmp_path: Path) -> None:
    path = tmp_path / "phase174_r3_r7_r72_closeout_preflight" / "audit.py"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"# unreviewed content\n")
    with pytest.raises(RuntimeError, match="R73_R72_AUDIT_SOURCE_CHANGED"):
        require_r72_audit_source(tmp_path)


def test_r72_audit_source_pin_matches_original_archive() -> None:
    source_root = Path(__file__).resolve().parents[2]
    path = source_root / "phase174_r3_r7_r72_closeout_preflight" / "audit.py"
    if not path.is_file():
        pytest.skip("R72 archive is not installed beside this isolated test")
    raw = path.read_bytes()
    lf = raw.replace(b"\r\n", b"\n")
    assert R72_AUDIT_BLOB in {
        git_blob_sha(raw), git_blob_sha(lf),
        git_blob_sha(lf.replace(b"\n", b"\r\n")),
    }
```


## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$package = 'phase174_r3_r7_r73_closeout_documents'

python -B -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R73 reviewed-source and prior-report preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R73_GATE=PASS_R73_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r72_closeout_preflight/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R73 focused pytest failed before document write' }

python -B -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R73 five full-document installation failed' }

Write-Output 'PHASE174_R73_GATE=PASS_R73_FOCUSED_AND_FIVE_FULL_DOCUMENTS'
Write-Output '(END)'
```


## `__init__.py`

```python
"""Phase 174 R73 full-document closeout preparation package."""
```


## `updates/README.md`（追記・挿入する新節の全文）

<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## Current status — Phase 174 closeout preparation (2026-11-11)

**Phase 174 is not formally closed.** R71 and R72 passed their focused and public regression gates. The single phase-end active `pytest tests/` suite and final Git/documentation review remain pending. No full-suite pass or final Phase 174 closeout is claimed here.

The verified public examples include $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ and $\pi_{12}^{7}=0$, both with `generic-complete-proof` provenance and, respectively, 7 and 3 cited references. The latter reuses an earlier admitted database result for $\pi_{11}^{6}$ instead of reproving it. R70/R70R1 improved the common narrative through source-backed, typed ProofStep relationships; these display improvements introduced no new GIVEN or mathematical inference rule.

R71 reported **81 focused tests passed** and checked eight completed public queries and reference counts: $\pi_6^3$ (8), $\pi_7^4$ (4), $\pi_8^4$ (4), $\pi_9^4$ (4), $\pi_{11}^4$ (4), $\pi_8^5$ (7), $\pi_{11}^6$ (7), and $\pi_{12}^7$ (3). R72 reported **38 focused tests passed**, validated the retained R71 evidence, and checked that the named-generator goals for $\pi_{12}^4$ and $\pi_{35}^4$ remain incomplete (`SEARCH_FAILED`). These are focused results, **not** a substitute for the phase-end active full suite.

The canonical public route remains source-first typed Backward Search, verified Proof Tree, one `ProofNarrativeModel`, one common Renderer, and Web. Search stops at its first successful proof and does not perform a proof-uniqueness search. Display-only EHP implications are not independent ProofSteps. No dedicated narrative for an individual $(n,k)$ or generator has been added.

R73 prepares complete versions of this README and the four canonical Japanese documents, preserving previous phase records. It changes no production code, adds no new mathematics, and does not close Phase 174. The final phase-end gate belongs to the following step.

---



## `updates/design.md`（追記・挿入する新節の全文）

<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## Phase 174 R73 — 共通証明経路と Closeout 前の設計境界（2026-11-11）

Phase 174 は **R73 時点では正式終了していない**。R71・R72 の限定 Gate は通過したが、Phase 末尾の現行アクティブ `tests/` 全体 pytest と最終 Git・文書整合確認は未実施である。R73 は全文文書を整備する工程であり、新しい数学的証明を追加する工程ではない。

### 現在有効な公開経路

```text
出典付きの型付き Goal
→ Source-first Backward Search（出典優先の逆向き探索）
→ Verified Proof Tree（検証済み証明木）
→ 単一 ProofNarrativeModel（証明文章モデル）
→ 共通 Narrative Renderer（文章表示器）
→ Web Group proof
```

探索は First Successful Proof Search（最初に成功した証明で終了）であり、唯一性検査を実施しない。`GIVEN`（文献・先行結果の採用）と `INFERENCE`（一般規則による導出）の責務を分ける。特定の群・生成元・次元専用の Narrative（文章分岐）や、結論を直接 GIVEN とする登録は導入しない。

### R70／R70R1 の表示限定性

`phase174_r3_r7_r70_verified_narrative_projection/projection.py` は、完成した証明木の根の祖先内にある型付き ProofStep と Citation の対応を要求し、合成像・結合法則・零像、Δ 全射性、EHP 完全性による説明を共通の表示へ投影する。R70R1 は associativity（結合法則）による一段の型付き証明連鎖をたどる条件を補正した。不一致・欠落・曖昧な場合には表示変換を実行しない fail-closed（検証不能なら変換しない）方式を維持する。

`E=0` と `H の単射性` の説明は、既に検証された四前提の零群一般推論規則の論理的帰結を文章にしたものであり、新たな独立 ProofStep として数えてはならない。`ProofSearchStatus`、`conclusion`、`open_goals`、`diagnostics`、証明木と引用数は Renderer が変更しない。

### 公開回帰の境界

R71 は完成8群の実探索と共通表示・引用数を監査し、限定 pytest 81 PASS。R72 はその保存レポートを確認し、未完成の $\pi_{12}^{4}$ と $\pi_{35}^{4}$ が `SEARCH_FAILED` のまま共通 Renderer／Web で表示されることを確認し、限定 pytest 38 PASS。R72 までの本番コード変更、新規 GIVEN、新規数学推論規則はいずれも 0 件。

これは登録されたすべての数学的文章の意味を個別に証明したという認定ではない。文献転記全件の正しさ、任意の $(n,k)$ の証明完成、ブラウザにおける全数式の画素単位の表示確認も未認定である。正式 Closeout は次の最終 Gate で判定する。



## `updates/development_log.md`（追記・挿入する新節の全文）

<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## 2026-11-11 — Phase 174 R56〜R73：一般推論、共通表示、限定回帰、文書準備（正式終了前）

本節は Phase 174 終了前の追記記録であり、Phase 173 の正式終了記録を上書きしない。Phase 末尾の全体 pytest は未実施であり、**Phase 174 はまだ正式終了していない**。

- **R56〜R57：** 検証済みの Hopf 単射性・像・生成元の情報から自由巡回構造を決定する一般規則、および生成元の $\Delta$ 像が群を生成するときの全射性一般規則を分離。共通 Renderer と既存 ProofStep の責務を整理した。後続の零群証明では先行データベース結果を再実行せずに採用する。
- **R63〜R66：** 主要証明文章の出典・ProofStep 対応を段階的に監査。文章全件の数学的意味の完全な認証とは区別する。
- **R67〜R69：** 零写像の TeX 矢印を修正。Hopf 単射性の直接2前提と零群結論の直接4前提を照合。既存 ProofStep による Narrative 統合可能範囲を監査。
- **R70〜R70R1：** 型付き合成像・結合法則・零像の連鎖をまとめ、$\Delta$ 全射性から $E=0$ と $H$ 単射性への説明を共通表示へ統合。R70R1 は結合法則連鎖の表示条件を修正。限定 pytest **59 PASS**、2群の実際の Web 表示を確認。Reference は $\pi_{11}^{6}$ が7件、$\pi_{12}^{7}$ が3件。新規 GIVEN・新規数学推論規則はともに0件。
- **R71：** 完成8群（$\pi_6^3$, $\pi_7^4$, $\pi_8^4$, $\pi_9^4$, $\pi_{11}^4$, $\pi_8^5$, $\pi_{11}^6$, $\pi_{12}^7$）を対象に共通 Narrative の限定回帰監査。引用件数は順に 8, 4, 4, 4, 4, 7, 7, 3 件。限定 pytest **81 PASS**、`PASS_R71_FOCUSED_AND_CROSS_GROUP`、本番コード変更0件。
- **R72：** R71 保存証拠8群を確認。記名生成元 Goal の未完成例 $\pi_{12}^{4}$ および $\pi_{35}^{4}$ がともに `SEARCH_FAILED` のまま維持されることを実探索・Web 表示で確認。限定 pytest **38 PASS**、Source Guard 10件、`PASS_R72_FOCUSED_AND_PREFLIGHT`、本番コード変更0件。主要5文書に Phase 174 の最終記録が未掲載であることを識別。
- **R73：** 主要5文書の全文出力を行う準備工程。既存本文を保存し、現在状態・設計・履歴・計画・証明記録を追記する。正式終了認定は Phase 末尾の全体 pytest と最終監査を通過した後に行う。

R71・R72 の pytest はそれぞれ限定テストであり、合算しても全体テストではない。Git HEAD は R71 実行時 `01c5246a011b43e10ed85699a6048f117562a748`、R72 実行時 `b66099598177d74e979492f1d04a916e6f0821a8`。実行結果と Git 履歴の時点差を保持する。Git の更新に伴う検査を行わずに新しい HEAD のテスト成功を遡及的に主張しない。

**次の Gate：** Phase 174 最後の現行アクティブ `tests/` 全体 pytest を1回実行し、既存の完成・未完成境界、出典、文書全文、Git 差分を再監査する。その結果が PASS するまでは Phase 174 正式終了を宣言しない。



## `updates/proof_records.md`（追記・挿入する新節の全文）

<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## 2026-11-11 — Phase 174 R71〜R73：2つの完成証明と未完成境界（終了前の追記）

本節は検証済み Proof Tree（証明木）／出典付き一般規則に基づく公開証明の記録である。Phase 174 の最終全体 pytest と正式終了はまだ行っていない。Phase 173 における過去の未完成記録は当時の事実として保存する。

### $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$

使用した出典は Reference 7件。Toda (5.9) の一般的な零合成と懸垂の合成保存性、検証済み結合法則連鎖から、次を公開表示する。

$$
\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\},\qquad
E(\nu_5\eta_8^2)=\nu_6\eta_9^2=0.
$$

したがって $E:\pi_{10}^{5}\to\pi_{11}^{6}$ は零写像、完全性より $H:\pi_{11}^{6}\to\pi_{11}^{11}$ は単射。さらに引用済みの生成元像から

$$
\ker(\Delta:\pi_{11}^{11}\to\pi_9^5)=\mathbb Z\{2\iota_{11}\},
\qquad H(\Delta(\iota_{13}))=\pm2\iota_{11}.
$$

これにより $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ を得る。この一般推論による結論は `generic-complete-proof` である。

### $\pi_{12}^{7}=0$

Reference 3件。順序づけられた先行データベース結果 $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ を利用する。ここで先行群を再証明しない。生成元から、$\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$ は全射である。EHP 完全性より

$$
\operatorname{Im}\Delta=\ker E=\pi_{11}^{6},\qquad
\ker H=\operatorname{Im}E=0.
$$

よって $H:\pi_{12}^{7}\to\pi_{12}^{13}$ は単射。$\pi_{12}^{13}=0$ から $\pi_{12}^{7}=0$ を得る。これも `generic-complete-proof` である。$E=0$ と $H$ の単射性の文章は、4前提の既存零群一般規則に基づく説明であって、新規の独立 ProofStep ではない。

### 回帰監査と認定範囲

R70R1 は限定 pytest 59 PASS と両群の Web 表示を確認。R71 は完成8群の限定 pytest 81 PASS（Reference 件数：8、4、4、4、4、7、7、3）。R72 は限定 pytest 38 PASS と先行監査記録の照合、および $\pi_{12}^{4}$、$\pi_{35}^{4}$ の記名生成元 Goal が `SEARCH_FAILED` のまま公開されることを確認した。R71・R72 で新規 GIVEN、数学推論規則、本番コード変更はいずれも0件。

これらは特定の検証済み証明木と公開経路の監査であり、文献の全命題、すべてのホモトピー群、あるいはすべての証明文章の数学的意味を独立に検証したことを意味しない。全体 pytest の結果は次の正式 Closeout Gate に記録する。



## `updates/roadmap.md`（追記・挿入する新節の全文）

<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## Phase 174 R73 — 正式終了前の現在地と次の依存関係（2026-11-11）

**現在地：** R71 の完成8群回帰（限定 pytest 81 PASS）と R72 の文書・未完成境界監査（限定 pytest 38 PASS）を通過した。Phase 174 はなお終了前である。過去節で将来候補・未実装とされた Phase 172／173 の作業はその記録時点の状態であり、最新の状況は Phase 171〜173 の正式終了と、本節の Phase 174 終了準備を参照する。

**現在の証明済み範囲：** $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ は一般推論規則による完成証明、$\pi_{12}^{7}=0$ は先行データベース結果から一般規則を用いる完成証明。いずれも `generic-complete-proof`。R71 はこの2群を含む完成8群を監査した。$\pi_8^5$ は Phase 173 の歴史的未完成状態から Phase 174 で完成に進展した。一方、$\pi_{12}^4$ と $\pi_{35}^4$ の記名生成元 Goal は R72 時点で未完成である。

**R73：** 現行 Git と R72 レポートの Source Guard に基づいて主要5文書の**全文版**を作成・確認・適用する。文書の英日区分と過去の開発記録を維持する。数学的な GIVEN、推論規則、Renderer、本番 API を変更しない。限定 pytest のみ行い、Phase を終了したとは記載しない。

**R73 の後の最終 Gate（次工程）：** (1) 本番・文書差分の確認、(2) R71/R72 の監査証拠と未完成範囲の再確認、(3) **Phase 末尾の現行アクティブ `tests/` 全体 pytest を1回のみ**実行、(4) 結果と HEAD を記録して正式 Closeout 可否を決定する。失敗時は失敗記録を保全し、原因を監査する。未実行の全体テストを PASS と記載しない。

**次 Phase との境界：** 任意の群への拡大、未完成記名生成元の新規数学証明、文献全件の独立検証、個別 Narrative 追加は本 Phase の Closeout に含めない。次 Phase の機能と Goal は終了 Gate の後に選定する。

