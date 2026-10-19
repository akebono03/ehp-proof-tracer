"""R57-R1: all standard Web queries use the same registered goal selector."""
import web_group_proof
import phase165_r55_nk_only_goal
import phase165_r52_r3_web_adapter
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result


def test_standard_route_uses_r55_for_arbitrary_nk(monkeypatch):

    calls = []

    sentinel = object()

    def search(*, n, k, goal=None):

        calls.append((n, k, goal))

        return sentinel

    def adapt(result, *, max_depth, mode):

        assert result is sentinel

        assert (max_depth, mode) == (2, "narrative")

        return "shared-adapter-result"

    monkeypatch.setattr(phase165_r55_nk_only_goal, "search_group_from_registered_goal", search)

    monkeypatch.setattr(phase165_r52_r3_web_adapter, "build_partial_web_group_proof_view", adapt)

    assert web_group_proof.build_standard_web_group_proof_view(3, 2) == "shared-adapter-result"

    assert calls == [(3, 2, None)]


def test_standard_route_rejects_invalid_mode_before_search(monkeypatch):
    def forbidden(**kwargs):
        raise AssertionError("search should not start")
    monkeypatch.setattr(phase165_r55_nk_only_goal, "search_group_from_registered_goal", forbidden)
    try:
        web_group_proof.build_standard_web_group_proof_view(2, 1, mode="broken")
    except ValueError as e:
        assert "mode" in str(e)
    else:
        raise AssertionError("invalid mode accepted")


def test_standard_route_real_pi32_public_renderer():
    view = web_group_proof.build_standard_web_group_proof_view(2, 1)
    rendered = " ".join(str(line) for line in view.rendered_lines)
    assert view.rendered_lines
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert "GeneratorSuspension" not in rendered
    assert "出典情報は検証済み ProofStep との対応確認待ち" not in rendered
