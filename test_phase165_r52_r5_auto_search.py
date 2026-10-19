"""R52-R5: fresh typed proof search; no historical replay."""
from types import SimpleNamespace

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r5_auto_search import (
    GroupStructureSearchGoal,
    search_group_structure_automatically,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _discovery(*, content=None, linked=False):
    target = TodaPrimaryGroup(group_dimension=4, sphere_dimension=3)
    statement = content if content is not None else Relation(
        lhs=target,
        rhs=FiniteCyclicGroup(order=2, generator="eta_3"),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="source-1",
        kind=ReferenceKind.PROPOSITION,
        locator="Synthetic proposition (test only)",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="statement-1",
        reference_id="source-1",
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    links = (
        (ProofStepLink(
            assertion_id="statement-1",
            step=ProofStep(
                conclusion=statement,
                premises=(),
                rule=ProofRule.GIVEN,
            ),
        ),)
        if linked else ()
    )
    bridge = RegistryBridgeResult(registry, (), links)
    return SimpleNamespace(bridge=bridge, expansion_provider=lambda goal: ())


def test_r5_search_executes_registered_typed_goal():
    result = search_group_structure_automatically(
        n=3, k=1, discovery=_discovery(linked=True),
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(result.proven_steps) == 1
    assert result.conclusion == result.proven_steps[0].conclusion


def test_r5_unlinked_claim_not_promoted_to_proof():
    result = search_group_structure_automatically(
        n=3, k=1, discovery=_discovery(linked=False),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert not result.proven_steps
    assert result.open_goals


def test_r5_archived_text_not_treated_as_typed_conclusion():
    result = search_group_structure_automatically(
        n=3, k=1, discovery=_discovery(content="pi4^3 = Z/2"),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert isinstance(result.open_goals[-1], GroupStructureSearchGoal)
    assert any("未登録" in diagnostic for diagnostic in result.diagnostics)


def test_r5_not_restricted_to_previously_audited_112_groups():
    result = search_group_structure_automatically(
        n=100, k=20, discovery=_discovery(content="source archive only"),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.target.group_dimension == 120
    assert result.target.sphere_dimension == 100


def test_r5_invalid_indices_rejected_before_discovery():
    with pytest.raises(ValueError):
        search_group_structure_automatically(n=1, k=1, discovery=_discovery())


def test_r5_does_not_invoke_legacy_replay(monkeypatch):
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(
        auto, "search_registered_partial_proof",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("search actually invoked")),
    )
    with pytest.raises(RuntimeError, match="search actually invoked"):
        auto.search_group_structure_automatically(
            n=3, k=1, discovery=_discovery(),
        )


def test_r5_flask_progress_form_starts_actual_search(monkeypatch):
    from web_app import create_app
    import phase165_r55_nk_only_goal as registered
    from phase165_r52_partial_proof import make_partial_proof_result
    seen = []

    def actual(*, n, k, **kwargs):
        seen.append((n, k))
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("unproved",),
            diagnostics=("Registered search has no derivation",),
        )

    monkeypatch.setattr(registered, "search_group_from_registered_goal", actual)
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof_progress", "n": "3", "k": "1",
    })
    assert response.status_code == 200
    assert seen == [(3, 1)]
    assert "証明未完成".encode("utf-8") in response.data
    assert b"not_searched" not in response.data


def test_r5_group_query_also_starts_search(monkeypatch):
    import web_app
    from web_app import create_app
    from web_group_query import WebGroupQueryView
    from toda_calculation_result import TodaCalculationStatus
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    import phase165_r52_r5_auto_search as auto
    called = []

    monkeypatch.setattr(
        web_app, "build_standard_web_group_query_view",
        lambda n, k: WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None,
        ),
    )

    def render(n, k):
        called.append((n, k))
        result = auto.search_group_structure_automatically(
            n=n, k=k, discovery=_discovery(content="untyped")
        )
        return build_partial_web_group_proof_view(result)

    monkeypatch.setattr(web_app, "build_group_proof_progress_view", render)
    response = create_app().test_client().post("/", data={
        "form_kind": "group", "n": "3", "k": "1",
    })
    assert response.status_code == 200
    assert called == [(3, 1)]
    assert "証明未完成".encode("utf-8") in response.data
