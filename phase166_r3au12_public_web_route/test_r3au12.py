from types import SimpleNamespace

from phase166_r3au12_public_web_route import audit


def test_r3au12_standard_entry(monkeypatch):
    import web_group_proof
    import web_group_proof_common
    monkeypatch.setattr(web_group_proof_common, "WebGroupProofView", SimpleNamespace)
    expected = SimpleNamespace(key="generic-partial-proof", partial_result=True, conclusion_latex="test", rendered_lines=(), steps=(), mode="narrative")
    monkeypatch.setattr(web_group_proof, "build_standard_web_group_proof_view", lambda **kwargs: expected)
    monkeypatch.setattr(audit, "source_checks", lambda: {"checked": True})
    actual = audit.inspect_view(3, 2, "standard")
    assert actual["key"] == "generic-partial-proof"
    assert actual["partial_result"] is True


def test_r3au12_flask_entry(monkeypatch):
    import phase165_r52_r4_flask_bridge as flask_bridge
    import web_group_proof_common
    monkeypatch.setattr(web_group_proof_common, "WebGroupProofView", SimpleNamespace)
    expected = SimpleNamespace(key="generic-complete-proof", partial_result=False, conclusion_latex="test", rendered_lines=("line",), steps=(), mode="narrative")
    monkeypatch.setattr(flask_bridge, "build_group_proof_progress_view", lambda **kwargs: expected)
    actual = audit.inspect_view(3, 2, "flask")
    assert actual["key"] == "generic-complete-proof"
    assert actual["rendered_line_count"] == 1


def test_r3au12_source_route_includes_adapter():
    checks = audit.source_checks()
    assert checks["standard_calls_adapter"]
    assert checks["flask_bridge_calls_adapter"]
    assert checks["adapter_uses_open_goals_if_partial"]
    assert checks["adapter_uses_markdown_renderer"]
