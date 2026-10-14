"""Exercise the new production facade functions with an isolated canonical search."""
import ast
from pathlib import Path
import sys
from types import ModuleType

sys.path.insert(0, str(Path(__file__).parent))
from apply import FUNCTIONS


class FakeQuery:
    def __init__(self, n, k):
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
            raise ValueError('invalid n')
        if not isinstance(k, int) or isinstance(k, bool):
            raise ValueError('invalid k')
        self.n, self.k = n, k


def _functions_with_stub(monkeypatch):
    module = ModuleType('phase165_r52_r5_auto_search')
    calls = []
    def search_group_structure_automatically(*, n, k):
        calls.append((n,k))
        return {'typed_partial_result': (n, k)}
    module.search_group_structure_automatically = search_group_structure_automatically
    monkeypatch.setitem(sys.modules, module.__name__, module)
    namespace = {'TodaGroupQuery': FakeQuery}
    exec(compile(ast.parse(FUNCTIONS), '<new-facade-functions>', 'exec'), namespace)
    return namespace, calls


def test_real_function_delegates_to_common_search(monkeypatch):
    ns, calls = _functions_with_stub(monkeypatch)
    result = ns['build_standard_toda_partial_result'](2, 1)
    assert result == {'typed_partial_result': (2, 1)}
    assert calls == [(2, 1)]


def test_typed_query_entry_returns_same_result(monkeypatch):
    ns, calls = _functions_with_stub(monkeypatch)
    result = ns['build_toda_partial_result'](FakeQuery(3, 2))
    assert result == {'typed_partial_result': (3, 2)}
    assert calls == [(3, 2)]


def test_typed_entry_rejects_non_query(monkeypatch):
    ns, calls = _functions_with_stub(monkeypatch)
    try:
        ns['build_toda_partial_result']((2, 1))
    except TypeError:
        pass
    else:
        raise AssertionError('non-query accepted')
    assert calls == []
