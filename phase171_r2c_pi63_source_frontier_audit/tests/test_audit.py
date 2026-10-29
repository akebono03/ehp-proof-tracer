"""Focused R2C source-frontier and trust-boundary regression tests."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2c_pi63_source_frontier_audit import audit


class Origin(Enum):
    FIXED_STATEMENT = "fixed_statement"


class Rule(Enum):
    GIVEN = "given"


def example_r2b() -> dict:
    return {
        "phase": "171 R2B", "read_only": True,
        "cases": [{
            "n": n, "proof_link_count": 0,
            "blockers": ["TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK"],
        } for n in (3, 4, 5)],
        "source": {"has_question_marker": True,
                   "references_in_proof": ["(5.3)", "(5.6)"]},
    }


def fake_registry():
    hopf = SimpleNamespace(
        assertion_id="shared:9:toda:adopted:eq5.3:nu_prime_hopf_relation",
        reference_id="h", content=("H(nu')", "eta5"),
        origin=Origin.FIXED_STATEMENT, scope=None,
    )
    proposition = SimpleNamespace(
        assertion_id="shared:0:boundary:Proposition 5.6:pi6_3_group_relation",
        reference_id="p", content=("pi63", "Z4:literature"),
        origin=Origin.FIXED_STATEMENT, scope=None,
    )
    match_step = SimpleNamespace(rule=Rule.GIVEN, conclusion=hopf.content)
    link = SimpleNamespace(assertion_id=hopf.assertion_id, step=match_step)
    entries = {"h": SimpleNamespace(locator="(5.3)"),
               "p": SimpleNamespace(locator="Proposition 5.6")}
    registry = SimpleNamespace(
        _assertions={hopf.assertion_id: hopf, proposition.assertion_id: proposition},
        reference=lambda key: entries[key],
    )
    bridge = SimpleNamespace(registry=registry, proof_links=(link,))
    return bridge


def test_r2b_accepts_expected_scope():
    assert audit.validate_r2b(example_r2b())["n"] == 3


def test_r2b_rejects_wrong_phase():
    report = example_r2b()
    report["phase"] = "171 R2A"
    with pytest.raises(ValueError, match="R2B"):
        audit.validate_r2b(report)


def test_r2b_rejects_wrong_number_of_cases():
    report = example_r2b()
    report["cases"] = report["cases"][:2]
    with pytest.raises(ValueError, match="three"):
        audit.validate_r2b(report)


def test_r2b_rejects_nonzero_proof_links():
    report = example_r2b()
    report["cases"][0]["proof_link_count"] = 1
    with pytest.raises(ValueError, match="gap case"):
        audit.validate_r2b(report)


def test_r2b_rejects_missing_uncertainty_marker():
    report = example_r2b()
    report["source"]["has_question_marker"] = False
    with pytest.raises(ValueError, match="unresolved"):
        audit.validate_r2b(report)


def test_r2b_rejects_unreviewed_dependency_list():
    report = example_r2b()
    report["source"]["references_in_proof"] = []
    with pytest.raises(ValueError, match="lacks"):
        audit.validate_r2b(report)


def test_locator_inventory_counts_only_matching_verified_given():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    hopf = next(x for x in inventory if x["locator"] == "(5.3)")
    prop = next(x for x in inventory if x["locator"] == "Proposition 5.6")
    assert hopf["assertion_count"] == 1
    assert hopf["matching_given_total"] == 1
    assert prop["assertion_count"] == 1
    assert prop["matching_given_total"] == 0


def test_locator_inventory_rejects_mismatched_given_conclusion():
    bridge = fake_registry()
    bridge.proof_links[0].step.conclusion = "unrelated"
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_locator_inventory_rejects_inference_as_given():
    bridge = fake_registry()
    bridge.proof_links[0].step.rule = SimpleNamespace(name="INFERENCE")
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_pi63_summary_never_equates_goal_and_candidate():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    output = audit.summarize_pi63(bridge, ("pi63", "Z4:DB"), inventory)
    assert output["typed_equal"] is False
    assert output["candidate_link_count"] == 0
    assert output["toda53_hopf_assertion_count"] == 1
    assert output["toda53_hopf_link_count"] == 1


def test_pi63_summary_refuses_target_proof_link():
    bridge = fake_registry()
    bridge.proof_links += (SimpleNamespace(
        assertion_id="shared:0:boundary:Proposition 5.6:pi6_3_group_relation",
        step=None,
    ),)
    with pytest.raises(ValueError, match="proof links"):
        audit.summarize_pi63(bridge, object(), audit.locator_inventory(bridge))


def test_markdown_does_not_claim_proof():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    output = audit.markdown_report({
        "inventory": inventory,
        "pi63": audit.summarize_pi63(bridge, ("pi63", "Z4:DB"), inventory),
    })
    assert "GIVEN に昇格させない" in output
    assert "(5.6)?" in output
    assert "ProofStep リンク：0件" in output


def test_git_guard_rejects_changed_production(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase165_r52_r9_shared_math.py\0"
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="non-audit"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_tracked_diff(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return " M data/sphere.csv"
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="modified"):
        audit.tracked_state(tmp_path)


def test_git_guard_allows_ahead_audit_only_commit(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "local-head"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "remote-base"
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase171_r2b_prop56_source_dependency_audit/audit.py\0"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.EXPECTED_BLOBS[args[1][5:]]
        return ""
    monkeypatch.setattr(audit, "git", fake)
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kw: SimpleNamespace(
        returncode=0, stdout=b"", stderr=b"",
    ))
    output = audit.tracked_state(tmp_path)
    assert output["head"] == "local-head"
    assert output["origin_develop"] == "remote-base"


def test_git_guard_rejects_diverged_upstream(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"):
            raise RuntimeError("not an ancestor")
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="diverged"):
        audit.tracked_state(tmp_path)


def test_run_dry_run_does_not_import_production(monkeypatch, tmp_path, capsys):
    report_path = tmp_path / "r2b.json"
    report_path.write_text(json.dumps(example_r2b()), encoding="utf-8")
    monkeypatch.setattr(audit, "tracked_state", lambda root: {"head": "fixed"})
    assert audit.run(tmp_path, report_path, dry_run=True) == 0
    text = capsys.readouterr().out
    assert "PHASE171_R2C_DRY_RUN=PASS" in text
    assert "PHASE171_R2C_RESULT=PASS" in text


def test_module_entrypoint_works_with_sibling_module(tmp_path):
    root = tmp_path / "isolated"
    (root / "package").mkdir(parents=True)
    (root / "package" / "__init__.py").write_text("", encoding="utf-8")
    (root / "sibling.py").write_text("VALUE = 11\n", encoding="utf-8")
    (root / "package" / "run.py").write_text(
        "from sibling import VALUE\nprint(VALUE)\n", encoding="utf-8",
    )
    import sys
    result = subprocess.run(
        [sys.executable, "-B", "-m", "package.run"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "11"


def test_locator_inventory_does_not_adopt_nonfixed_statement():
    bridge = fake_registry()
    assertion = next(item for item in bridge.registry._assertions.values()
                     if item.reference_id == "h")
    assertion.origin = SimpleNamespace(value="source_archive")
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_run_normal_records_read_only_inventory(monkeypatch, tmp_path, capsys):
    import sys
    import types

    report_path = tmp_path / "r2b.json"
    report_path.write_text(json.dumps(example_r2b()), encoding="utf-8")
    bridge = fake_registry()
    maths = types.ModuleType("phase165_r52_r9_shared_math")
    maths.build_shared_typed_bridge = lambda: bridge
    goals = types.ModuleType("phase165_r55_nk_only_goal")
    goals.registered_group_goal_candidates = lambda bridge, n, k: (("pi63", "DB"),)
    monkeypatch.setitem(sys.modules, maths.__name__, maths)
    monkeypatch.setitem(sys.modules, goals.__name__, goals)
    monkeypatch.setattr(audit, "tracked_state", lambda root: {"head": "fixed"})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    assert audit.run(tmp_path, report_path, dry_run=False) == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2C_DETAIL=" in output
    assert "PHASE171_R2C_TRACKED_UNCHANGED=True" in output
    report = list((tmp_path / "EHPProofTracerRecovery").glob("*/frontier.json"))
    assert len(report) == 1
    payload = json.loads(report[0].read_text(encoding="utf-8"))
    assert payload["pi63"]["typed_equal"] is False
    assert payload["pi63"]["toda53_hopf_link_count"] == 1
    assert payload["tracked_unchanged"] is True
