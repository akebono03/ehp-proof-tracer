"""Offline formatter validation with inert result stubs, not mathematical evidence."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType

import pytest


@pytest.fixture
def projection(monkeypatch):
    module = ModuleType("phase165_r52_partial_proof")

    class ProofSearchStatus(Enum):
        PARTIAL = "partial"
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"
        NOT_SEARCHED = "not_searched"

    @dataclass(frozen=True)
    class Target:
        group_dimension: int
        sphere_dimension: int

    @dataclass(frozen=True)
    class CertifiedAbstractStructure:
        group: object
        invariant_summands: tuple

    @dataclass(frozen=True)
    class PartialProofResult:
        target: Target
        status: ProofSearchStatus
        abstract_structure: object | None = None
        conclusion: object | None = None

    module.CertifiedAbstractStructure = CertifiedAbstractStructure
    module.PartialProofResult = PartialProofResult
    module.ProofSearchStatus = ProofSearchStatus
    monkeypatch.setitem(sys.modules, module.__name__, module)
    path = Path(__file__).resolve().parents[1] / "projection.py"
    spec = spec_from_file_location("phase173_r4_r15r9_isolated_projection", path)
    assert spec is not None and spec.loader is not None
    loaded = module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded, module, Target


def test_multiple_finite_summands(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex((("finite", 2),) * 8) == (
        r"\left(\mathbb{Z}/2\right)^{8}"
    )


def test_empty_invariants_render_zero(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex(()) == "0"


def test_mixed_free_and_finite_summands(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex(
        (("free", 0), ("finite", 4), ("free", 0))
    ) == r"\mathbb{Z}/4 \oplus \left(\mathbb{Z}\right)^{2}"


def test_wrong_finite_order_is_rejected(projection) -> None:
    render, _, _ = projection
    for data in ((("finite", 0),), (("finite", True),), (("free", 2),)):
        with pytest.raises(ValueError):
            render.abstract_invariants_latex(data)


def test_verified_sidecar_is_rendered_as_abstract_only(projection) -> None:
    render, m, Target = projection
    group = Target(35, 4)
    sidecar = m.CertifiedAbstractStructure(group, (("finite", 2),) * 8)
    pending = m.PartialProofResult(group, m.ProofSearchStatus.SEARCH_FAILED, sidecar)
    markdown = render.render_certified_abstract_section(pending)
    assert r"\pi_{35}^{4} \cong \left(\mathbb{Z}/2\right)^{8}" in markdown
    assert "証明済みの抽象群構造" in markdown
    assert "記名生成元の対応は未証明" in markdown


def test_unproved_result_has_no_extra_section(projection) -> None:
    render, m, Target = projection
    pending = m.PartialProofResult(Target(35, 4), m.ProofSearchStatus.SEARCH_FAILED)
    assert render.render_certified_abstract_section(pending) == ""


def test_forged_complete_result_is_rejected(projection) -> None:
    render, m, Target = projection
    target = Target(35, 4)
    sidecar = m.CertifiedAbstractStructure(target, (("finite", 2),) * 8)
    complete = m.PartialProofResult(target, m.ProofSearchStatus.COMPLETE, sidecar)
    with pytest.raises(ValueError, match="unverified"):
        render.render_certified_abstract_section(complete)


def test_wrong_abstract_target_is_rejected(projection) -> None:
    render, m, Target = projection
    sidecar = m.CertifiedAbstractStructure(Target(36, 4), (("finite", 2),) * 8)
    pending = m.PartialProofResult(Target(35, 4), m.ProofSearchStatus.PARTIAL, sidecar)
    with pytest.raises(ValueError, match="unverified"):
        render.render_certified_abstract_section(pending)
