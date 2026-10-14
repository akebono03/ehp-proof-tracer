"""R27-R6: reject old proof paths and false proof-completion on public entries."""
from pathlib import Path
from types import SimpleNamespace

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r5_auto_search import search_group_structure_automatically
from web_app import create_app


def test_default_auto_search_does_not_call_legacy_report(monkeypatch):
    import phase165_r9_production_wiring as wiring
    import toda_calculation_facade as old
    from phase165_r52_r5_auto_search import GroupStructureSearchGoal
    from unified_statement_registry import UnifiedStatementRegistry
    from phase163_r4_registry_bridge import RegistryBridgeResult

    def forbidden(*args, **kwargs):
        raise AssertionError('legacy report was called')

    monkeypatch.setattr(old, 'build_standard_toda_report', forbidden)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(wiring, 'discover_goal_search_inputs', lambda: SimpleNamespace(
        bridge=bridge, expansion_provider=lambda goal: (),
    ))
    result = search_group_structure_automatically(n=3, k=1)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert isinstance(result.open_goals[0], GroupStructureSearchGoal)


def test_regular_group_proof_uses_common_progress_not_legacy_renderer(monkeypatch):
    import web_app

    def forbidden(*args, **kwargs):
        raise AssertionError('legacy route called')

    monkeypatch.setattr(web_app, 'build_standard_web_group_query_view', forbidden)
    if hasattr(web_app, 'build_standard_web_group_proof_view'):
        monkeypatch.setattr(web_app, 'build_standard_web_group_proof_view', forbidden)
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    def replacement(*, n, k, max_depth=2):
        return build_partial_web_group_proof_view(
            make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=('unproven',), diagnostics=('No typed derivation',)),
            max_depth=max_depth,
        )

    monkeypatch.setattr(web_app, 'build_group_proof_progress_view', replacement)
    response = create_app().test_client().post('/', data={
        'form_kind': 'group_proof', 'n': '3', 'k': '1',
        'group_proof_depth': '2', 'group_proof_mode': 'narrative',
    })
    assert response.status_code == 200
    assert "証明未完成".encode("utf-8") in response.data
    assert b'No typed derivation' in response.data
    assert '□'.encode('utf-8') not in response.data


def test_no_old_constructor_in_default_auto_entry():
    import inspect
    import phase165_r52_r5_auto_search as auto
    source = inspect.getsource(auto.search_group_structure_automatically)
    assert 'build_standard_toda_report' not in source
    assert 'search_shared_group_goal' not in source
