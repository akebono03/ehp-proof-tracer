"""Targeted fail-closed migration tests."""
from types import SimpleNamespace

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from toda_calculation_result import TodaCalculationStatus


def _incomplete(n, k):
    return make_partial_proof_result(
        n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("not proven",), diagnostics=("No typed rule",),
    )


def test_web_query_never_uses_legacy_report(monkeypatch):
    import web_group_query
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(auto, 'search_group_structure_automatically', _incomplete)
    result = web_group_query.build_standard_web_group_query_view(11, 7)
    assert result.status is TodaCalculationStatus.NOT_FOUND
    assert result.result_latex is None
    assert result.proof_available is False


def test_cli_normal_query_is_incomplete(monkeypatch, capsys):
    import main
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(auto, 'search_group_structure_automatically', _incomplete)
    assert main.main(['11', '7']) == 1
    output = capsys.readouterr().out
    assert '証明未完成' in output
    assert '□' not in output


def test_cli_group_proof_is_incomplete(monkeypatch, capsys):
    import main
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(auto, 'search_group_structure_automatically', _incomplete)
    assert main.main(['group-proof', '11', '7']) == 1
    output = capsys.readouterr().out
    assert '証明未完成' in output
    assert '□' not in output


def test_web_boundary_domain_does_not_use_prover(monkeypatch):
    import web_group_query
    import phase165_r52_r5_auto_search as auto
    monkeypatch.setattr(auto, 'search_group_structure_automatically', lambda **kw: (_ for _ in ()).throw(AssertionError('unexpected')))
    result = web_group_query.build_standard_web_group_query_view(3, -3)
    assert result.proof_available is False
