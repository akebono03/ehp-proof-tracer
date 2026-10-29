"""Phase 170 R3-R12 focused tests; never import application mathematics."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

from phase170_r3_r12_document_closeout import update_docs as d


def source_bytes(relative: str) -> bytes:
    if relative == "README.md":
        return (
            "# EHP Proof Tracer\n\n" + d.README_INSERT_BEFORE
            + "\n\n## Phase 169 historical section\n"
        ).encode("utf-8")
    return ("# 既存記録\n\n歴史を保持する。\n" + relative + "\n").encode("utf-8")


@pytest.mark.parametrize("relative", tuple(d.DOC_BLOBS))
def test_full_output_preserves_historical_text(relative: str) -> None:
    original = source_bytes(relative)
    changed = d.append_section(original, relative)
    assert changed != original
    assert changed.count(d.MARKER.encode("ascii")) == 1
    if relative == "README.md":
        assert changed.index(d.MARKER.encode("ascii")) < changed.index(b"PHASE169_FINAL_CLOSEOUT")
        assert changed.endswith(b"## Phase 169 historical section\n")
    else:
        assert changed.startswith(original)
        assert changed.count(original) == 1


@pytest.mark.parametrize("relative", tuple(d.DOC_BLOBS))
def test_duplicate_document_phase_marker_is_refused(relative: str) -> None:
    created = d.append_section(source_bytes(relative), relative)
    with pytest.raises(RuntimeError, match="already exists"):
        d.append_section(created, relative)


def test_bom_and_crlf_preserved() -> None:
    original = b"\xef\xbb\xbf" + ("# 履歴\r\n\r\n旧行\r\n".encode("utf-8"))
    changed = d.append_section(original, "docs/design.md")
    assert changed.startswith(original)
    assert b"\r\n<!-- PHASE170_FINAL" in changed
    assert b"\r\n\r\n## Phase 170" in changed


def fake_row(k: int) -> dict:
    return {
        "k": k, "n": 2, "group_dimension": k + 2,
        "target_typed": True, "source_precedes": True,
        "search_status": "complete", "search_complete": True,
        "open_goals": 0, "proven_steps": 4,
        "result": "COMPLETE_AND_WEB_VERIFIED",
        "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 3, "web_error": None,
    }


def fake_evidence(tmp_path: Path) -> tuple[dict, dict, Path]:
    domain = {
        "phase": "170 R3-R10", "mode": "AUDIT_ONLY_FRESH_33",
        "dry_run": False, "result": "DOMAIN_ALL_VERIFIED",
        "domain": list(range(1, 34)), "domain_checked": 33,
        "domain_complete": 33, "domain_gaps": 0,
        "tracked_unchanged": True,
        "preflight": {"head": d.AUDITED_HEAD},
        "rows": [fake_row(k) for k in range(1, 34)],
    }
    domain_path = tmp_path / "audit.json"
    domain_path.write_text(json.dumps(domain), encoding="utf-8")
    closeout = {
        "phase": "170 R3-R11", "mode": "PHASE_END_ACTIVE_SUITE",
        "dry_run": False, "full_pytest": True,
        "pytest_exit": 0, "result": "FULL_SUITE_PASS",
        "tracked_unchanged": True,
        "domain_checked": 33, "domain_complete": 33, "domain_gaps": 0,
        "domain_report_sha256": sha256(domain_path.read_bytes()).hexdigest(),
        "preflight": {"head": d.EXPECTED_HEAD},
        "pytest_summary": "3546 passed in 34.94s",
        "active_command": ["python", "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "tests"],
    }
    return domain, closeout, domain_path


def test_successful_previous_reports_are_accepted(tmp_path: Path) -> None:
    domain, closeout, path = fake_evidence(tmp_path)
    d.validate_evidence(domain, closeout, path)


@pytest.mark.parametrize("field,value", [
    ("domain_complete", 32),
    ("domain_gaps", 1),
    ("result", "DOMAIN_GAPS_FOUND"),
    ("tracked_unchanged", False),
])
def test_incomplete_domain_evidence_refused(tmp_path: Path, field: str, value: object) -> None:
    domain, closeout, path = fake_evidence(tmp_path)
    domain[field] = value
    with pytest.raises(RuntimeError, match="fresh-domain"):
        d.validate_evidence(domain, closeout, path)


def test_one_forged_worker_is_refused(tmp_path: Path) -> None:
    domain, closeout, path = fake_evidence(tmp_path)
    domain["rows"][11]["web_partial"] = True
    with pytest.raises(RuntimeError, match="worker evidence incomplete"):
        d.validate_evidence(domain, closeout, path)


@pytest.mark.parametrize("field,value", [
    ("pytest_exit", 1),
    ("result", "FULL_SUITE_FAILED"),
    ("pytest_summary", "3545 passed in 34.94s"),
    ("tracked_unchanged", False),
])
def test_forged_or_failed_closeout_refused(tmp_path: Path, field: str, value: object) -> None:
    domain, closeout, path = fake_evidence(tmp_path)
    closeout[field] = value
    with pytest.raises(RuntimeError):
        d.validate_evidence(domain, closeout, path)


def test_readme_english_and_other_sections_japanese() -> None:
    assert "Current status — Phase 170" in d.README_SECTION
    for relative in ("docs/design.md", "docs/development_log.md", "docs/roadmap.md", "docs/proof_records.md"):
        section = d.SECTIONS[relative]
        assert "Phase 170" in section
        assert "監査" in section
        assert "3546" in section or "3,546" in section


def test_expected_five_reviewed_docs() -> None:
    assert set(d.DOC_BLOBS) == {
        "README.md", "docs/design.md", "docs/development_log.md",
        "docs/roadmap.md", "docs/proof_records.md",
    }
    assert len(set(d.DOC_BLOBS.values())) == 5


def preflight_answers(head: str = "new-commit") -> dict:
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): head,
        ("merge-base", "--is-ancestor", d.GATE_HEAD, "HEAD"): "",
        ("-c", "core.quotePath=false", "diff", "--name-status", d.GATE_HEAD, "HEAD", "--"):
            "A\tphase170_r3_r11r2_unicode_git_path_fix/監査仕様.md",
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for relative, sha in d.DOC_BLOBS.items():
        answers[("rev-parse", f"HEAD:{relative}")] = sha
    return answers


def test_preflight_accepts_additions_only_in_reviewed_audit_paths(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    answers = preflight_answers()
    for path in d.DOC_BLOBS:
        file = tmp_path / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
    monkeypatch.setattr(d, "git", lambda root, *args: answers[args])
    report = d.preflight(tmp_path, check_remote=False)
    assert report["gate_head"] == d.GATE_HEAD
    assert report["head"] == "new-commit"


@pytest.mark.parametrize("delta", [
    "M\tphase170_r3_r11r2_unicode_git_path_fix/監査仕様.md",
    "A\tsources/toda/Toda_07_2.tex",
    "A     \"phase170_r3_r11r2_unicode_git_path_fix/\\347\\233\\243.md\"",
])
def test_preflight_rejects_non_audit_changes(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, delta: str) -> None:
    answers = preflight_answers()
    answers[("-c", "core.quotePath=false", "diff", "--name-status", d.GATE_HEAD, "HEAD", "--")] = delta
    monkeypatch.setattr(d, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="non-audit change"):
        d.preflight(tmp_path, check_remote=False)


def test_preflight_refuses_existing_changes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    answers = preflight_answers()
    answers[("diff", "--name-only", "HEAD", "--")] = "README.md"
    monkeypatch.setattr(d, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="pre-existing tracked changes"):
        d.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_wrong_branch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    answers = preflight_answers()
    answers[("branch", "--show-current")] = "main"
    monkeypatch.setattr(d, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="unreviewed branch"):
        d.preflight(tmp_path, check_remote=False)


def test_full_document_output_dry_run_and_apply_on_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "repo"
    for relative in d.DOC_BLOBS:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source_bytes(relative))
    domain, closeout, domain_path = fake_evidence(tmp_path)
    monkeypatch.setattr(d, "preflight", lambda root, **kwargs: {"head": d.EXPECTED_HEAD})
    monkeypatch.setattr(d, "load_evidence", lambda recovery: (domain_path, domain_path, domain, closeout))
    def mock_git(root: Path, *args: str) -> str:
        if args == ("diff", "--cached", "--name-only", "--"):
            return ""
        if args == ("diff", "--name-only", "HEAD", "--"):
            return "\n".join(d.DOC_BLOBS)
        raise AssertionError(args)
    monkeypatch.setattr(d, "git", mock_git)
    output = tmp_path / "output"
    report = d.build_docs(root, output, tmp_path, apply=False)
    assert report["result"] == "FIVE_FULL_DOCUMENTS_PREPARED"
    assert all((root / rel).read_bytes() == source_bytes(rel) for rel in d.DOC_BLOBS)
    assert all((output / rel).is_file() for rel in d.DOC_BLOBS)
    applied = d.build_docs(root, output, tmp_path, apply=True)
    assert applied["result"] == "FIVE_DOCUMENTS_APPLIED"
    assert all((root / rel).read_bytes() == (output / rel).read_bytes() for rel in d.DOC_BLOBS)
    assert all((Path(applied["backup_root"]) / "before" / rel).read_bytes() == source_bytes(rel) for rel in d.DOC_BLOBS)
