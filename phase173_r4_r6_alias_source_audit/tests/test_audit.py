"""Focused read-only checks for eta aliases and source-position guards."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import pytest

from phase173_r4_r6_alias_source_audit import audit


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


def eta(index: int, *, underscore: bool = False, source: int | None = None,
        generator_index: int | None = None) -> HomotopyElement:
    name = "η_" + str(index) if underscore else "η" + str(index).translate(audit._SUBSCRIPTS)
    return HomotopyElement(name, index, index + 1 if source is None else source,
                           index, GeneratorSymbol("η", index if generator_index is None else generator_index))


def test_eta_alias_is_exactly_two_spellings() -> None:
    assert audit.eta_name_alias(eta(7, underscore=True), eta(7))
    assert audit.eta_name_alias(eta(7), eta(7, underscore=True))
    assert audit.eta_name_alias(eta(7), eta(7))


@pytest.mark.parametrize("wrong", [
    HomotopyElement("η_8", 8, 9, 8, GeneratorSymbol("η", 8)),
    HomotopyElement("η_7", 7, 8, 7, GeneratorSymbol("ν", 7)),
    HomotopyElement("eta7", 7, 8, 7, GeneratorSymbol("η", 7)),
    HomotopyElement("η_7", 7, 9, 7, GeneratorSymbol("η", 7)),
    HomotopyElement("η_7", 7, 8, 7, GeneratorSymbol("η", 8)),
    HomotopyElement("η_7", 7, 8, 7, GeneratorSymbol("η", 7, "prime")),
])
def test_eta_alias_rejects_nonidentical_typed_element(wrong: HomotopyElement) -> None:
    assert not audit.eta_name_alias(eta(7), wrong)
    assert not audit.alias_equal(eta(7), wrong)


def test_pi8_composition_eta_alias_only() -> None:
    prime = HomotopyElement("ν'", 3, 6, 3, GeneratorSymbol("\\nu'"))
    first = FiniteCyclicGroup(2, Composition(IteratedSuspension(prime, 1), eta(7, underscore=True)))
    second = FiniteCyclicGroup(2, Composition(IteratedSuspension(prime, 1), eta(7)))
    assert first != second
    assert audit.components_match_alias((first,), (second,))


def test_pi9_pi10_exact_also_matches_alias() -> None:
    nu4 = HomotopyElement("ν₄", 4, 7, 4, GeneratorSymbol("ν", 4))
    eta7_squared = Composition(eta(7), eta(8))
    a = FiniteCyclicGroup(2, Composition(nu4, eta7_squared))
    b = FiniteCyclicGroup(8, nu4)
    assert audit.components_match_alias((a, b), (b, a))


def test_wrong_group_order_is_not_equivalent() -> None:
    a = FiniteCyclicGroup(2, eta(7))
    b = FiniteCyclicGroup(4, eta(7, underscore=True))
    assert not audit.components_match_alias((a,), (b,))
    assert not audit.components_match_alias((a, a), (a,))


def test_ambiguous_matching_fails_closed() -> None:
    x = FiniteCyclicGroup(2, eta(7))
    y = FiniteCyclicGroup(2, eta(7, underscore=True))
    assert not audit.components_match_alias((x, x), (x, y))


def test_missing_components_not_vacuous_success() -> None:
    assert not audit.components_match_alias(None, ())
    assert not audit.components_match_alias((), None)
    assert audit.components_match_alias((), ())


def test_strict_preflight_rejects_unreviewed_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    replies = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "wrong-head",
    }
    monkeypatch.setattr(audit, "git", lambda root, *args: replies[args])
    with pytest.raises(RuntimeError, match="unreviewed"):
        audit.preflight(tmp_path, remote=False)


def test_preflight_rejects_dirty_tracked_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    replies = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): " M file.py",
    }
    monkeypatch.setattr(audit, "git", lambda root, *args: replies[args])
    with pytest.raises(RuntimeError, match="tracked changes"):
        audit.preflight(tmp_path, remote=False)


def test_dry_run_does_not_call_proof_engine(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root, remote: {
        "branch": "develop", "head": audit.REVIEWED_HEAD, "source_guard": "PASS",
    })
    monkeypatch.setattr(audit, "inspect_live", lambda root: pytest.fail("no runtime on dry run"))
    assert audit.run(tmp_path, dry_run=True, remote=False) == 0
    report = list((tmp_path / "EHPProofTracerRecovery").glob("*/audit.json"))
    assert len(report) == 1
    saved = json.loads(report[0].read_text(encoding="utf-8"))
    assert saved["result"] == "DRY_RUN_PASS"
    assert saved["tracked_unchanged"] is True
    assert saved["production_modified"] is False


def test_unchanged_source_first_policy() -> None:
    assert audit.TARGETS == (8, 9, 10)
    assert all(len(blob) == 40 for blob in audit.REVIEWED_BLOBS.values())
