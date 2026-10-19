from pathlib import Path
import ast, shutil, datetime

ROOT=Path.cwd()
REPLACEMENTS={
 'test_phase165_r52_r4_flask_connection.py': {
 'test_failed_search_state_is_not_presented_as_conclusion': '''def test_failed_search_state_is_not_presented_as_conclusion(monkeypatch):
    import phase165_r55_nk_only_goal as registered
    def failed(**kwargs):
        return make_partial_proof_result(
            n=kwargs["n"], k=kwargs["k"],
            status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("unproved",),
            diagnostics=("No registered rule",),
        )
    monkeypatch.setattr(registered, "search_group_from_registered_goal", failed)
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof_progress", "n": "17", "k": "4",
    })
    assert response.status_code == 200
    assert "証明未完成".encode("utf-8") in response.data
    assert b"No registered rule" in response.data
    assert b"Proof target" in response.data
    assert "□".encode("utf-8") not in response.data
''',
 },
 'test_phase165_r52_r5_auto_search.py': {
 'test_r5_flask_progress_form_starts_actual_search': '''def test_r5_flask_progress_form_starts_actual_search(monkeypatch):
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
''',
 },
 'test_phase165_r52_r8_show_proof_route.py': {
 'test_r8_unconfigured_proof_calls_partial_search': '''def test_r8_unconfigured_proof_calls_partial_search(monkeypatch):
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    called = []

    def partial(**kwargs):
        called.append(kwargs)
        return build_partial_web_group_proof_view(
            make_partial_proof_result(
                n=kwargs["n"], k=kwargs["k"],
                status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=("missing proof",),
                diagnostics=("Typed goal has no registered derivation",),
            ), max_depth=kwargs["max_depth"],
        )

    monkeypatch.setattr(web_app, "build_group_proof_progress_view", partial)
    response = _post(3, 1)
    assert response.status_code == 200
    assert called == [{"n": 3, "k": 1, "max_depth": 2}]
    assert "証明未完成".encode("utf-8") in response.data
''',
 'test_r8_registered_proof_does_not_fall_back': '''def test_r8_registered_proof_does_not_fall_back(monkeypatch):
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    calls = []
    def registered(**kwargs):
        calls.append(kwargs)
        return build_partial_web_group_proof_view(
            make_partial_proof_result(
                n=kwargs["n"], k=kwargs["k"],
                status=ProofSearchStatus.SEARCH_FAILED,
                diagnostics=("Registered proof test fixture",),
            ), max_depth=kwargs["max_depth"],
        )
    monkeypatch.setattr(web_app, "build_group_proof_progress_view", registered)
    assert _post(2, 1).status_code == 200
    assert calls == [{"n": 2, "k": 1, "max_depth": 2}]
''',
 'test_r8_actual_pi32_registered_narrative_unchanged': '''def test_r8_actual_pi32_registered_narrative_unchanged():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(
        2, 1, max_depth=2, mode="narrative"
    )
    assert view.phase.startswith("165")
    body = "\\n".join(
        line.prefix + " " + " ".join(
            segment.value for segment in line.segments
        ) for line in view.rendered_lines
    )
    assert "証明対象" in body
    assert "使用する結果" in body
    assert "証明" in body
''',
 }
}

def patch():
    backup=ROOT/'phase165_r6_audit_results'/'runner_backup'/('web_route_alignment_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    pending=[]
    for name, funcs in REPLACEMENTS.items():
        path=ROOT/name
        if not path.is_file(): raise RuntimeError(f'Missing {path}')
        src=path.read_text(encoding='utf-8')
        tree=ast.parse(src)
        nodes={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        for fn, replacement in funcs.items():
            if fn not in nodes: raise RuntimeError(f'Missing {fn} in {name}')
            ast.parse(replacement)
        lines=src.splitlines(keepends=True)
        for fn in sorted(funcs,key=lambda fn:nodes[fn].lineno,reverse=True):
            node=nodes[fn]
            lines[node.lineno-1:node.end_lineno]=[funcs[fn].rstrip()+'\n']
        updated=''.join(lines)
        ast.parse(updated)
        pending.append((path,src,updated))
    backup.mkdir(parents=True,exist_ok=False)
    for path,src,updated in pending:
        shutil.copy2(path,backup/path.name)
        path.write_text(updated,encoding='utf-8')
        print('PATCHED:',path)
    print('BACKUP:',backup)

if __name__=='__main__': patch()
