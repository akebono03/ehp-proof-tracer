"""Tests for source parsing, typed mismatch evidence and the Git safety boundary."""
from __future__ import annotations

from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2b_prop56_source_dependency_audit import audit


def example_cases() -> list[dict]:
    cases = []
    for n, key in audit.CASES:
        cases.append({
            "n": n, "k": 3, "key": key,
            "goal_count": 1, "exact_equal": False,
            "differences": [{"path": "goal.rhs.generator.name", "kind": "value"}],
            "source_assertions": [{
                "assertion_id": "shared:0:boundary:Proposition 5.6:" + key,
                "origin": "fixed_statement", "proof_link_count": 0,
                "linked_step_count": 0,
            }],
        })
    return cases


def example_alignment() -> dict:
    return {
        "phase": "171 R2A", "mode": "READ_ONLY_TYPED_ALIGNMENT",
        "read_only": True, "source_head": audit.BASELINE,
        "cases": example_cases(),
    }


def example_source() -> str:
    return (
        "Header\n"
        r"\begin{proposition}\label{prop:5.6}" + "\n"
        r"\(\pi^{3}_{6}=\gen{\nu'}\cong \mathbb Z_{4}\)" + "\n"
        r"\(\pi^{4}_{7}=\gen{\nu_{4}}\oplus\gen{E\nu'}\)" + "\n"
        r"\(\pi^{n}_{n+3}=\gen{\nu_{n}}\cong\mathbb Z_8 (n\ge5)\)" + "\n"
        r"\end{proposition}" + "\n"
        r"\textbf{Proof.} (5.2), Prop 5.3, (4.4), (5.6)? "
        r"(4.8), (5.5), (4.5) \qed" + "\n"
        r"\paragraph*{iv). The next section}" + "\n"
    )


def test_validate_alignment_accepts_three_exact_gaps():
    cases = audit.validate_alignment(example_alignment())
    assert tuple(item["n"] for item in cases) == (3, 4, 5)


def test_validate_alignment_rejects_wrong_phase():
    report = example_alignment()
    report["phase"] = "171 R1D"
    with pytest.raises(ValueError, match="R2A"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_unverified_scope():
    report = example_alignment()
    report["read_only"] = False
    with pytest.raises(ValueError, match="read-only"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_wrong_source_head():
    report = example_alignment()
    report["source_head"] = "wrong"
    with pytest.raises(ValueError, match="commit"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_extra_case():
    report = example_alignment()
    report["cases"].append(dict(report["cases"][0]))
    with pytest.raises(ValueError, match="exactly three"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_proof_link():
    report = example_alignment()
    report["cases"][1]["source_assertions"][0]["proof_link_count"] = 1
    with pytest.raises(ValueError, match="proof-link"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_false_claim_of_equal_types():
    report = example_alignment()
    report["cases"][0]["exact_equal"] = True
    with pytest.raises(ValueError, match="already aligned"):
        audit.validate_alignment(report)


def test_source_sections_extracts_original_proposition_and_proof():
    result = audit.source_sections(example_source())
    assert r"\pi^{3}_{6}" in result["theorem"]
    assert r"\textbf{Proof.}" in result["proof"]
    assert result["theorem_start_line"] == 2
    assert result["has_question_marker"] is True
    assert "(5.2)" in result["references_in_proof"]
    assert "(4.5)" in result["references_in_proof"]


def test_source_sections_rejects_missing_proposition():
    with pytest.raises(ValueError, match="uniquely"):
        audit.source_sections("no proposition")


def test_source_sections_rejects_duplicate_proposition():
    with pytest.raises(ValueError, match="uniquely"):
        audit.source_sections(example_source() + example_source())


def test_source_sections_rejects_missing_theorem_marker():
    source = example_source().replace(r"\gen{\nu_{4}}", r"\gen{x}")
    with pytest.raises(ValueError, match="n=4"):
        audit.source_sections(source)


def test_source_sections_rejects_proof_without_qed():
    source = example_source().replace(r"\qed", "not yet")
    with pytest.raises(ValueError, match="incomplete"):
        audit.source_sections(source)


def test_source_sections_rejects_missing_next_section():
    source = example_source().replace(r"\paragraph*{iv).", "No section")
    with pytest.raises(ValueError, match="boundary"):
        audit.source_sections(source)


def test_classification_does_not_normalize_discrepant_symbols():
    case = example_cases()[0]
    case["differences"] = [
        {"path": "goal.rhs.generator.name", "kind": "value"},
        {"path": "goal.rhs.generator.source", "kind": "type"},
        {"path": "goal.rhs.generator.generator.family", "kind": "value"},
    ]
    item = audit.classify_case(case, audit.source_sections(example_source()))
    assert item["typed_difference_kinds"] == [
        "GENERATOR_DISPLAY_NAME", "GENERATOR_DOMAIN_CODOMAIN",
        "GENERATOR_SYMBOL_IDENTITY",
    ]
    assert item["blockers"] == ("TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK")
    assert item["proof_link_count"] == 0


def test_classification_detects_iterated_suspension_type():
    case = example_cases()[1]
    case["differences"] = [{"path": "goal.rhs.summands[1].generator", "kind": "type"}]
    item = audit.classify_case(case, audit.source_sections(example_source()))
    assert item["typed_difference_kinds"] == ["GENERATOR_EXPRESSION_TYPE"]


def test_markdown_includes_original_text_and_boundary():
    source = audit.source_sections(example_source())
    items = [audit.classify_case(x, source) for x in example_cases()]
    output = audit.markdown_report({"cases": items, "source": source})
    assert "π_6^3" in output
    assert "π_7^4" in output
    assert "π_8^5" in output
    assert r"\begin{proposition}" in output
    assert "GIVEN" in output


def test_git_guard_allows_only_reviewed_paths(monkeypatch, tmp_path):
    expected = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "commit",
        ("rev-parse", "--verify", "refs/remotes/origin/develop"): "commit",
        ("status", "--porcelain", "--untracked-files=no"): "",
        ("merge-base", "--is-ancestor", audit.BASELINE, "HEAD"): "",
        ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"): "",
        ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"): "phase171_r1d_k3_three_gap_diagnostics/triage.py\0",
        ("diff", "--name-only", "-z", "refs/remotes/origin/develop", "HEAD"): "",
    }
    for path, blob in audit.EXPECTED_BLOBS.items():
        expected[("rev-parse", "HEAD:" + path)] = blob
    monkeypatch.setattr(audit, "git", lambda root, *args: expected[args])
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=b""))
    result = audit.tracked_state(tmp_path)
    assert result["head"] == "commit"
    assert result["reviewed_changes"] == ("phase171_r1d_k3_three_gap_diagnostics/triage.py",)


def test_git_guard_rejects_changed_production(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return ""
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase165_r52_r9_shared_math.py\0"
        return "commit"
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="unreviewed committed files"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_diverged_upstream(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "local"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "remote"
        if args == ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"):
            raise RuntimeError("git reports remote not ancestor")
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_tracked_working_diff(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "commit"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "commit"
        return " M phase165_r52_r9_shared_math.py"
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="not clean"):
        audit.tracked_state(tmp_path)




def setup_temporary_git_repository(monkeypatch, tmp_path):
    """Build an isolated fixture with a tracking ref, not an application checkout."""
    def command(*arguments):
        finished = subprocess.run(
            ["git", *arguments], cwd=tmp_path, capture_output=True,
            text=True, check=True,
        )
        return finished.stdout.strip()

    command("init", "-q")
    command("config", "user.name", "Audit Test")
    command("config", "user.email", "audit@example.invalid")
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.parent.mkdir(parents=True)
    source.write_text("reviewed source fixture\n", encoding="utf-8")
    command("add", "--", "sources/toda/Toda_05_2.tex")
    command("commit", "-q", "-m", "baseline")
    command("branch", "-M", "develop")
    base = command("rev-parse", "HEAD")
    command("update-ref", "refs/remotes/origin/develop", base)
    blob = command("rev-parse", "HEAD:sources/toda/Toda_05_2.tex")
    monkeypatch.setattr(audit, "BASELINE", base)
    monkeypatch.setattr(
        audit, "EXPECTED_BLOBS", {"sources/toda/Toda_05_2.tex": blob}
    )
    return command, base


def test_git_guard_accepts_audit_only_local_ahead_commit(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md")
    command("commit", "-q", "-m", "local audit only")
    assert command("rev-parse", "HEAD") != remote
    state = audit.tracked_state(tmp_path)
    assert state["origin_develop"] == remote
    assert state["head"] == command("rev-parse", "HEAD")
    assert state["local_ahead_audit_changes"] == (
        "phase171_r2a_prop56_alignment_audit/README.md",
    )


def test_git_guard_rejects_ahead_unreviewed_source_commit(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.write_text("unreviewed source edit\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md", "sources/toda/Toda_05_2.tex")
    command("commit", "-q", "-m", "not audit only")
    assert command("rev-parse", "HEAD") != remote
    with pytest.raises(RuntimeError, match="unreviewed committed files"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_remote_ahead_of_local(monkeypatch, tmp_path):
    command, base = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r1d_k3_three_gap_diagnostics"
    package.mkdir()
    (package / "README.md").write_text("remote audit\n", encoding="utf-8")
    command("add", "--", "phase171_r1d_k3_three_gap_diagnostics/README.md")
    command("commit", "-q", "-m", "remote audited commit")
    remote = command("rev-parse", "HEAD")
    command("update-ref", "refs/remotes/origin/develop", remote)
    command("reset", "--hard", base)
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_ahead_commit_with_wrong_pinned_blob(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md")
    command("commit", "-q", "-m", "local audit only")
    assert command("rev-parse", "HEAD") != remote
    monkeypatch.setattr(
        audit, "EXPECTED_BLOBS", {"sources/toda/Toda_05_2.tex": "different"}
    )
    with pytest.raises(RuntimeError, match="source blob has changed"):
        audit.tracked_state(tmp_path)

def test_run_script_uses_python_module_launch():
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "phase171_r2b_prop56_source_dependency_audit.audit" in script
    assert "'--root'" in script
    assert "-m" in script


def test_blob_pin_covers_source_tex():
    assert "sources/toda/Toda_05_2.tex" in audit.EXPECTED_BLOBS
    assert "phase165_r52_r9_shared_math.py" in audit.EXPECTED_BLOBS
