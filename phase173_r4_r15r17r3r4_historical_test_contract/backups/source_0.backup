"""Repository-dependent real source-first certificates and common Web projection."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    abstract_invariants_latex,
    render_certified_abstract_section,
)
from proof import ProofRule


@pytest.mark.parametrize("raw, expected", (
    ((), "0"),
    ((("finite", 2),) * 8, r"\left(\mathbb{Z}/2\right)^{8}"),
    ((("free", 0),), r"\mathbb{Z}"),
    ((("free", 0),) * 2 + (("finite", 4),),
     r"\mathbb{Z}/4 \oplus \left(\mathbb{Z}\right)^{2}"),
))
def test_abstract_invariants_render_without_generator_names(raw, expected) -> None:
    assert abstract_invariants_latex(raw) == expected


@pytest.mark.parametrize("invalid", (
    (("finite", 1),),
    (("free", 2),),
    (("finite", True),),
    (("unknown", 4),),
    (("finite", 2, 3),),
))
def test_invalid_invariants_not_rendered(invalid) -> None:
    with pytest.raises(ValueError):
        abstract_invariants_latex(invalid)


@pytest.fixture(scope="module")
def proved_abstract_result():
    bridge = build_shared_typed_bridge()
    source = search_source_first_abstract(k=31, bridge=bridge)
    assert source is not None
    assert source.root_step.rule is ProofRule.INFERENCE
    goal = exact_prior_database_result(4, 31)
    assert source.proof_target == goal
    abstract = CertifiedAbstractStructure(
        group=source.conclusion.group,
        invariant_summands=source.conclusion.invariant_summands,
        proof_step=source.root_step,
    )
    result = make_partial_proof_result(
        n=4, k=31, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,), diagnostics=("記名生成元の証明は未解決",),
    )
    from dataclasses import replace
    return replace(result, abstract_structure=abstract)


def test_source_verified_abstract_markdown_is_explicitly_partial(proved_abstract_result) -> None:
    section = render_certified_abstract_section(proved_abstract_result)
    assert "証明済みの抽象群構造" in section
    assert r"\pi_{35}^{4} \cong \left(\mathbb{Z}/2\right)^{8}" in section
    assert "記名生成元の対応は未証明" in section
    assert proved_abstract_result.status is ProofSearchStatus.SEARCH_FAILED
    assert proved_abstract_result.conclusion is None
    assert len(proved_abstract_result.open_goals) == 1


def test_shared_model_backed_web_displays_abstract_and_keeps_named_pending(proved_abstract_result) -> None:
    model = build_proof_narrative_model(proved_abstract_result)
    view = build_partial_web_group_proof_view(
        proved_abstract_result, mode="narrative", narrative_model=model,
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert any(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines)
    assert any(r"\pi_{35}^{4}" in (line.statement_latex or "")
               and r"\cong" in (line.statement_latex or "")
               for line in view.rendered_lines)
    assert any(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines)


def test_shared_fallback_web_uses_same_abstract_projection(proved_abstract_result) -> None:
    view = build_partial_web_group_proof_view(
        proved_abstract_result, mode="outline",
    )
    assert view.partial_result
    assert sum(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines) == 1


def test_trace_route_remains_without_added_narrative(proved_abstract_result) -> None:
    view = build_partial_web_group_proof_view(proved_abstract_result, mode="trace")
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert view.rendered_lines == ()


def test_no_abstract_sidecar_preserves_original_partial_text(proved_abstract_result) -> None:
    from dataclasses import replace
    bare = replace(proved_abstract_result, abstract_structure=None)
    assert render_certified_abstract_section(bare) == ""
    view = build_partial_web_group_proof_view(
        bare, mode="narrative", narrative_model=build_proof_narrative_model(bare),
    )
    assert view.key == "generic-partial-proof"
    assert not any(line.prefix == "証明済みの抽象群構造"
                   for line in view.rendered_lines)
