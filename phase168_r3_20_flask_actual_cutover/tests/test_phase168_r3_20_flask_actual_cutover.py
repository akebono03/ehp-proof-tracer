from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from web_app import create_app
from web_group_proof import build_standard_web_group_proof_view


def _text(view):
    return "\\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )


def test_r320_flask_bridge_uses_explicit_model_for_normal_group(monkeypatch):
    import web_group_proof
    original = web_group_proof.build_standard_web_group_proof_view
    seen = []

    def spy(**kwargs):
        seen.append(kwargs.copy())
        return original(**kwargs)

    monkeypatch.setattr(web_group_proof, "build_standard_web_group_proof_view", spy)
    view = build_group_proof_progress_view(n=2, k=2)
    assert seen == [{"n": 2, "k": 2, "max_depth": 2, "mode": "narrative", "citation_source": "model"}]
    expected = original(n=2, k=2, citation_source="model")
    assert _text(view) == _text(expected)


def test_r320_real_flask_post_calls_model_path(monkeypatch):
    import web_group_proof
    original = web_group_proof.build_standard_web_group_proof_view
    seen = []

    def spy(**kwargs):
        seen.append(kwargs.copy())
        return original(**kwargs)

    monkeypatch.setattr(web_group_proof, "build_standard_web_group_proof_view", spy)
    response = create_app().test_client().post("/", data={
        "form_kind": "group_proof", "n": "2", "k": "2", "group_proof_depth": "2"
    })
    assert response.status_code == 200
    assert seen and seen[-1]["citation_source"] == "model"
    assert seen[-1]["n"] == 2 and seen[-1]["k"] == 2


def test_r320_standard_group_form_calls_model_path(monkeypatch):
    import web_group_proof
    original = web_group_proof.build_standard_web_group_proof_view
    seen = []

    def spy(**kwargs):
        seen.append(kwargs.copy())
        return original(**kwargs)

    monkeypatch.setattr(web_group_proof, "build_standard_web_group_proof_view", spy)
    response = create_app().test_client().post("/", data={
        "form_kind": "group", "n": "2", "k": "2"
    })
    assert response.status_code == 200
    assert seen and seen[-1]["citation_source"] == "model"
