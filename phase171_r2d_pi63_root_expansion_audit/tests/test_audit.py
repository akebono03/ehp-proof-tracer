"""Focused tests for the pi_6^3 read-only root-expansion audit."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from phase171_r2d_pi63_root_expansion_audit import audit


class Rule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


def saved_r2c() -> dict:
    return {
        "phase": "171 R2C",
        "read_only": True,
        "tracked_unchanged": True,
        "pi63": {
            "target": "pi_6^3", "typed_equal": False,
            "candidate_link_count": 0,
            "toda53_hopf_link_count": 1,
        },
    }


def fake_bridge():
    records = (
        ("p42", "Proposition 4.2 (4.4)", ("EHP", "schema")),
        ("h53", "(5.3)", ("H(nu')", "eta5")),
        ("p56", "Proposition 5.6", ("pi63", "Z4")),
    )
    refs = {}
    assertions = {}
    links = []
    for id_, locator, content in records:
        refs[id_] = SimpleNamespace(locator=locator)
        assertions[id_] = SimpleNamespace(
            assertion_id=id_, reference_id=id_, content=content,
        )
        if id_ != "p56":
            links.append(SimpleNamespace(
                assertion_id=id_,
                step=SimpleNamespace(
                    rule=Rule.GIVEN, premises=(), conclusion=content,
                ),
            ))
    registry = SimpleNamespace(
        _assertions=assertions,
        reference=lambda id_: refs[id_],
    )
    complete = SimpleNamespace(registry=registry)
    screened = SimpleNamespace(proof_links=tuple(links))
    return complete, screened


def fake_expansion(name="exactness rule", children=("EHP", "H(nu')")):
    return SimpleNamespace(
        rule=SimpleNamespace(name=name), subgoals=tuple(children),
    )


def test_saved_r2c_accepted():
    assert audit.validate_r2c(saved_r2c())["target"] == "pi_6^3"


@pytest.mark.parametrize("wrong", [None, [], "str", 123])
def test_saved_r2c_rejects_invalid_payload(wrong):
    with pytest.raises(ValueError, match="R2C"):
        audit.validate_r2c(wrong)


def test_saved_r2c_rejects_wrong_phase():
    payload = saved_r2c()
    payload["phase"] = "171 R2B"
    with pytest.raises(ValueError, match="R2C"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_missing_readonly():
    payload = saved_r2c()
    payload["read_only"] = False
    with pytest.raises(ValueError, match="read-only"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_tracked_modifications():
    payload = saved_r2c()
    payload["tracked_unchanged"] = False
    with pytest.raises(ValueError, match="tracked"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_wrong_target():
    payload = saved_r2c()
    payload["pi63"]["target"] = "pi_7^4"
    with pytest.raises(ValueError, match="pi_6"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_unexpected_existing_link():
    payload = saved_r2c()
    payload["pi63"]["candidate_link_count"] = 1
    with pytest.raises(ValueError, match="state differs"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_hopf_missing():
    payload = saved_r2c()
    payload["pi63"]["toda53_hopf_link_count"] = 0
    with pytest.raises(ValueError, match="Hopf"):
        audit.validate_r2c(payload)


def test_locator_alias_is_separate_from_exact_4_4():
    complete, screened = fake_bridge()
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 1
    assert results["(4.4)"]["registered_assertions"] == 0


def test_given_hopf_is_counted_but_target_candidate_is_not():
    complete, screened = fake_bridge()
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["(5.3)"]["screened_given_links"] == 1
    assert results["Proposition 5.6"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_conclusion_mismatches():
    complete, screened = fake_bridge()
    screened.proof_links[1].step.conclusion = ("wrong", "data")
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["(5.3)"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_rule_is_inference():
    complete, screened = fake_bridge()
    screened.proof_links[0].step.rule = Rule.INFERENCE
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_premises_nonempty():
    complete, screened = fake_bridge()
    screened.proof_links[0].step.premises = ("fake",)
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 0


def test_no_root_expansions_is_not_a_proof():
    _, screened = fake_bridge()
    frontier = audit.root_expansion_inventory("goal", lambda goal: (), screened)
    assert frontier["root_expansions"] == 0
    assert frontier["root_is_verified_proof"] is False


def test_root_expansion_counts_distinct_rules():
    _, screened = fake_bridge()
    expansions = (
        fake_expansion(), fake_expansion(),
        fake_expansion("cyclic relation", ("H(nu')",)),
    )
    frontier = audit.root_expansion_inventory("goal", lambda goal: expansions, screened)
    assert frontier["root_expansions"] == 3
    assert frontier["rule_counts"] == {
        "cyclic relation": 1, "exactness rule": 2,
    }
    assert len(frontier["preview"]) == 3
    assert frontier["root_is_verified_proof"] is False


def test_expansion_subgoals_count_screened_evidence_only():
    _, screened = fake_bridge()
    candidates = (fake_expansion(children=(("H(nu')", "eta5"), ("unknown",))),)
    frontier = audit.root_expansion_inventory("goal", lambda goal: candidates, screened)
    subgoals = frontier["preview"][0]["subgoals"]
    assert subgoals[0]["screened_exact_step_count"] == 1
    assert subgoals[1]["screened_exact_step_count"] == 0


def test_provider_must_be_callable():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="callable"):
        audit.root_expansion_inventory("goal", object(), screened)


def test_provider_must_return_tuple():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="tuple"):
        audit.root_expansion_inventory("goal", lambda goal: [], screened)


def test_provider_rejects_invalid_expansion():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="typed"):
        audit.root_expansion_inventory("goal", lambda goal: (object(),), screened)


def test_truncated_expansion_preview():
    _, screened = fake_bridge()
    options = tuple(fake_expansion() for _ in range(audit.MAX_PREVIEW + 1))
    result = audit.root_expansion_inventory("goal", lambda goal: options, screened)
    assert result["root_expansions"] == audit.MAX_PREVIEW + 1
    assert result["preview_count"] == audit.MAX_PREVIEW
    assert result["truncated_expansions"] is True


def test_markdown_warns_proposals_are_not_proofs():
    _, screened = fake_bridge()
    payload = {
        "screened_sources": [{"locator": "(5.3)", "registered_assertions": 1,
                              "screened_given_links": 1}],
        "frontier": audit.root_expansion_inventory("goal", lambda goal: (), screened),
        "citing_assertion_id": None,
        "screened_link_total": 1,
    }
    result = audit.markdown_report(payload)
    assert "ProofStep" in result
    assert "Proposition 5.6" in result
    assert "(5.6)?" in result


def test_git_guard_blocks_unknown_committed_file(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args[:3] == ("diff", "--name-only", "-z"):
            return "phase165_r52_r9_shared_math.py"
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.BASELINE
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return audit.BASELINE
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="unreviewed committed"):
        audit.tracked_state(tmp_path)


def test_git_guard_blocks_modified_tracked(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.BASELINE
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return audit.BASELINE
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return " M proof.py"
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="tracked"):
        audit.tracked_state(tmp_path)


def test_cli_imports_as_module_from_repository_root():
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-B", "-m", "phase171_r2d_pi63_root_expansion_audit.audit", "--help"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--report" in result.stdout


def test_dry_run_does_not_import_proof_engine(monkeypatch, tmp_path, capsys):
    report = tmp_path / "frontier.json"
    report.write_text(json.dumps(saved_r2c()), encoding="utf-8")
    state = {"head": audit.BASELINE, "diff": "clean"}
    monkeypatch.setattr(audit, "tracked_state", lambda root: state.copy())
    result = audit.run(tmp_path, report, dry_run=True)
    assert result == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2D_DRY_RUN=PASS" in output
    assert "PHASE171_R2D_TRACKED_UNCHANGED=True" in output
