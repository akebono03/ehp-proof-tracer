"""Focused fail-closed R4R5 lineage, prior-evidence and source guard tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from types import ModuleType

import pytest

from phase175_r4r5_eta7_annihilator_isolated import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R4",
        "mode": "SOURCE_FIRST_PREMISE_FRONTIER_AUDIT",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "public_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.EXPECTED_PRIOR_HEAD, "pinned_source_count": 18},
        "premise_count": 6,
        "verified_parent_steps_replayed_here": 0,
        "premises": [
            {"index": n, "verified_parent_step_in_r4r4": False}
            for n in range(1, 7)
        ],
    }


def test_prior_real_gate_is_not_a_proof_certificate() -> None:
    found = audit.validate_prior_report(prior_fixture())
    assert found["prior_head"] == audit.EXPECTED_PRIOR_HEAD
    assert found["premises"] == 6
    assert found["prior_audit_is_not_a_proof"] is True


@pytest.mark.parametrize("key,value", [
    ("phase", "175-R4R3"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("public_proof_complete", True),
    ("full_pytest_executed", True),
    ("premise_count", 5),
])
def test_prior_scope_rejects_changed_fields(key: str, value: object) -> None:
    record = prior_fixture()
    record[key] = value
    with pytest.raises(RuntimeError, match="PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior_report(record)


@pytest.mark.parametrize("target,value", [
    ("head", "f" * 40),
    ("pinned_source_count", 17),
])
def test_prior_head_and_pins_rejected(target: str, value: object) -> None:
    record = prior_fixture()
    record["preflight"][target] = value
    with pytest.raises(RuntimeError, match="PRIOR_HEAD_OR_SOURCE_INVALID"):
        audit.validate_prior_report(record)


def test_prior_premises_must_not_be_marked_proved() -> None:
    record = prior_fixture()
    record["premises"][2]["verified_parent_step_in_r4r4"] = True
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)


def test_prior_missing_or_malformed_rows_rejected() -> None:
    record = prior_fixture()
    record["premises"].pop()
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)
    record = prior_fixture()
    record["premises"][1] = "bad row"
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)


def test_latest_successful_report_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    a, b = folder / "20261117T055000Z", folder / "20261117T055100Z"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    (a / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    rejected = prior_fixture()
    rejected["gate"] = "FAIL_R4R4"
    (b / "report.json").write_text(json.dumps(rejected), encoding="utf-8")
    assert audit.latest_prior_report() == a / "report.json"
    assert audit.latest_prior_report(a / "report.json") == (a / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R4_REPORT_MISSING"):
        audit.latest_prior_report(folder / "missing.json")


def test_source_pins_require_exact_committed_blobs(monkeypatch, tmp_path: Path) -> None:
    for name in audit.EXTRA_SOURCE_PINS:
        file = tmp_path / name
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text("fixture", encoding="utf-8")

    def good_git(root, *args, allow_failure=False):
        name = args[-1].removeprefix("HEAD:")
        return 0, audit.EXTRA_SOURCE_PINS[name]

    monkeypatch.setattr(audit, "git", good_git)
    monkeypatch.setattr(audit, "verify_code_and_source_pins", lambda root: {})
    assert audit.verify_source_pins(tmp_path) == audit.EXTRA_SOURCE_PINS

    def bad_git(root, *args, allow_failure=False):
        return 0, "f" * 40

    monkeypatch.setattr(audit, "git", bad_git)
    with pytest.raises(RuntimeError, match="SOURCE_PIN_DRIFT"):
        audit.verify_source_pins(tmp_path)


def test_lineage_allow_only_reviewed_r4r4_package(monkeypatch, tmp_path: Path) -> None:
    new = "a" * 40

    def good_git(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, new
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase175_r4r4_pi95_premise_frontier/audit.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", good_git)
    assert audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, new) == [
        "phase175_r4r4_pi95_premise_frontier/audit.py",
    ]


def test_lineage_reject_unrelated_code_change(monkeypatch, tmp_path: Path) -> None:
    new = "a" * 40

    def bad_git(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, new
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase165_r52_r9_shared_math.py\nphase175_r4r4_pi95_premise_frontier/audit.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", bad_git)
    with pytest.raises(RuntimeError, match="UNREVIEWED_LINEAGE_CHANGES"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, new)


def test_lineage_rejects_wrong_prior_and_wrong_current(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args, allow_failure=False: (0, "a" * 40))
    with pytest.raises(RuntimeError, match="UNREVIEWED_PRIOR_HEAD"):
        audit.validate_prior_lineage(tmp_path, "b" * 40, "a" * 40)
    with pytest.raises(RuntimeError, match="HEAD_CHANGED"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, "b" * 40)


def test_scope_cannot_silently_claim_pi95_complete() -> None:
    assert audit.FINAL_GATE.endswith("NOT_PUBLIC")
    assert audit.DRY_GATE.endswith("DRYRUN")
    assert audit.PACKAGE == "phase175_r4r5_eta7_annihilator_isolated"
    assert "proof.py" in audit.EXTRA_SOURCE_PINS
    assert len(audit.EXTRA_SOURCE_PINS) == 11


def _install_checked_prior_fixture(monkeypatch, *, source=None, target=None,
                                   order_allowed=True, admitted=True, verified=True):
    """Mock existing ordered DB API only; no actual source proof is fabricated."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType

    eta7 = HomotopyElement("η_7", 7, source=8, target=7,
                           generator=GeneratorSymbol("η", index=7))
    nu5eta8 = HomotopyElement("ν5η8", 5, source=9, target=5)
    if source is None:
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, eta7), RelationType.EQUALITY)
    if target is None:
        target = Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(2, nu5eta8), RelationType.EQUALITY)

    calls = []
    parent_name = "phase169_r10e4_ordered_db_prior"
    child_name = parent_name + ".db_prior"
    parent = ModuleType(parent_name)
    parent.__path__ = []
    child = ModuleType(child_name)

    def get_result(n, k):
        calls.append(("read", n, k))
        return {(7, 1): source, (5, 4): target}.get((n, k))

    def precedes(n, k, tn, tk):
        calls.append(("order", n, k, tn, tk))
        return order_allowed

    def admit(statement, *, proof_target):
        calls.append(("admit", statement, proof_target))
        if not admitted:
            return None
        return ProofStep(statement, (), ProofRule.GIVEN,
                         note="ADOPTED_DATABASE_PRIOR; independent reference not asserted",
                         inference_rule=InferenceRule(name="test-only adoption"))

    def check(step, *, proof_target):
        calls.append(("verify", step.conclusion, proof_target))
        return verified

    child.exact_prior_database_result = get_result
    child.precedes_db_goal = precedes
    child.admitted_db_step = admit
    child.verified_db_step = check
    monkeypatch.setitem(sys.modules, parent_name, parent)
    monkeypatch.setitem(sys.modules, child_name, child)
    return calls


def test_reuse_ordered_prior_does_not_replay_proof(monkeypatch) -> None:
    calls = _install_checked_prior_fixture(monkeypatch)
    result = audit.eta7_prior_and_isolated_zero()
    assert result["prior_status"] == "ADOPTED_DATABASE_PRIOR"
    assert result["prior_proof_search_executed"] is False
    assert result["prior_proof_tree_reconstructed"] is False
    assert result["prior_rechecked_against_explicit_csv"] is True
    assert result["derived_rule_proof_step"] is True
    assert result["derived_step_has_authenticated_db_premise"] is True
    assert result["adopted_db_prior_step_count"] == 1
    assert result["new_literature_given"] == 0
    assert result["registered_in_public"] is False
    assert [c[0] for c in calls] == ["read", "read", "order", "admit", "verify"]
    assert calls[0] == ("read", 7, 1)
    assert calls[1] == ("read", 5, 4)


@pytest.mark.parametrize("wrong", ["wrong_order", "wrong_generator", "wrong_group"])
def test_wrong_prior_group_rejected(monkeypatch, wrong: str) -> None:
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation
    eta = HomotopyElement("η_7", 7, source=8, target=7,
                          generator=GeneratorSymbol("η", index=7))
    if wrong == "wrong_order":
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(4, eta))
    elif wrong == "wrong_generator":
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2,
                          HomotopyElement("η_7", 7, source=8, target=7,
                                          generator=GeneratorSymbol("ν", index=7))))
    else:
        source = Relation(TodaPrimaryGroup(9, 7), FiniteCyclicGroup(2, eta))
    _install_checked_prior_fixture(monkeypatch, source=source)
    with pytest.raises(RuntimeError, match="PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID|PI87_DB_GENERATOR_UNVERIFIED"):
        audit.eta7_prior_and_isolated_zero()


def test_prior_order_rejects_unapproved_reuse(monkeypatch) -> None:
    _install_checked_prior_fixture(monkeypatch, order_allowed=False)
    with pytest.raises(RuntimeError, match="PRIOR_ORDER_DISALLOWED"):
        audit.eta7_prior_and_isolated_zero()


@pytest.mark.parametrize("admitted,verified", [(False, True), (True, False)])
def test_db_prior_requires_existing_authentication(monkeypatch, admitted: bool, verified: bool) -> None:
    _install_checked_prior_fixture(monkeypatch, admitted=admitted, verified=verified)
    with pytest.raises(RuntimeError, match="DB_PRIOR_AUTHENTICATION_FAILED"):
        audit.eta7_prior_and_isolated_zero()


def test_target_is_not_marked_as_proved(monkeypatch) -> None:
    from homotopy_groups import TodaPrimaryGroup
    from proof import Relation
    from expression import Zero
    target = Relation(TodaPrimaryGroup(10, 5), Zero())
    _install_checked_prior_fixture(monkeypatch, target=target)
    with pytest.raises(RuntimeError, match="PI95_DB_TARGET_GOAL_MISSING"):
        audit.eta7_prior_and_isolated_zero()


def test_missing_group_prior_rejected(monkeypatch) -> None:
    _install_checked_prior_fixture(monkeypatch, source=False)
    with pytest.raises(RuntimeError, match="PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID"):
        audit.eta7_prior_and_isolated_zero()


def _install_checked_direct_sum_prior_fixture(
    monkeypatch, *, source=None, target=None, order_allowed=True,
    admitted=True, verified=True,
):
    """Supply test-only ordered DB responses; no real proof is claimed."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from proof import InferenceRule, ProofRule, ProofStep, Relation

    eta7 = HomotopyElement("η_7", 7, source=8, target=7,
                           generator=GeneratorSymbol("η", index=7))
    nu4 = HomotopyElement("ν_4", 4, source=7, target=4,
                          generator=GeneratorSymbol("ν", index=4))
    nuprime = HomotopyElement("ν'", 3, source=6, target=3,
                             generator=GeneratorSymbol("ν'", index=3))
    x = Composition(nu4, eta7)
    y = Composition(IteratedSuspension(nuprime, 1), eta7)
    if source is None:
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
            FiniteCyclicGroup(2, x), FiniteCyclicGroup(2, y),
        )))
    if target is None:
        target = Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(
            2, HomotopyElement("target", 5, source=9, target=5),
        ))
    calls = []
    parent_name = "phase169_r10e4_ordered_db_prior"
    child_name = parent_name + ".db_prior"
    parent = ModuleType(parent_name)
    parent.__path__ = []
    child = ModuleType(child_name)

    def get_result(n, k):
        calls.append(("read", n, k))
        return {(4, 4): source, (5, 4): target}.get((n, k))

    def precedes(n, k, tn, tk):
        calls.append(("order", n, k, tn, tk))
        return order_allowed

    def admit(statement, *, proof_target):
        calls.append(("admit", statement, proof_target))
        if not admitted:
            return None
        return ProofStep(statement, (), ProofRule.GIVEN,
                         note="ADOPTED_DATABASE_PRIOR; independent reference not asserted",
                         inference_rule=InferenceRule(name="test-only DB adoption"))

    def check(step, *, proof_target):
        calls.append(("verify", step.conclusion, proof_target))
        return verified

    child.exact_prior_database_result = get_result
    child.precedes_db_goal = precedes
    child.admitted_db_step = admit
    child.verified_db_step = check
    monkeypatch.setitem(sys.modules, parent_name, parent)
    monkeypatch.setitem(sys.modules, child_name, child)
    return calls


def test_real_shape_direct_sum_prior_is_reused_without_replay(monkeypatch) -> None:
    calls = _install_checked_direct_sum_prior_fixture(monkeypatch)
    data = audit.direct_sum_prior_and_isolated_zero()
    assert data["prior_group"] == "pi_8^4"
    assert data["prior_status"] == "ADOPTED_DATABASE_PRIOR"
    assert data["prior_proof_search_executed"] is False
    assert data["prior_proof_tree_reconstructed"] is False
    assert data["summands_verified_in_isolation"] == 2
    assert data["inferred_zero_steps"] == 2
    assert all(row["authenticated_prior_parent"] for row in data["summand_derivations"])
    assert all(row["order"] == 2 for row in data["summand_derivations"])
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
    assert all(row["inference_rule"] == RULE_NAME
               for row in data["summand_derivations"])
    assert [item[0] for item in calls] == ["read", "read", "order", "admit", "verify"]
    assert calls[0] == ("read", 4, 4)
    assert calls[1] == ("read", 5, 4)


@pytest.mark.parametrize("order_allowed,admitted,verified", [
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_direct_sum_prior_authentication_fail_closed(monkeypatch, order_allowed, admitted, verified) -> None:
    _install_checked_direct_sum_prior_fixture(
        monkeypatch, order_allowed=order_allowed, admitted=admitted, verified=verified,
    )
    with pytest.raises(RuntimeError, match="PRIOR_ORDER_OR_TARGET_INVALID|DB_PRIOR_AUTHENTICATION_FAILED"):
        audit.direct_sum_prior_and_isolated_zero()


def test_direct_sum_prior_bad_shape_rejected(monkeypatch) -> None:
    from expression import HomotopyElement
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation
    g = HomotopyElement("g", 4, source=8, target=4)
    wrong = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, g),)))
    _install_checked_direct_sum_prior_fixture(monkeypatch, source=wrong)
    with pytest.raises(RuntimeError, match="PI84_DIRECT_SUM_DB_PRIOR_MISSING"):
        audit.direct_sum_prior_and_isolated_zero()
