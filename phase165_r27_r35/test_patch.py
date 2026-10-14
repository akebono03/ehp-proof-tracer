from types import SimpleNamespace


def test_r35_generator_web_uses_typed_lookup(monkeypatch):
    import web_generator_exploration as module
    import phase165_r27_r34_typed_lookup as typed
    from expression import GeneratorSymbol
    monkeypatch.setattr(typed, 'search_typed_generator_statements', lambda generator_input: SimpleNamespace(
        status=typed.TypedLookupStatus.SEARCH_FAILED, proven_steps=(),
        open_goals=(), diagnostics=('not registered',),
    ))
    view = module.build_standard_web_generator_exploration_view('eta_3')
    assert view.search_status == 'search_failed'
    assert view.occurrence_count == 0
    assert view.diagnostics == ('not registered',)


def test_r35_operation_web_exposes_status(monkeypatch):
    import web_operation_query as module
    import phase165_r27_r34_typed_lookup as typed
    monkeypatch.setattr(typed, 'search_typed_operation_statements', lambda query_input: SimpleNamespace(
        status=typed.TypedLookupStatus.SEARCH_FAILED, proven_steps=(),
        open_goals=('missing typed goal',), diagnostics=('not registered',),
    ))
    view = module.build_standard_web_operation_query_view('E(nu_5)')
    assert view.search_status == 'search_failed'
    assert view.open_goal_count == 1
    assert view.found is False
    assert view.diagnostics == ('not registered',)


def test_r35_cli_explore_uses_typed_lookup(monkeypatch, capsys):
    import main
    import phase165_r27_r34_typed_lookup as typed
    monkeypatch.setattr(typed, 'search_typed_generator_statements', lambda generator_input: SimpleNamespace(
        status=typed.TypedLookupStatus.SEARCH_FAILED, proven_steps=(),
        open_goals=('a',), diagnostics=('no evidence',),
    ))
    assert main._run_explore_command('eta_3') == 1
    output = capsys.readouterr().out
    assert 'search_failed' in output
    assert 'no evidence' in output


def test_r35_old_generator_facade_not_called():
    import inspect
    import web_generator_exploration
    assert 'explore_standard_repository_generator_input(' not in inspect.getsource(
        web_generator_exploration.build_standard_web_generator_exploration_view)
