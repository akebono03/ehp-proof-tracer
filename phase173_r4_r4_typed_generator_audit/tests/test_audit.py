"""Focused offline contracts and typed symbolic checks for Phase 173 R4-R4."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

from phase173_r4_r4_typed_generator_audit import audit


@pytest.fixture
def types(monkeypatch: pytest.MonkeyPatch):
    """Provide stand-in dataclasses only; no database or proof engine is mocked as evidence."""
    @dataclass(frozen=True)
    class GeneratorSymbol:
        family: str
        index: int | None = None
        decoration: str | None = None

    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int
        generator: GeneratorSymbol

    @dataclass(frozen=True)
    class Composition:
        left: object
        right: object

    @dataclass(frozen=True)
    class IteratedSuspension:
        expression: object
        exponent: int

    @dataclass(frozen=True)
    class FiniteCyclicGroup:
        order: int
        generator: object

    @dataclass(frozen=True)
    class FreeCyclicGroup:
        generator: object

    @dataclass(frozen=True)
    class DirectSumGroup:
        summands: tuple

    @dataclass(frozen=True)
    class TodaPrimaryGroupZeroStatement:
        group: object

    class RelationType(Enum):
        EQUALITY = "equality"

    @dataclass(frozen=True)
    class Relation:
        lhs: object
        rhs: object
        relation_type: RelationType

    expression = ModuleType("expression")
    groups = ModuleType("homotopy_groups")
    proof = ModuleType("proof")
    for name in ("GeneratorSymbol", "HomotopyElement", "Composition", "IteratedSuspension"):
        setattr(expression, name, locals()[name])
    for name in ("FiniteCyclicGroup", "FreeCyclicGroup", "DirectSumGroup", "TodaPrimaryGroupZeroStatement"):
        setattr(groups, name, locals()[name])
    proof.Relation = Relation
    proof.RelationType = RelationType
    monkeypatch.setitem(sys.modules, "expression", expression)
    monkeypatch.setitem(sys.modules, "homotopy_groups", groups)
    monkeypatch.setitem(sys.modules, "proof", proof)
    nu4 = HomotopyElement("ν₄", 4, 7, 4, GeneratorSymbol("ν", 4))
    hopf = ModuleType("phase173_r4_r1_lemma54_source_bridge.source")
    hopf.canonical_hopf_relation = lambda: SimpleNamespace(lhs=SimpleNamespace(expression=nu4))
    monkeypatch.setitem(sys.modules, hopf.__name__, hopf)
    return SimpleNamespace(GeneratorSymbol=GeneratorSymbol, HomotopyElement=HomotopyElement,
                           Composition=Composition, IteratedSuspension=IteratedSuspension,
                           FiniteCyclicGroup=FiniteCyclicGroup, FreeCyclicGroup=FreeCyclicGroup,
                           DirectSumGroup=DirectSumGroup, TodaPrimaryGroupZeroStatement=TodaPrimaryGroupZeroStatement,
                           Relation=Relation, RelationType=RelationType, nu4=nu4)


def _eta(t, i: int):
    return t.HomotopyElement("η" + str(i).translate(audit.SUBSCRIPT_DIGITS), i, i + 1, i,
                             t.GeneratorSymbol("η", i))


def _nu_prime(t):
    return t.HomotopyElement("ν'", 3, 6, 3, t.GeneratorSymbol("\\nu'"))


def _present(t, group):
    return t.Relation("group", group, t.RelationType.EQUALITY)


def test_typed_nu_prime_eta6_suspension_is_expected_shape_only(types) -> None:
    t = types
    source = t.Composition(_nu_prime(t), _eta(t, 6))
    actual = audit._suspend_verified_shape(source)
    assert actual == t.Composition(t.IteratedSuspension(_nu_prime(t), 1), _eta(t, 7))
    assert audit._typed_endpoints(source) == (7, 3)
    assert audit._typed_endpoints(actual) == (8, 4)


def test_pi8_toda56_symbolic_image_multiset(types) -> None:
    t = types
    # pi_7^3 = Z/2{nu' eta_6}; pi_8^7 = Z/2{eta_7}
    source3 = _present(t, t.FiniteCyclicGroup(2, t.Composition(_nu_prime(t), _eta(t, 6))))
    source7 = _present(t, t.FiniteCyclicGroup(2, _eta(t, 7)))
    expected = (
        t.FiniteCyclicGroup(2, t.Composition(t.nu4, _eta(t, 7))),
        t.FiniteCyclicGroup(2, t.Composition(t.IteratedSuspension(_nu_prime(t), 1), _eta(t, 7))),
    )
    mapped = audit._map_components(source3, source7)
    assert audit._exact_multiset_match(mapped, expected)
    assert audit._exact_multiset_match(mapped, expected[::-1])


def test_pi9_toda56_composite_eta_squared_image(types) -> None:
    t = types
    eta6_square = t.Composition(_eta(t, 6), _eta(t, 7))
    eta7_square = t.Composition(_eta(t, 7), _eta(t, 8))
    source3 = _present(t, t.FiniteCyclicGroup(2, t.Composition(_nu_prime(t), eta6_square)))
    source7 = _present(t, t.FiniteCyclicGroup(2, eta7_square))
    target = (
        t.FiniteCyclicGroup(2, t.Composition(t.nu4, eta7_square)),
        t.FiniteCyclicGroup(2, t.Composition(t.IteratedSuspension(_nu_prime(t), 1), eta7_square)),
    )
    assert audit._exact_multiset_match(audit._map_components(source3, source7), target)


def test_pi10_toda56_zero_first_source(types) -> None:
    t = types
    nu7 = t.HomotopyElement("ν₇", 7, 10, 7, t.GeneratorSymbol("ν", 7))
    zero = t.TodaPrimaryGroupZeroStatement("pi9^3")
    source7 = _present(t, t.FiniteCyclicGroup(8, nu7))
    expected = (t.FiniteCyclicGroup(8, t.Composition(t.nu4, nu7)),)
    assert audit._exact_multiset_match(audit._map_components(zero, source7), expected)


def test_wrong_eta_index_and_untyped_composition_rejected(types) -> None:
    t = types
    eta_bad = t.HomotopyElement("η₆", 6, 7, 6, t.GeneratorSymbol("η", 7))
    assert audit._suspend_verified_shape(eta_bad) is None
    malformed = t.Composition(_nu_prime(t), _eta(t, 8))
    assert audit._typed_endpoints(malformed) is None
    assert audit._suspend_verified_shape(malformed) is None


def test_unknown_generator_cannot_silently_be_normalized(types) -> None:
    t = types
    unknown = t.HomotopyElement("mystery", 3, 6, 3, t.GeneratorSymbol("unknown"))
    assert audit._suspend_verified_shape(unknown) is None
    assert audit._map_components(_present(t, t.FiniteCyclicGroup(2, unknown)),
                                 _present(t, t.FiniteCyclicGroup(2, _eta(t, 7)))) is None


def test_exact_match_rejects_wrong_order_and_duplicate(types) -> None:
    t = types
    a = t.FiniteCyclicGroup(2, _eta(t, 7))
    b = t.FiniteCyclicGroup(4, _eta(t, 7))
    assert not audit._exact_multiset_match((a,), (b,))
    assert not audit._exact_multiset_match((a, a), (a,))
    assert not audit._exact_multiset_match((a, b), (a, a))
    assert not audit._exact_multiset_match(None, (a,))


def test_existing_i7_is_protected_and_not_redeclared() -> None:
    assert audit.TARGET_DIMENSIONS == (7, 8, 9, 10)
    assert audit.REVIEWED_HEAD == "cd93bac8a2e4c08742f7eabc0ba97fda294d20b6"


def test_report_never_declares_generator_proof(tmp_path: Path) -> None:
    report = {"observation": {"rows": [
        {"group": "pi_8^4", "status": "SYNTACTIC_MATCH_UNPROVED",
         "abstract_compatible": True, "symbolic_generator_match": True,
         "first_admitted_db_prior": True, "second_admitted_db_prior": True,
         "generator_images_proved": False, "result_is_complete_proof": False,
         "citation": {"lemma54_eligible": True}}
    ]}}
    audit.write_report(tmp_path, report)
    saved = json.loads((tmp_path / "audit.json").read_text(encoding="utf-8"))
    assert saved["observation"]["rows"][0]["generator_images_proved"] is False
    assert "証明完了を意味しない" in (tmp_path / "audit.md").read_text(encoding="utf-8")


def test_dryrun_does_not_call_runtime_proof_system(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root, remote: {
        "branch": "develop", "head": audit.REVIEWED_HEAD,
        "source_guard": "PASS", "remote_checked": remote,
    })
    monkeypatch.setattr(audit, "inspect_live", lambda root: pytest.fail("no live proof in DryRun"))
    assert audit.run(tmp_path, dry_run=True, remote=False) == 0
    reports = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r4_r4_*/audit.json"))
    assert len(reports) == 1
    saved = json.loads(reports[0].read_text(encoding="utf-8"))
    assert saved["result"] == "DRY_RUN_PASS"
    assert saved["tracked_unchanged"] is True


def test_preflight_rejects_wrong_head_without_accessing_runtime(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "unreviewed",
    }
    monkeypatch.setattr(audit, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="unreviewed"):
        audit.preflight(tmp_path, remote=False)


def test_preflight_refuses_dirty_tracked_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): " M relation_rules.py",
    }
    monkeypatch.setattr(audit, "git", lambda root, *args: answers[args])
    with pytest.raises(RuntimeError, match="tracked changes"):
        audit.preflight(tmp_path, remote=False)
