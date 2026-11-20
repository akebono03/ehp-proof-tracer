"""Focused contracts for the isolated general zero-right-composition rule."""
from __future__ import annotations

from dataclasses import replace
import json

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase176_r3r10_right_zero_transport_isolated import audit
from phase176_r3r10_right_zero_transport_isolated.rule import (
    RULE_NAME, expand_right_zero_transport, right_zero_transport_inputs,
    right_zero_transport_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def fixture():
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    base = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
                          Composition(a, b), Zero())
    goal = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
                          Composition(a, Composition(b, c)), Zero())
    return base, goal


def test_isolated_rule_infers_actual_proof_step() -> None:
    base, goal = fixture()
    assert right_zero_transport_inputs(goal, base) == (base,)
    options = expand_right_zero_transport(goal, base)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == (base,)
    parent = ProofStep(base, (), ProofRule.INFERENCE)
    matches = find_inference_matches_for_rule(options[0].rule, (parent,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (parent,)


def test_missing_parent_and_direct_given_rejected() -> None:
    base, goal = fixture()
    rule = right_zero_transport_rule(goal, base)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (ProofStep(base, (), ProofRule.GIVEN),)) == ()


def test_wrong_prefix_rejected() -> None:
    base, goal = fixture()
    bad = replace(base, source_generator=Composition(base.source_generator.right,
                                                     base.source_generator.left))
    assert right_zero_transport_inputs(goal, bad) is None
    assert expand_right_zero_transport(goal, bad) == ()


def test_wrong_dimension_or_map_rejected() -> None:
    base, goal = fixture()
    bad = replace(base, map=TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(8, 3)))
    assert right_zero_transport_inputs(goal, bad) is None
    bad_goal = replace(goal, map=TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(9, 3)))
    assert right_zero_transport_inputs(bad_goal, base) is None


def test_nonzero_base_and_nonzero_goal_rejected() -> None:
    base, goal = fixture()
    assert right_zero_transport_inputs(goal, replace(base, target_generator=base.source_generator)) is None
    assert right_zero_transport_inputs(replace(goal, target_generator=goal.source_generator), base) is None


def test_different_last_factor_rejected() -> None:
    base, goal = fixture()
    fourth = HomotopyElement("d", dimension=7, source=8, target=7)
    extended = replace(goal, source_generator=Composition(goal.source_generator, fourth),
                       map=TodaSuspensionMap(TodaPrimaryGroup(8, 2), TodaPrimaryGroup(9, 3)))
    assert right_zero_transport_inputs(extended, base) is None


def test_source_contract_fails_closed(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)
    (tmp_path / next(iter(audit.SOURCES))).write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.check_sources(tmp_path)


def test_dry_run_never_executes_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker started"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["root_proof_complete"] is False
    assert report["full_pytest"] == "NOT_RUN"
