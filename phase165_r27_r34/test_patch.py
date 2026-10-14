import ast
from pathlib import Path
from types import SimpleNamespace

from phase165_r27_r34_typed_lookup import TypedLookupStatus, search_typed_statement_matches
from unified_statement_registry import AssertionOrigin


def test_r34_no_assertions_fail_closed():
    result = search_typed_statement_matches(lambda item: True, discovery=SimpleNamespace(
        bridge=SimpleNamespace(registry=SimpleNamespace(_assertions={})), expansion_provider=lambda goal: (),
    ))
    assert result.status is TypedLookupStatus.SEARCH_FAILED
    assert result.proven_steps == ()


def test_r34_no_match_fail_closed():
    a = SimpleNamespace(assertion_id='a', origin=AssertionOrigin.FIXED_STATEMENT, content='a')
    result = search_typed_statement_matches(lambda item: False, discovery=SimpleNamespace(
        bridge=SimpleNamespace(registry=SimpleNamespace(_assertions={'a': a})), expansion_provider=lambda goal: (),
    ))
    assert result.status is TypedLookupStatus.SEARCH_FAILED


def test_r34_web_operation_uses_typed_backend():
    import web_operation_query
    source = Path(web_operation_query.__file__).read_text(encoding='utf-8')
    tree = ast.parse(source)
    fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'build_standard_web_operation_query_view')
    assert 'search_typed_operation_statements' in ast.unparse(fn)
    assert 'query_standard_repository_operation_input' not in ast.unparse(fn)


def test_r34_web_operation_unproved_not_found(monkeypatch):
    import web_operation_query
    import phase165_r27_r34_typed_lookup as lookup
    from phase165_r27_r34_typed_lookup import TypedLookupResult
    monkeypatch.setattr(lookup, 'search_typed_operation_statements', lambda query: TypedLookupResult(
        TypedLookupStatus.SEARCH_FAILED, (), (), ('unproved',),
    ))
    view = web_operation_query.build_standard_web_operation_query_view('E(nu_5)')
    assert not view.found
    assert view.items == ()
