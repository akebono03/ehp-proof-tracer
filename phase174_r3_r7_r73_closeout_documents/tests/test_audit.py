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
