import importlib.util
import sys
import types
from pathlib import Path


def test_typed_facade_can_run_without_legacy_repository(monkeypatch):
    # Supply only a group-query class and the typed search function.
    calls = []
    group_query = types.ModuleType('toda_group_query')
    class TodaGroupQuery:
        def __init__(self, n, k):
            self.n, self.k = n, k
    group_query.TodaGroupQuery = TodaGroupQuery
    search = types.ModuleType('phase165_r52_r5_auto_search')
    def search_group_structure_automatically(*, n, k):
        calls.append((n, k))
        return ('partial', n, k)
    search.search_group_structure_automatically = search_group_structure_automatically
    monkeypatch.setitem(sys.modules, 'toda_group_query', group_query)
    monkeypatch.setitem(sys.modules, 'phase165_r52_r5_auto_search', search)
    filename = Path(__file__).with_name('toda_typed_group_facade.py')
    spec = importlib.util.spec_from_file_location('r52_isolated_facade_test', filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build_standard_toda_partial_result(2, 1) == ('partial', 2, 1)
    assert module.build_toda_partial_result(TodaGroupQuery(3, 2)) == ('partial', 3, 2)
    assert calls == [(2, 1), (3, 2)]
