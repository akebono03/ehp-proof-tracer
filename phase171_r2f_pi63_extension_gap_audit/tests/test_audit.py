"""Source-independent, narrow tests for Phase 171 R2F read-only audit."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase171_r2f_pi63_extension_gap_audit import audit


def test_git_read_blocks_mutating_commands(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "reset", "--hard")
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "checkout", "--", "proof.py")


def test_typed_differences_rejects_same_text_with_different_types() -> None:
    left = SimpleNamespace(name="nu-prime", source=6)
    right = {"name": "nu-prime", "source": 6}
    result = audit.typed_differences(left, right)
    assert result == [{
        "path": "generator", "reason": "type_mismatch",
        "left": "SimpleNamespace", "right": "dict",
    }]


def test_typed_differences_detects_dataclass_field_mismatch() -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Generator:
        family: str
        decoration: str

    differences = audit.typed_differences(Generator("nu", "prime"), Generator("nu", "apostrophe"))
    assert len(differences) == 1
    assert differences[0]["path"] == "generator.decoration"


def test_assessment_keeps_sources_separate_from_proven_inference() -> None:
    sample = {locator: {"count": 1} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=0,
    )
    assert len(rows) == 8
    assert rows[4]["key"] == "nu_prime_hopf"
    assert rows[5]["key"] == "nu_prime_double"
    assert all(row["certified_as_completed_inference"] is False for row in rows)
    assert rows[-1]["screened_fixed_given_count"] == 0


def test_assessment_reports_absent_prop22_source_without_claiming_proof() -> None:
    sample = {locator: {"count": 0} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=2,
    )
    assert rows[0]["key"] == "prop22_hopf_composition"
    assert rows[0]["screened_fixed_given_count"] == 0
    assert "候補" in rows[-1]["note"]


def test_dry_run_preserves_snapshot_and_does_not_load_proof_engine(monkeypatch, tmp_path: Path, capsys) -> None:
    before = {"branch": "develop", "head": "dummy", "tracked_diff_sha256": "hash", "status": [" M source.py"]}
    monkeypatch.setattr(audit, "snapshot", lambda root: before.copy())
    assert audit.run(tmp_path, dry_run=True, search=False) == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2F_RESULT=PASS_AUDIT_ONLY" in output
    assert "PHASE171_R2F_DRY_RUN=PASS" in output


def test_dry_run_fails_closed_when_snapshot_changes(monkeypatch, tmp_path: Path) -> None:
    calls = iter((
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "one"},
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "two"},
    ))
    monkeypatch.setattr(audit, "snapshot", lambda root: next(calls))
    with pytest.raises(RuntimeError, match="worktree changed"):
        audit.run(tmp_path, dry_run=True, search=False)


@pytest.mark.parametrize("search", (False, True))
def test_normal_run_preserves_path_after_root_frontier(monkeypatch, tmp_path: Path, search: bool) -> None:
    """Exercise the actual non-DryRun branch and reject a dict in snapshot(root)."""
    import json
    import sys
    from dataclasses import dataclass
    from types import ModuleType

    original_root = tmp_path / "repository"
    original_root.mkdir()
    recovery = tmp_path / "recovery"
    monkeypatch.setenv("LOCALAPPDATA", str(recovery))
    state = {"branch": "develop", "head": "test-head", "tracked_diff_sha256": "test-diff", "status": []}
    observed_roots = []

    def guarded_snapshot(path: Path) -> dict:
        assert isinstance(path, Path), "repository root must remain a Path, not an expansion dict"
        assert path == original_root
        observed_roots.append(path)
        return state.copy()

    monkeypatch.setattr(audit, "snapshot", guarded_snapshot)

    @dataclass(frozen=True)
    class FakeMultiple:
        coefficient: int
        expression: object

    @dataclass(frozen=True)
    class FakeFiniteCyclic:
        order: int
        generator: object

    @dataclass(frozen=True)
    class FakeCyclic:
        group: object
        generator: object
        order: int

    target_generator = object()
    target_group = object()
    goal = SimpleNamespace(
        lhs=target_group,
        rhs=FakeFiniteCyclic(order=4, generator=target_generator),
    )
    double = SimpleNamespace(lhs=FakeMultiple(2, target_generator), rhs="eta-composite")
    source_id = "shared:12:" + audit.EXPECTED_DOUBLE_SUFFIX
    hopf_id = "shared:8:" + audit.EXPECTED_HOPF_SUFFIX
    reference = SimpleNamespace(locator="(5.3)", publication_position=8100)
    registry = SimpleNamespace(
        assertion=lambda assertion_id: SimpleNamespace(reference_id="adopted53"),
        reference=lambda reference_id: reference,
    )
    complete = SimpleNamespace(registry=registry)
    screened = SimpleNamespace(registry=registry, proof_links=())

    class FakeProofRule:
        GIVEN = object()
        INFERENCE = object()

    # Only the externally imported collaborators are stubbed. The real
    # audit.run(), including its final snapshot and JSON write, executes.
    def stub(name: str, **attributes: object) -> None:
        module = ModuleType(name)
        for attribute, value in attributes.items():
            setattr(module, attribute, value)
        monkeypatch.setitem(sys.modules, name, module)

    parent = ModuleType("phase166_r3t_goal_source_binding")
    parent.__path__ = []
    monkeypatch.setitem(sys.modules, parent.__name__, parent)
    stub("expression", Multiple=FakeMultiple)
    stub("homotopy_groups", FiniteCyclicGroup=FakeFiniteCyclic)
    stub("phase165_r12_r2_quotient_rules", CyclicStructureStatement=FakeCyclic)
    stub("phase165_r12_r11_prop42_unified", prefer_universal_prop42_derivation=lambda bridge: bridge)
    stub("phase165_r52_r16_web_citation_gate", screen_shared_proof_context=lambda *args, **kwargs: screened)
    stub(
        "phase165_r52_r9_shared_math",
        build_shared_typed_bridge=lambda: complete,
        shared_expansion_provider=lambda *args, **kwargs: (lambda goal_value: ()),
    )
    search_result = SimpleNamespace(
        status="search_failed", conclusion=None,
        proven_steps=(), open_goals=(goal,),
    )
    stub(
        "phase165_r55_nk_only_goal",
        registered_group_goal_candidates=lambda *args, **kwargs: (goal,),
        search_group_from_registered_goal=lambda *args, **kwargs: search_result,
    )
    stub(
        "phase166_r3t_goal_source_binding.goal_source",
        resolve_specialized_goal_citing_id=lambda *args, **kwargs: audit.EXPECTED_TARGET,
    )
    stub("phase166_r3c_publication_order", precedes_citing_assertion=lambda *args: True)
    stub("proof", ProofRule=FakeProofRule)

    monkeypatch.setattr(
        audit, "matching_cited_steps",
        lambda bridge, suffix: ((source_id, double),)
        if suffix == audit.EXPECTED_DOUBLE_SUFFIX else ((hopf_id, "hopf"),),
    )
    monkeypatch.setattr(
        audit, "expansion_inventory",
        lambda goal_value, provider, bridge: {
            "count": 2, "rules": {"audited candidate": 2}, "examples": [],
        },
    )
    monkeypatch.setattr(
        audit, "source_inventory",
        lambda bridge: {locator: {"count": 0} for locator in audit.LOCATORS},
    )
    assert audit.run(original_root, dry_run=False, search=search) == 0
    assert observed_roots == [original_root, original_root]
    reports = list((recovery / "EHPProofTracerRecovery").glob("phase171_r2f_*/audit.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["git_after_identical"] is True
    assert report["root_expansions"]["rules"] == {"audited candidate": 2}
    assert (report["runtime_search"] is not None) is search
