from types import SimpleNamespace
import pytest


def _module():
    import web_group_proof
    return web_group_proof


def test_r33_incomplete_proof_is_presentable(monkeypatch):
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    import phase165_r52_r5_auto_search as search
    module = _module()
    calls = []

    def fake_search(*, n, k):
        calls.append((n, k))
        return make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED, diagnostics=('typed premise absent',))

    monkeypatch.setattr(search, 'search_group_structure_automatically', fake_search)
    view = module.build_standard_web_group_proof_view(2, 1)
    assert calls == [(2, 1)]
    assert view.partial_result is True
    assert view.n == 2 and view.k == 1
    assert view.rendered_lines


def test_r33_modes_preserved(monkeypatch):
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    import phase165_r52_r5_auto_search as search
    module = _module()
    monkeypatch.setattr(search, 'search_group_structure_automatically', lambda *, n, k: make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED, diagnostics=('missing',)))
    for mode in ('trace', 'outline', 'narrative'):
        view = module.build_standard_web_group_proof_view(3, 1, max_depth=1, mode=mode)
        assert view.mode == mode
        assert view.max_depth == 1
        assert view.partial_result


def test_r33_rejects_invalid_depth_before_search():
    with pytest.raises((TypeError, ValueError)):
        _module().build_standard_web_group_proof_view(3, 1, max_depth=-1)


def test_r33_no_legacy_standard_builder_call():
    import ast
    import inspect
    node = ast.parse(inspect.getsource(_module().build_standard_web_group_proof_view))
    assert 'build_standard_toda_report' not in {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
