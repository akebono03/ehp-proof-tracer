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
